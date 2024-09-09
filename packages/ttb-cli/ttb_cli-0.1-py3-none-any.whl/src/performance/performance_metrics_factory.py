import asyncio

import subprocess
from tqdm import tqdm
from tqdm.asyncio import tqdm_asyncio

from src.performance import PerformanceMetrics
from src.utils import write_performance_metrics_to_csv, create_tmp_dir, delete_dir
from src.utils.config import config

class PerformanceMetricsFactory:
    def __init__(self, urls, num_iterations, headless=False,):
        self.urls = urls
        self.num_iterations = num_iterations
        self.headless = headless
        self.semaphore = asyncio.Semaphore(config.max_browser_instances)

        create_tmp_dir()

    async def create_and_run(self, url):
        async with self.semaphore:
            metrics = PerformanceMetrics(url, self.num_iterations, self.headless)
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

        try:
            delete_dir(config.tmp_dir)
        except Exception as e:
            print(f"Error while removing temporary directory: {e}")
