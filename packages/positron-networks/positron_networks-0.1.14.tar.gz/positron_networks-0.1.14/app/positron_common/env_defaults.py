from typing import Dict
from dataclasses import dataclass
from .build_env import build_env, EnvType
from .utils import debug

@dataclass
class EnvDefaults():
  api_base: str
  ws_base: str
  auth0_domain: str
  auth0_audience: str
  auth0_client_id: str

env_config: Dict[EnvType, EnvDefaults] = {
  EnvType.DEV: EnvDefaults(
    api_base='https://dev.positronsupercompute.com/backend/api',
    ws_base='wss://dev.positronsupercompute.com',
    auth0_domain='dev-k1t01pbanrr04itm.us.auth0.com',
    auth0_client_id='Mr3GW8Ub4e2bLaEvZ5o0XK5pGfEhtH3d',
    auth0_audience='https://localhost/positron/api',
  ),
  EnvType.ALPHA: EnvDefaults(
    api_base='https://alpha.positronsupercompute.com/backend/api',
    ws_base='wss://alpha.positronsupercompute.com',
    auth0_domain='dev-k1t01pbanrr04itm.us.auth0.com',
    auth0_client_id='Mr3GW8Ub4e2bLaEvZ5o0XK5pGfEhtH3d',
    auth0_audience='https://localhost/positron/api',
  ),
  EnvType.BETA: EnvDefaults(
    api_base='https://beta.positronsupercompute.com/backend/api',
    ws_base='wss://beta.positronsupercompute.com',
    auth0_domain='positron-beta.us.auth0.com',
    auth0_client_id='ZW0vio95rYfbHrN7kE3PoUXwmPloBw7e',
    auth0_audience='https://beta/positron/api',
  ),
}

current = env_config[EnvType.DEV]

# Set current based on build
if build_env:
  current = env_config[build_env]
  debug(f'Using build environment: "{build_env.value}" backend url: "{current.api_base}"')
