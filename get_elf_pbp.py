import glob
import os
import time
from datetime import datetime

import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

from elf_utils import parse_names

def get_raw_elf_pbp_data(season:int,save=False):
    print('')