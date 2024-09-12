import csv
import os
from datetime import datetime
from typing import List, Dict


def write_performance_metrics_to_csv(metrics: List[Dict], output_file_path: str):
    if not metrics:
        return

    fieldnames = ['url', 'iteration', 'test_time', 'ttfb', 'load_time', 'total_time', 'error']

    try:
        if os.path.exists(output_file_path):
            output_file_path = f"{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}_{output_file_path}"

        with open(output_file_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)

            writer.writeheader()

            for metric in metrics:
                writer.writerow(metric)

    except Exception as e:
        print(f"Failed to write metrics to CSV: {e}")


def write_lighthouse_reports_to_csv(reports: List[Dict], output_file_path: str):
    if not reports:
        return

    fieldnames = ['url', 'finalUrl', 'requestedUrl', 'performance', 'accessibility', 'best-practices', 'seo', 'pwa', 'error']

    try:
        if os.path.exists(output_file_path):
            output_file_path = f"{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}_{output_file_path}"

        with open(output_file_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)

            writer.writeheader()

            for report in reports:
                writer.writerow({
                    'url': report.get('finalUrl', 'N/A'),
                    'finalUrl': report.get('finalUrl', 'N/A'),
                    'requestedUrl': report.get('requestedUrl', 'N/A'),
                    'performance': report.get('categories', {}).get('performance', {}).get('score', 'N/A'),
                    'accessibility': report.get('categories', {}).get('accessibility', {}).get('score', 'N/A'),
                    'best-practices': report.get('categories', {}).get('best-practices', {}).get('score', 'N/A'),
                    'seo': report.get('categories', {}).get('seo', {}).get('score', 'N/A'),
                    'pwa': report.get('categories', {}).get('pwa', {}).get('score', 'N/A'),
                    'error': report.get('error', 'N/A')
                })

    except Exception as e:
        print(f"Failed to write Lighthouse reports to CSV: {e}")

