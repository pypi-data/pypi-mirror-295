import asyncio
import os
from urllib.parse import urlparse

from tqdm import tqdm
from tqdm.asyncio import tqdm_asyncio

from src.performance import PerformanceMetrics
from src.utils import write_performance_metrics_to_csv, delete_dir, load_yaml_file, create_dir_in_tmp
from src.utils.config import config

class PerformanceMetricsFactory:
    def __init__(self, urls, num_iterations, headless=False, headers_file: str | None = None, cookies_file: str | None = None):
        self.urls = urls
        self.num_iterations = num_iterations
        self.headless = headless
        self.semaphore = asyncio.Semaphore(config.max_browser_instances)

        self.extra_headers = load_yaml_file(headers_file)
        self.cookies = load_yaml_file(cookies_file)

        self.tmp_output_dir = os.path.join(config.tmp_dir, 'performance')
        create_dir_in_tmp('performance')


    async def create_and_run(self, url):
        async with self.semaphore:
            metrics = PerformanceMetrics(url, self.num_iterations, self.tmp_output_dir, self.headless, self.extra_headers, self.cookies)
            return await metrics.gather_metrics()

    async def run_all(self, concurrent=True):
        if concurrent:
            tasks = [self.create_and_run(url) for url in self.urls]
            return await tqdm_asyncio.gather(*tasks, desc="Gathering metrics")
        else:
            results = []
            for url in tqdm(self.urls, desc="Gathering metrics"):
                result = await self.create_and_run(url)
                results.append(result)
            return results

    def run(self, output_file_path, concurrent=True):
        loop = asyncio.get_event_loop()
        all_metrics = loop.run_until_complete(self.run_all(concurrent=concurrent))

        grouped_metrics = {}
        for metric_list in all_metrics:
            for metric in metric_list:
                domain = urlparse(metric['url']).netloc
                if domain not in grouped_metrics:
                    grouped_metrics[domain] = []
                grouped_metrics[domain].append(metric)

        flattened_metrics = []
        for domain, metrics in grouped_metrics.items():
            flattened_metrics.extend(metrics)
            average = PerformanceMetrics.compute_averages(metrics)[0]
            flattened_metrics.append(average)

        write_performance_metrics_to_csv(flattened_metrics, output_file_path)

        delete_dir(config.tmp_dir, 10)

