from pathlib import Path
from split_settings.tools import include, optional


BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent

LOCAL_SETTINGS_PATH = str(BASE_DIR / "local/settings.dev.py")

include(
    'base.py',
    optional(LOCAL_SETTINGS_PATH),
    'rest_framework.py'
)
