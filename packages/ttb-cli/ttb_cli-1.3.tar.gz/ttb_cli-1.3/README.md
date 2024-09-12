# TToolbox CLI
[![Release](https://github.com/medicm/ttb/actions/workflows/release.yml/badge.svg?event=release)](https://github.com/medicm/ttb/actions/workflows/release.yml)

This is a CLI tool for managing scripts and other tools for performance metrics and other automated tasks.

## Installation
Please note that the minimum required Python version is `3.12`. Before proceeding make sure you are running Python `3.12` or higher by running the following command: `python --version`

To install the CLI tool run the following command:
```bash
pip install ttb-cli
```

### Upgrading

To upgrade to the latest version, run the following command:

```bash
pip install ttb-cli --upgrade
```

## Usage

### Config file

Create a `.tt.config.yml` file in your home directory with the following structure:
```yaml
chrome_executable_path: /Applications/Google Chrome.app/Contents/MacOS/Google Chrome
max_browser_instances: 5
tmp_dir: /Users/marko/.tmp
```

Running commands:
```bash
ttb <command> <arguments>
```

Aliases:
- `ttb`
- `tammtoolbox`

## Commands

### `performance`

Run performance metrics for given URLs.

```bash
ttb performance <arguments>
```

Arguments:
- `--url`: List of URLs to test (required, can be specified multiple times)
- `--output`: Output file for performance metrics (required)
- `--iterations`: Number of iterations per URL (default: 10)
- `--headless`: Run headless browser (optional flag)
- `--concurrent`: Run tests concurrently (optional flag)
- `--headers_file`: File containing headers to be used in the request in YAML format (optional) (examples and explanation in the [Cookies and Headers Files](#cookies-and-headers-files) section below)
- `--cookies_file`: File containing cookies to be used in the request in YAML format (optional) (examples and explanation in the [Cookies and Headers Files](#cookies-and-headers-files) section below)

Example:
```bash
ttb performance --url https://tamm.abudhabi --url https://doh.gov.ae --iterations 5 --output metrics_report.csv --headless --concurrent
```

### `lighthouse`
Prerequisites: `npm install -g lighthouse`

Run Lighthouse report for given URLs.

```bash
ttb lighthouse <arguments>
```

Arguments:
- `--url`: List of URLs to test (required, can be specified multiple times)
- `--output`: Output file for Lighthouse report (required)
- `--headless`: Run headless browser (optional flag)
- `--concurrent`: Run tests concurrently (optional flag)
- `--preset`: Lighthouse preset (desktop or mobile, default: desktop)
- `--headers_file`: File containing headers to be used in the request in YAML format (optional) (examples and explanation in the [Cookies and Headers Files](#cookies-and-headers-files) section below)
- `--cookies_file`: File containing cookies to be used in the request in YAML format (optional) (examples and explanation in the [Cookies and Headers Files](#cookies-and-headers-files) section below)

Example:
```bash
ttb lighthouse --url https://tamm.abudhabi --url https://www.tamm.abudhabi/en/contact --output lighthouse_report.csv --headless --concurrent --preset mobile
```

These commands allow you to run performance metrics and Lighthouse reports on specified URLs, with options for headless browsing, concurrent execution, and customizable settings.

### Cookies and Headers Files

You can use the `--headers_file` and `--cookies_file` arguments to specify files containing headers and cookies to be
used in the request. These files should be in YAML format.

Example headers file:

```yaml
- name: X-My-Header
  value: my-header-value
- name: X-Another-Header
  value: another-header-value
```

Example cookies file:

```yaml
- name: my-cookie
  value: my-cookie-value
- name: another-cookie
  value: another-cookie-value
```