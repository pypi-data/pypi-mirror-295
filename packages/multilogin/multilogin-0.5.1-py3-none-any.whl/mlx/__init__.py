import warnings

# Optionally disable all warnings, just to be sure
warnings.filterwarnings("ignore",module="requests")


import os

from .models import Profile

from .api.profile import ProfileApi

os.environ["PAGER"] = "cat"


__all__ = ["Profile", "ProfileApi"]
