import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()


######################
# cache configurations
######################

CACHE_DIR = Path.home() / ".bonsait"

######################
# model configuration
######################

DEFAULT_MODEL = "all-mpnet-base-v2"

######################
# base dimension table configuration
######################

BONSAI_ACTIVITY_API = "https://lca.aau.dk/api/activity-names"
BONSAI_API_KEY = os.environ.get("BONSAI_API_KEY")
