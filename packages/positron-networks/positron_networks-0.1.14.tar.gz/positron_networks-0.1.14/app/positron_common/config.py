from pydantic import BaseModel, field_validator
from typing import Dict, Optional
from typing_extensions import Self
import os
import yaml
import re
from .utils import PositronException

class PositronJob(BaseModel):
    """
    The Job details as defined in the `python_job` from the `job_config.yaml` file.
    """
    funding_group_id: Optional[str] = None
    environment_id: Optional[str] = None
    image: Optional[str] = None
    commands: Optional[str] = None
    entry_point: Optional[str] = None
    workspace_dir: Optional[str] = None
    max_tokens: Optional[str] = None
    max_time: Optional[str] = None
    env: Optional[Dict[str, str]] = None

    @field_validator('commands', mode='after')
    def ensure_non_empty(cls, commands):
        return commands if len(commands) else None

    @field_validator('env', mode='after')
    def ensure_env_is_dict(cls, v):
        if isinstance(v, dict):
            return v
        raise ValueError('env must be a dictionary')

    def validate(self) -> Self:
        errors = []
        if not self.funding_group_id:
            errors.append('funding_group is required')
        if not self.commands and not self.entry_point:
            errors.append('At least one of commands or entry_point must be provided')
        if self.env and not validate_env_vars(self.env):
            errors.append('At least one of the environment variables provided is invalid')
        if errors:
            raise PositronException(f'Invalid configuration. Errors: {errors}')

        return self

class PositronJobConfig(BaseModel):
    """
    The `job_config.yaml` schema class.
    """
    version: float
    python_job: PositronJob


def has_valid_prefix(key):
    """
    Check if the key starts with the required prefix.
    """
    return key.startswith("POSITRON_ENV_")

def is_valid_key_value(keyvalue):
    """
    Validate that the key-value contains only alphanumeric characters, dashes, and underscores, and has no spaces.
    """
    return bool(re.match(r'^[\w-]+$', keyvalue))

def validate_env_vars(env_dict):
    """
    Validate the environment variables from the given dictionary.
    """
    valid = True
    for key, value in env_dict.items():
        if not has_valid_prefix(key):
            print(f"Invalid key (missing prefix): {key}")
            valid = False
        if not is_valid_key_value(key):
            print(f"Invalid key (contains invalid characters or spaces): {key}")
            valid = False
        if not is_valid_key_value(value):
            print(f"Invalid value (contains invalid characters or spaces): {value}")
            valid = False
    return valid

def merge_config(base_config: PositronJob, override_config: PositronJob) -> PositronJob:
    """
    Makes it easy to merge decorator configs on top of the YAML config.
    """
    update_data = override_config.dict(exclude_unset=True)
    updated_config = base_config.copy(update=update_data)
    return updated_config

def get_job_config(config_path: str = 'job_config.yaml') -> Optional[PositronJob]:
    """
    Load the job configuration from the `job_config.yaml` file if it exists
    """
    if not os.path.exists(config_path):
        print('job_config.yaml file not found')
        return None

    try:
        with open(config_path, 'r') as job_config_file:
            job_config_dict = yaml.safe_load(job_config_file)
            job_config = PositronJobConfig(**job_config_dict)
            return job_config.python_job
    except Exception as e:
        print(f'Error loading job configuration! {str(e)}')

def parse_job_config(config_file):
    job_config_yaml = get_job_config(config_file)
    commands = getattr(job_config_yaml, 'commands', None)
    env_vars = getattr(job_config_yaml, 'env', None)
    # Determine if job is decorator job or generic
    return (commands is not None and len(commands) > 0), commands, env_vars