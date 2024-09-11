"""Package 'fedinesia' level definitions."""

from datetime import timedelta
from datetime import timezone
from importlib.metadata import version
from typing import Final

__version__: Final[str] = version(__package__)

__package_name__: Final[str] = __package__
__display_name__: Final[str] = __package__.title()
USER_AGENT: Final[str] = f"{__display_name__}"

CLIENT_WEBSITE: Final[str] = "https://codeberg.org/MarvinsMastodonTools/fedinesia"

UTC = timezone(offset=timedelta(hours=0))
PROGRESS_ID_KEY = "last_deleted_id"
