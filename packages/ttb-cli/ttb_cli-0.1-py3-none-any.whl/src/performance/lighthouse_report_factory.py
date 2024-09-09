import os
import time
from concurrent.futures import ThreadPoolExecutor

from tqdm import tqdm

from src.performance import LighthouseReport
from src.utils import write_lighthouse_reports_to_csv, create_tmp_dir_, delete_file, delete_dir
from src.utils.config import config


class LighthouseReportFactory:
    def __init__(self, urls, headless=True, max_concurrent_browsers=config.max_browser_instances, preset='desktop'):
        self.urls = urls
        self.tmp_output_dir = os.path.join(config.tmp_dir, 'reports')
        self.headless = headless
        self.max_concurrent_browsers = max_concurrent_browsers
        self.preset = preset

        create_tmp_dir_('reports')

    def create_and_run_report(self, url, pbar):
        unique_filename = f"lighthouse_report_{self._sanitize_url(url)}_{int(time.time() * 1000)}.json"
        output_path = os.path.join(self.tmp_output_dir, unique_filename)

        report = LighthouseReport(url, self.tmp_output_dir, output_path, self.headless, self.preset)
        return report.run_report(pbar), output_path

    def run_all(self, concurrent=True):
        if concurrent:
            with ThreadPoolExecutor(max_workers=self.max_concurrent_browsers) as executor:
                with tqdm(total=len(self.urls), desc="Running Lighthouse reports") as pbar:
                    results = list(executor.map(lambda url: self.create_and_run_report(url, pbar), self.urls))
        else:
            results = []
            with tqdm(total=len(self.urls), desc="Running Lighthouse reports") as pbar:
                for url in self.urls:
                    results.append(self.create_and_run_report(url, pbar))
        return results

    def run(self, output_file_path, concurrent=True):
        with tqdm(total=3, desc="Lighthouse Reports Progress") as pbar:
            pbar.set_description("LHR: Running reports")
            all_reports = self.run_all(concurrent=concurrent)
            pbar.update(1)

            pbar.set_description("LHR: Writing reports to CSV")
            flattened_reports = [report[0] for report in all_reports if report[0] is not None]
            report_paths = [report[1] for report in all_reports if report[0] is not None]
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

        try:
            delete_dir(self.tmp_output_dir)
        except Exception as e:
            print(f"Error while removing directory: {e}")
