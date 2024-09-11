from pydantic import BaseModel
from typing import List, Optional

class PositronCLIArgs(BaseModel):
    """
    Positron CLI command line arguments.
    """
    is_init: bool = False
    local: bool = False
    deploy: bool = False
    stream_stdout: bool = False
    debug: bool = False
    job_args: Optional[List[str]] = None

    def init(self,
        local: bool = False,
        deploy: bool = False,
        stream_stdout: bool = False,
        debug: bool = False,
        job_args: Optional[List[str]] = None
    ):
        if self.is_init:
            raise ValueError('CLI Args already initialized')
        
        self.local = local
        self.deploy = deploy
        self.stream_stdout = stream_stdout
        self.debug = debug
        self.job_args = job_args
        self.is_init = True

#
# Export global (singleton)
#
args = PositronCLIArgs()
"""
Global CLI arguments singleton, make sure you call init() before using it.
"""
