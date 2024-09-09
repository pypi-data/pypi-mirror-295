import subprocess
import json
import os

from tqdm import tqdm

from src.utils import get_current_time_ms, create_tmp_dir_


class LighthouseReport:
    def __init__(self, url: str, temp_dir, output_path: str = 'lighthouse_report.json', headless: bool = True, preset:str = 'desktop'):
        self.url = url
        self.output_path = output_path
        self.headless = headless
        self.preset = preset

        self.temp_dir = temp_dir
        create_tmp_dir_(temp_dir)

        self.data_dir = os.path.join(self.temp_dir, 'chrome_data_dir_' + str(get_current_time_ms()))

    def run_report(self, pbar: tqdm) -> dict:
        try:
            command = ['lighthouse', self.url, '--output', 'json', '--output-path', self.output_path, '--quiet',
                       '--chrome-flags="--enable-logging --v=99 --log-path=' + self.data_dir + '/logs --user-data-dir=' + self.data_dir + ' --headless"' if self.headless else '"',
                       '--preset=' + self.preset]

            pbar.set_description(f"Running Lighthouse for {self.url}")
            subprocess.run(command, capture_output=True, text=True, check=True)

            if os.path.exists(self.output_path):
                result = self._read_report()
            else:
                pbar.set_description(f"Report file not found: {self.output_path}")
                result = self._generate_fallback_report("File not created")

        except subprocess.CalledProcessError as e:
            pbar.set_description(f"Failed to run Lighthouse for {self.url}: {e}")
            result = self._generate_fallback_report(f"CalledProcessError: {e}")

        pbar.set_description(f"Completed Lighthouse report for {self.url}")
        pbar.update(1)
        return result

    def _read_report(self) -> dict:
        try:
            with open(self.output_path, 'r') as report_file:
                return json.load(report_file)
        except FileNotFoundError:
            print(f"Lighthouse report file not found at {self.output_path}")
            return self._generate_fallback_report(f"FileNotFoundError: {self.output_path}")

    def _generate_fallback_report(self, error_message: str) -> dict:
        return {
            'url': self.url,
            'error': error_message,
            'output_path': self.output_path
        }
