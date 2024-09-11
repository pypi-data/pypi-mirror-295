import yaml
from typing import Optional
from pydantic import BaseModel
import configparser
import os
from .utils import debug

DEFAULT_USER_CONFIG_PATH = os.path.expanduser('~/.positron/config.yaml')

class UserConfigFile(BaseModel):
    """
    The user configuration file for the Positron CLI.
    """
    user_auth_token: Optional[str] = None
    backend_api_base_url: Optional[str] = None
    backend_ws_base_url: Optional[str] = None

    def migrate(self):
        """
        Migrate an existing .ini file to .yaml, once.
        Leave old file in place so that switching to old and new versions works.
        """
        old_config_path = os.path.expanduser('~/.positron/config.ini')
        new_config_path = DEFAULT_USER_CONFIG_PATH
        if os.path.exists(new_config_path):
            # We've already migrated.
            return

        debug('config migration from ini to yaml required')
        old_config = configparser.ConfigParser()
        old_config.read(old_config_path)    
        if not old_config['DEFAULT']:
            debug('old config file is empty, nothing to migrate')
            self.write()
            return
        
        # write out new config from old
        new_config = UserConfigFile(
            user_auth_token=old_config['DEFAULT'].get('userauthtoken'),
            backend_api_base_url=old_config['DEFAULT'].get('POSITRON_API_BASE_URL'),
            backend_ws_base_url=old_config['DEFAULT'].get('POSITRON_WS_BASE_URL')
        )
        debug(f'previous configs: {new_config}')
        new_config.write()
        debug('Done migrating to new yaml config file!')

    
    def load_config(self):
        """
        Loads the user configuration from the user's home directory.
        """
        if not os.path.exists(DEFAULT_USER_CONFIG_PATH):
            debug(f'user config file not found: `{DEFAULT_USER_CONFIG_PATH}`')
            print('Could not find a user config file, please run `positron login` to set up your configuration.')
            return

        try:
            with open(DEFAULT_USER_CONFIG_PATH, 'r') as job_config_file:
                job_config_dict = yaml.safe_load(job_config_file)
                self.__init__(**job_config_dict)
        except Exception as e:
            print(f'Error loading job configuration! {str(e)}')
            print(f'Ignoring user config file: `{DEFAULT_USER_CONFIG_PATH}`')
    
    def write(self):
        """
        Write the user configuration to the user's home directory.
        """
        data = self.model_dump(exclude_none=True)
        os.makedirs(os.path.dirname(DEFAULT_USER_CONFIG_PATH), exist_ok=True)
        with open(DEFAULT_USER_CONFIG_PATH, 'w') as user_config_file:
            yaml.dump(data, user_config_file)

user_config = UserConfigFile()
"""
The user configuration file for the Positron CLI.
"""

if os.getenv('POSITRON_CLOUD_ENVIRONMENT', False):
    debug("Cloud environment detected, skipping config file load.")
else:
    debug('loading user config')
    user_config.migrate()
    user_config.load_config()
