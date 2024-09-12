import asyncio
import os
import time

import yaml
from tqdm import tqdm
from tqdm.asyncio import tqdm_asyncio

from src.performance import LighthouseReport
from src.utils import write_lighthouse_reports_to_csv, create_tmp_dir_, delete_file, delete_dir, config

class LighthouseReportFactory:
    def __init__(self, urls, headless=True, max_concurrent_browsers=config.max_browser_instances, preset='desktop',
                 headers_file: str | None = None, cookies_file: str | None = None):
        self.urls = urls
        self.tmp_output_dir = os.path.join(config.tmp_dir, 'reports')
        self.headless = headless
        self.max_concurrent_browsers = max_concurrent_browsers
        self.preset = preset
        self.semaphore = asyncio.Semaphore(self.max_concurrent_browsers)

        self.extra_headers = None
        if headers_file and os.path.exists(headers_file):
            try:
                with open(headers_file, 'r') as file:
                    self.extra_headers = yaml.safe_load(file)
            except Exception as e:
                print(f"Error loading extra headers: {e}")

        self.cookies = None
        if cookies_file and os.path.exists(cookies_file):
            try:
                with open(cookies_file, 'r') as file:
                    self.cookies = yaml.safe_load(file)
            except Exception as e:
                print(f"Error loading cookies: {e}")

        create_tmp_dir_('reports')

    async def create_and_run_report(self, url, pbar):
        async with self.semaphore:
            unique_filename = f"lighthouse_report_{self._sanitize_url(url)}_{int(time.time() * 1000)}.json"
            output_path = os.path.join(self.tmp_output_dir, unique_filename)

            report = LighthouseReport(url, self.tmp_output_dir, output_path, self.headless, self.preset,
                                      self.extra_headers, self.cookies)
            return await report.run_report(pbar), output_path

    async def run_all(self, concurrent=True):
        with tqdm(total=len(self.urls), desc="Running Lighthouse reports") as pbar:
            if concurrent:
                tasks = [self.create_and_run_report(url, pbar) for url in self.urls]
                return await tqdm_asyncio.gather(*tasks)
            else:
                results = []
                for url in self.urls:
                    result = await self.create_and_run_report(url, pbar)
                    results.append(result)
                return results

    def run(self, output_file_path, concurrent=True):
        loop = asyncio.get_event_loop()
        all_reports = loop.run_until_complete(self.run_all(concurrent=concurrent))

        with tqdm(total=3, desc="Lighthouse Reports Progress") as pbar:
            pbar.set_description("LHR: Processing reports")
            flattened_reports = [report[0] for report in all_reports if report[0] is not None]
            report_paths = [report[1] for report in all_reports if report[0] is not None]
            pbar.update(1)

            pbar.set_description("LHR: Writing reports to CSV")
            write_lighthouse_reports_to_csv(flattened_reports, output_file_path)
            pbar.update(1)

            pbar.set_description("LHR: Cleaning up files")
            self._cleanup_files(report_paths)
            pbar.update(1)

        tqdm.write(f"Lighthouse reports processing completed. Output saved to {output_file_path}")

    @staticmethod
    def _sanitize_url(url):
        return url.replace('https://', '').replace('http://', '').replace('/', '_')

    def _cleanup_files(self, file_paths):
        for file_path in file_paths:
            try:
                delete_file(file_path)
            except Exception as e:
                print(f"Error while removing file: {e}")

        delete_dir(self.tmp_output_dir)
