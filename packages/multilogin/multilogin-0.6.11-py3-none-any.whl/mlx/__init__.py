import warnings

import fire

# Optionally disable all warnings, just to be sure
warnings.filterwarnings("ignore", module="requests")


import os

from .api.profile import ProfileApi
from .models import Profile

os.environ["PAGER"] = "cat"


__all__ = ["Profile", "ProfileApi"]
