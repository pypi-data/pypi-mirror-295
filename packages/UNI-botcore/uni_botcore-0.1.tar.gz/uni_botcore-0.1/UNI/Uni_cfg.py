import asyncio
import aiohttp
from argparse import Namespace
import traceback
import json
from decimal import Decimal
import inspect
import time
from typing import List, Optional
import types
from os.path import basename, splitext
import functools
from functools import wraps
import textwrap
from random import randint
import httpx
from urllib.parse import urlparse
from typing import Optional, Callable, Dict, Any, List, Set

# from methods import texts, keyboards

# from Data_ import Packs as Custom_Packs

UNI_Handlers = {}
pre_UNI_Handlers = {}

Bot_Object = None

texts, keyboards = None, None
Custom_Packs = None

v_ = '0.6'