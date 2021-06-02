import os
import sys
import logging
from typing import List, Set, Dict, Tuple, Optional

from dotenv import load_dotenv
load_dotenv()

token: str = os.environ.get('BOT_TOKEN', None)

prefixes: List[str] = [ 'thread ', 'threads ', 'tr ' ]

logging.basicConfig(stream=sys.stdout,
                    level=logging.INFO,
                    format='%(levelname)-8s %(message)s',
                    datefmt='%d/%m/%Y %H:%M:%S'
                    )
log = logging.getLogger(__name__)
