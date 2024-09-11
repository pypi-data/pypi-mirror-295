import os
import yaml
from pathlib import Path

class Config:
    def __init__(self):
        self.chrome_executable_path = None
        self.tmp_dir = None
        self.max_browser_instances = None
        self.config_path = self._get_config_path()
        self.load_config()

    @staticmethod
    def _get_config_path():
        home = Path.home()
        return os.path.join(home, '.tt.config.yml')

    def load_config(self):
        if not os.path.exists(self.config_path):
            self.create_default_config()

        with open(self.config_path, 'r') as config_file:
            config_data = yaml.safe_load(config_file)

        self.chrome_executable_path = config_data.get('chrome_executable_path', self._get_default_chrome_path())
        self.tmp_dir = config_data.get('tmp_dir', os.path.join(Path.home(), '.tt_tmp'))
        self.max_browser_instances = config_data.get('max_browser_instances', 5)

    @staticmethod
    def _get_default_chrome_path():
        if os.name == 'nt':
            return r'C:\Program Files\Google\Chrome\Application\chrome.exe'
        elif os.name == 'posix':
            if os.path.exists('/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'):
                return '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
            else:
                return '/usr/bin/google-chrome'
        else:
            return ''

    def create_default_config(self):
        default_config = {
            'chrome_executable_path': self._get_default_chrome_path(),
            'tmp_dir': os.path.join(os.getcwd(), '.tt_tmp'),
            'max_browser_instances': 5
        }

        with open(self.config_path, 'w') as config_file:
            yaml.dump(default_config, config_file)

    def save_config(self):
        config_data = {
            'chrome_executable_path': self.chrome_executable_path,
            'tmp_dir': self.tmp_dir,
            'max_browser_instances': self.max_browser_instances
        }

        with open(self.config_path, 'w') as config_file:
            yaml.dump(config_data, config_file)

config = Config()