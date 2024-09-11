from enum import Enum
from importlib.resources import files
from .utils import debug

class EnvType(Enum):
    DEV = "dev"
    ALPHA = "alpha"
    BETA = "beta"

class BuildEnvFile():
  """
  Plain text file that reflects which env this package was build for.
  This will drive the default values that can be overridden via config options.
  """
  value: EnvType = EnvType.DEV

  def __init__(self):
    self.value = self.get_type()

  def get_text(self):
    build_env_resource = files('positron_common').joinpath('build_env')
    try:
      return build_env_resource.read_text().strip()
    except Exception as e:
      debug(f'Error reading build_env file: {e}, defaulting to "{self.value.value}"')
      return self.value.value

  def get_type(self):
    try:
      return EnvType(self.get_text())
    except ValueError as e:
      print(f"There seems to be a problem with the build: {e}")
      print(f"Defaulting to {self.value.value}")
      return self.value

build_env: EnvType = BuildEnvFile().value
"""
The type of env this package was built for.
Used when selecting default values for the package.
"""
