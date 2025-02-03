import os

import chess.engine
from dotenv import load_dotenv

load_dotenv()

SLEEP_TIME = 0.1
STOCKFISH_ENGINE = os.environ["STOCKFISH"]
USB_PORT = "/dev/ttyUSB0"
BAUD_RATE = 115200
SEEN_EXACTLY_N_TIMES = 2


LIMIT = chess.engine.Limit(time=0.05, depth=2)
