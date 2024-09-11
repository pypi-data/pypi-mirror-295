from typing import Optional, List
from pydantic import BaseModel, Field
from ..utils import undefined
from ..config import PositronJob
from ..cli_args import args as cli_args

class CreateJobBody(BaseModel):
    """
    Maps to the request body of the Create Job API
    """
    fundingGroupId: str
    imageName: Optional[str] = Field(default=undefined)
    environmentId: Optional[str] = Field(default=undefined)
    jobArguments: List[str] = Field(default=undefined)
    entryPoint: Optional[str] = Field(default=undefined)
    commands: Optional[str] = Field(default=undefined)
    maxTokens: Optional[int] = Field(default=undefined)
    maxMinutes: Optional[int] = Field(default=undefined)

    def json(self):
        """
        Enables dropping fields that were never set and should be treated as undefined
        """
        return {k: v for k, v in self.__dict__.items() if v is not undefined}

    @staticmethod
    def from_config(job_config: PositronJob):
      instance = CreateJobBody(
          fundingGroupId=job_config.funding_group_id,
          maxTokens=job_config.max_tokens,
          maxMinutes=job_config.max_time,
      )
      # determine if this is a generic or python job.
      if job_config.commands:
          instance.commands = job_config.commands
      elif job_config.entry_point:
          instance.entryPoint = job_config.entry_point
          instance.jobArguments = cli_args.job_args
      if job_config.image:
          instance.imageName = job_config.image
      if job_config.environment_id:
          instance.environmentId = job_config.environment_id
      return instance

