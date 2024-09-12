import asyncio
import os

import yaml
from tqdm import tqdm
from tqdm.asyncio import tqdm_asyncio

from src.performance import PerformanceMetrics
from src.utils import write_performance_metrics_to_csv, create_tmp_dir, delete_dir
from src.utils.config import config

class PerformanceMetricsFactory:
    def __init__(self, urls, num_iterations, headless=False, headers_file: str | None = None, cookies_file: str | None = None):
        self.urls = urls
        self.num_iterations = num_iterations
        self.headless = headless
        self.semaphore = asyncio.Semaphore(config.max_browser_instances)

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

        create_tmp_dir()

    async def create_and_run(self, url):
        async with self.semaphore:
            metrics = PerformanceMetrics(url, self.num_iterations, self.headless, self.extra_headers, self.cookies)
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
        flattened_metrics = [item for sublist in all_metrics for item in sublist]

        averages = PerformanceMetrics.compute_averages(flattened_metrics)
        if averages:
            flattened_metrics.append(averages)

        write_performance_metrics_to_csv(flattened_metrics, output_file_path)

        delete_dir(config.tmp_dir, 10)

