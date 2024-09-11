import sys

def debug(log):
    if sys.argv.__contains__('--debug'):
        print(f'DEBUG: {log}')

class PositronException(Exception):
    "Raised when decorator related errors are happening"
    pass

# Sentinel object for undefined
undefined = object()
