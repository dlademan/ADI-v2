import os
import wx

from pathlib import Path
from platform import system
from configobj import ConfigObj


class ConfigHandler:

    def __init__(self, debug=False):
        user_folder_path: Path = self.get_user_folder()

        self.config_path = user_folder_path / 'debug.ini' if debug else user_folder_path / 'config.ini'

        self.dimensions_path: Path = user_folder_path / 'dimensions.pkl'
        self.backup_path: Path = user_folder_path / 'backup'

        if not self.config_path.exists(): self._create_config()

        self._config = ConfigObj(str(self.config_path))

        self.archive: Path = Path(self._config['Options']['archive'])
        self.library: Path = Path(self._config['Options']['library'])
        self.clear_queue: bool = bool(self._config['Options']['clear_queue'])
        self.expand: bool = bool(self._config['Options']['expand'])
        self.close_dialog: bool = bool(self._config['Options']['close_dialog'])
        self.detect: bool = bool(self._config['Options']['detect'])

        self.win_size = tuple(self._config['Dimensions']['win_size'])
        self.win_pos = tuple(self._config['Dimensions']['win_pos'])
        self.first = bool(self._config['Dimensions']['first'])
        self.version = self._config['Dimensions']['version']

    def _create_config(self):
        self._config = ConfigObj()
        self._config.filename = self.config_path

        self._config['Options'] = {}
        self._config['Options']['archive'] = self.get_default_archive_path()
        self._config['Options']['library'] = self.get_default_library_path()
        self._config['Options']['clear_queue'] = True
        self._config['Options']['expand'] = True
        self._config['Options']['close_dialog'] = False
        self._config['Options']['detect'] = False

        self._config['Dimensions'] = {}
        self._config['Dimensions']['win_size'] = (1300, 800)
        self._config['Dimensions']['win_pos'] = wx.DefaultPosition.Get()
        self._config['Dimensions']['first'] = True
        self._config['Dimensions']['version'] = 'temp'

        self._config.write()

    def _save_config(self):
        self._config['Options'] = {}
        self._config['Options']['archive'] = self.get_default_archive_path()
        self._config['Options']['library'] = self.get_default_library_path()
        self._config['Options']['clear_queue'] = True
        self._config['Options']['expand'] = True
        self._config['Options']['close_dialog'] = False
        self._config['Options']['detect'] = False

        self._config['Dimensions'] = {}
        self._config['Dimensions']['win_size'] = (1300, 800)
        self._config['Dimensions']['win_pos'] = wx.DefaultPosition.Get()
        self._config['Dimensions']['first'] = True
        self._config['Dimensions']['version'] = 'temp'

        self._config.write()

    #todo make these better?
    @staticmethod
    def get_user_folder():
        if system() == 'Windows':
            return Path(os.getenv('APPDATA') + '/ADI/')
        elif system() == 'Darwin':  # mac
            return Path(os.path.expanduser('~/Library/Application Support/ADI/'))
        else:  # linux
            return Path(os.path.expanduser('~/.ADI/'))

    @staticmethod
    def get_default_library_path():
        if system() == 'Windows':
            return Path('C:/Users/Public/Documents/My DAZ 3D Library/')
        elif system() == 'Darwin':  # mac
            return Path(os.path.expanduser('~/Studio3D/DazStudio/Content/'))
        else:  # linux
            return Path(os.path.expanduser('~/Daz3D Library/'))

    @staticmethod
    def get_default_archive_path():
        if system() == 'Windows':
            return Path('C:/Users/Public/Documents/DAZ 3D/InstallManager/Downloads')
        elif system() == 'Darwin':  # mac
            return Path(os.path.expanduser('~/Studio3D/DazStudio/InstallManager/Download/'))
        else:  # linux
            return Path(os.path.expanduser('~/Daz3D Zips/'))
