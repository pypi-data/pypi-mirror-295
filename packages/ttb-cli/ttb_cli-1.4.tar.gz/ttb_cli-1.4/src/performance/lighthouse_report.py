import subprocess
import json
import os

from tqdm import tqdm
from src.utils import get_current_time_ms, create_tmp_dir_, config


class LighthouseReport:
    def __init__(self, url: str, temp_dir, output_path: str = 'lighthouse_report.json', headless: bool = False,
                 preset: str = 'desktop', extra_headers: dict[str, str] | None = None, cookies: list[dict] | None = None):
        self.url = url
        self.output_path = output_path
        self.headless = headless
        self.preset = preset
        self.extra_headers = extra_headers or {}
        self.cookies = cookies or []

        if self.cookies:
            cookie_header = "; ".join([f"{cookie['name']}={cookie['value']}" for cookie in self.cookies if 'name' in cookie and 'value' in cookie])
            self.extra_headers['Cookie'] = cookie_header

        self.temp_dir = temp_dir
        create_tmp_dir_(temp_dir)
        self.data_dir = os.path.join(self.temp_dir, 'chrome_data_dir_' + str(get_current_time_ms()))
        self.chrome_executable_path = config.chrome_executable_path

    async def run_report(self, pbar: tqdm) -> dict:
        start_time = get_current_time_ms()
        try:

            command = [
                'lighthouse', self.url, '--output', 'json', '--output-path', self.output_path, '--quiet',
                f'--chrome-flags="--enable-logging --v=99 --log-path={self.data_dir}/logs --user-data-dir={self.data_dir}{" --headless" if self.headless else ""}"',
                "--form-factor=mobile" if self.preset == 'mobile' else "--preset=desktop",
                f'--chrome-path={self.chrome_executable_path}'
            ]

            if self.extra_headers:
                headers_json = json.dumps(self.extra_headers)
                command.extend(['--extra-headers', headers_json])

            pbar.set_description(f"Running Lighthouse for {self.url}")
            subprocess.run(command, capture_output=True, text=True, check=True)

            if os.path.exists(self.output_path):
                result = self._read_report()
            else:
                pbar.set_description(f"Report file not found: {self.output_path}")
                result = self._generate_fallback_report("File not created")

        except Exception as err:
            error = f"Error: {str(err)}"
            pbar.set_description(f"Error running Lighthouse for {self.url}: {err}")
            result = self._generate_fallback_report(error)

        result['total_time'] = self._calculate_total_time(start_time)
        pbar.set_description(f"Completed Lighthouse report for {self.url}")
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

    @staticmethod
    def _calculate_total_time(start_time: float) -> float:
        return get_current_time_ms() - start_time