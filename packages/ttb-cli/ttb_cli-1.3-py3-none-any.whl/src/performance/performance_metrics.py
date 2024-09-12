import os
from pyppeteer import launch
from tqdm import tqdm

from src.utils import get_current_time_ms, get_iso_timestamp, config

class PerformanceMetrics:
    def __init__(self, url: str, num_iterations: int, headless: bool = False, extra_headers: dict[str, str] | None = None, cookies: list | None = None):
        self.url = url
        self.num_iterations = num_iterations
        self.headless = headless
        self.data_dir = os.path.join(config.tmp_dir, 'chrome_data_dir_' + str(get_current_time_ms()))
        self.extra_headers = extra_headers
        self.cookies = cookies

    async def gather_metrics(self) -> list[dict]:
        browser = await self._launch_browser()
        all_metrics = []

        try:
            with tqdm(total=self.num_iterations, desc=f"Gathering metrics for {self.url}") as pbar:
                for iteration in range(1, self.num_iterations + 1):
                    metrics = await self._run_test_iteration(browser, iteration, pbar)
                    all_metrics.append(metrics)
                    pbar.update(1)
                pbar.set_description(f"Gathered metrics for {self.url}")
        finally:
            await browser.close()

        return all_metrics

    async def _launch_browser(self):
        os.mkdir(self.data_dir)
        return await launch(
            headless=self.headless,
            args=['--enable-logging', '--v=99', '--log-path=' + self.data_dir + '/logs', '--user-data-dir=' + self.data_dir],
            executablePath=config.chrome_executable_path
        )

    async def _run_test_iteration(self, browser, iteration: int, pbar: tqdm) -> dict:
        start_time = get_current_time_ms()
        test_time = get_iso_timestamp()
        page = await browser.newPage()

        ttfb, load_time, total_time, error = None, None, None, None

        try:
            if self.extra_headers:
                await page.setExtraHTTPHeaders(self.extra_headers)

            if self.cookies:
                for cookie in self.cookies:
                    if 'domain' not in cookie:
                        url_parts = self.url.split('://')
                        domain = url_parts[1] if len(url_parts) > 1 else url_parts[0]
                        domain_parts = domain.split('.')
                        if len(domain_parts) > 2:
                            cookie['domain'] = domain
                        else:
                            cookie['domain'] = '.' + domain

                    await page.setCookie(cookie)

            await page.goto(self.url, waitUntil='networkidle0', timeout=30000)
            await page.waitForSelector('body', timeout=30000)
            await page.evaluate("window.scrollTo(0, document.body.scrollHeight);")

            performance_timing = await self._get_performance_timing(page)

            ttfb = self._calculate_ttfb(performance_timing)
            load_time = self._calculate_load_time(performance_timing)
            total_time = self._calculate_total_time(start_time)

        except Exception as err:
            total_time = self._calculate_total_time(start_time)
            error = f"Error: {str(err)}"
            pbar.set_description(f"Error during iteration {iteration} for {self.url}: {err}")

        await page.close()

        return self._create_metrics_record(iteration, test_time, ttfb, load_time, total_time, error)

    @staticmethod
    async def _get_performance_timing(page) -> dict:
        return await page.evaluate("JSON.parse(JSON.stringify(window.performance.timing))")

    @staticmethod
    def _calculate_ttfb(performance_timing: dict) -> float:
        return performance_timing['responseStart'] - performance_timing['navigationStart']

    @staticmethod
    def _calculate_load_time(performance_timing: dict) -> float:
        return performance_timing['loadEventEnd'] - performance_timing['navigationStart']

    @staticmethod
    def _calculate_total_time(start_time: float) -> float:
        return get_current_time_ms() - start_time

    def _create_metrics_record(self, iteration: int, test_time: str, ttfb: float, load_time: float,
                               total_time: float, error: str) -> dict:
        return {
            'url': self.url,
            'iteration': iteration,
            'test_time': test_time,
            'ttfb': f"{ttfb:.2f}" if ttfb is not None else "N/A",
            'load_time': f"{load_time:.2f}" if load_time is not None else "N/A",
            'total_time': f"{total_time:.2f}",
            'error': error or "N/A"
        }

    @staticmethod
    def compute_averages(all_metrics: list[dict]) -> dict | None:
        ttfb_total = load_time_total = total_time_total = 0
        count = 0

        for metric in all_metrics:
            if metric['ttfb'] != "N/A":
                ttfb_total += float(metric['ttfb'])
            if metric['load_time'] != "N/A":
                load_time_total += float(metric['load_time'])
            total_time_total += float(metric['total_time'])
            count += 1

        if count == 0:
            return None

        return {
            'url': 'AVERAGES',
            'iteration': 'N/A',
            'test_time': 'N/A',
            'ttfb': f"{(ttfb_total / count):.2f}" if ttfb_total else "N/A",
            'load_time': f"{(load_time_total / count):.2f}" if load_time_total else "N/A",
            'total_time': f"{(total_time_total / count):.2f}",
            'error': "N/A"
        }
