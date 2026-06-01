import sys
from contextlib import contextmanager

from botocore.exceptions import BotoCoreError, ClientError


class AwsFusionException(Exception):
    """Base class for all aws-fusion errors surfaced to the user."""
    pass


@contextmanager
def handle_cli_errors(debug=False):
    """Convert known exceptions into a clean `sys.exit`. Re-raises when debug is on so tracebacks survive."""
    try:
        yield
    except KeyboardInterrupt:
        sys.exit(130)
    except (AwsFusionException, ClientError, BotoCoreError) as e:
        if debug:
            raise
        sys.exit(str(e))
