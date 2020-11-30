import os
import logging
from datetime import datetime


cur_dir = os.getcwd()
timestamp = datetime.now()

if not os.path.exists(f"{cur_dir}/logs"):
    os.makedirs(f"{cur_dir}/logs")

# Create a logging instance
logger = logging.getLogger("get_in_my_cart")
logger.setLevel(logging.INFO) # set as DEBUG, INFO, ERROR

# Assigning a file-handler to that instance
fh = logging.FileHandler(f"{cur_dir}/logs/logs.txt")
fh.setLevel(logging.INFO)

# Format log (optional)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)

# Add the handler to logging instance
logger.addHandler(fh)
