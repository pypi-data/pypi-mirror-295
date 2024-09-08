import os
import importlib
import subprocess
import sys
import logging

def pip_install(package,no_deps=False):
  if no_deps:
    subprocess.check_call([sys.executable, "-m", "pip", "install", package,"--no-deps"])
  else:
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

def setup_install():

  facenet_check=importlib.util.find_spec("facenet_pytorch")

  if facenet_check is None:
    logging.info("LDT - Installing facenet_pytorch --no-deps")
    pip_install("facenet_pytorch",no_deps=True)

  req_lst=['imagehash','numpy','opencv-python','pandas','selenium','tqdm','webdriver-manager']

  for req in req_lst:
    spec=importlib.util.find_spec(req)
    if spec is None:
      logging.info(f"LDT - Installing {req}")
      pip_install(req)
try:
  setup_install()
except Exception as e:
  logging.error(f'Failed to install necessary packages for charloratools: {str(e)}')

from . import errors
from . import FilterAI
from . import Scrapers
from . import SysFileManager
from . import utils
