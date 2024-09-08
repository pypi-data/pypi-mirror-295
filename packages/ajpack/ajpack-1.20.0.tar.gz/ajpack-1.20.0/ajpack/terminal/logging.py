import datetime
import logging
import json
from ..settings import settings
from logging.handlers import RotatingFileHandler
from concurrent.futures import ThreadPoolExecutor

class Logger:
    """
    More advanced logging system.

    Use with 'logger = ajpack.Logger()'
    """
    def __init__(self):
        self.format = "[ {level} ] {timestamp} --> {message}"
        self.log_file = None # Start with no log file
        self.colored_log = True
        self.async_logging = False
        self.custom_levels = {}
        self.context = {}
        self.filters = set()
        self.rate_limits = {}
        self.structured_format = None
        self.executor = ThreadPoolExecutor(max_workers=1) if self.async_logging else None

        self._init_rate_limits()

    def _init_rate_limits(self):
        self.rate_limit_counters = {}

    def _rate_limited(self, level: str):
        if level not in self.rate_limits:
            return False

        max_messages, interval = self.rate_limits[level]
        current_time = datetime.datetime.now().timestamp()

        if level not in self.rate_limit_counters:
            self.rate_limit_counters[level] = []

        # Remove outdated timestamps
        self.rate_limit_counters[level] = [ts for ts in self.rate_limit_counters[level] if current_time - ts < interval]

        if len(self.rate_limit_counters[level]) < max_messages:
            self.rate_limit_counters[level].append(current_time)
            return False
        
        return True

    def set_format(self, format_str: str):
        self.format = format_str

    def log_to_file(self, file_path: str|None=None):
        self.log_file = file_path
        self._init_log_file() if file_path else logging.getLogger().handlers.clear()

    def _init_log_file(self):
        if self.log_file:
            handler = RotatingFileHandler(self.log_file, maxBytes=5*1024*1024, backupCount=3)
            logging.basicConfig(level=logging.DEBUG, handlers=[handler])
        else:
            logging.getLogger().handlers.clear()

    def enable_colored_output(self):
        self.colored_log = True

    def disable_colored_output(self):
        self.colored_log = False

    def enable_async_logging(self):
        self.async_logging = True
        self.executor = ThreadPoolExecutor(max_workers=1)

    def disable_async_logging(self):
        self.async_logging = False
        if self.executor:
            self.executor.shutdown(wait=False)
            self.executor = None

    def add_custom_level(self, level_name: str):
        self.custom_levels[level_name.upper()] = logging.DEBUG + len(self.custom_levels) + 1

    def add_context(self, **context):
        self.context.update(context)

    def set_filter(self, level: str):
        self.filters.add(level.upper())

    def enable_structured_logging(self, format: str='json'):
        self.structured_format = format

    def set_rate_limit(self, level: str, max_messages: int, interval: int):
        self.rate_limits[level.upper()] = (max_messages, interval)

    def log(self, level: str, message: str, **kwargs):
        """
        Logs the level and the message.

        :param level: Levels: success, warning, error, debug, info
        :param message: The message to be logged.
        """
        level = level.upper()

        if level in self.filters: return
        if self._rate_limited(level): return

        timestamp = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
        context = ' '.join([f"{key}={value}" for key, value in self.context.items()])
        formatted_message = self.format.format(level=level, timestamp=timestamp, message=message, **kwargs)

        if context: formatted_message += f" | {context}"
        if self.colored_log: formatted_message = self._color_message(level, formatted_message)

        if self.structured_format == 'json':
            formatted_message = json.dumps({
                "level": level,
                "timestamp": timestamp,
                "message": message,
                **self.context
            })

        if self.async_logging and self.executor:
            self.executor.submit(self._write_log, level, formatted_message)
        else:
            self._write_log(level, formatted_message)

    def _color_message(self, level: str, message: str):
        colors = {
            "SUCCESS": settings.GREEN,   # Green
            "WARNING": settings.YELLOW,   # Yellow
            "ERROR": settings.RED,     # Red
            "DEBUG": settings.BLUE,     # Blue
            "INFO": settings.CYAN,      # Cyan
            "ENDC": settings.RESET,        # Reset color (white)
        }
        color = colors.get(level, colors["ENDC"])
        return f"{color}{message}{colors['ENDC']}"

    def _write_log(self, level: str, message: str):
        logging.log(self.custom_levels.get(level, getattr(logging, level, logging.INFO)), message)

    def __del__(self):
        if self.executor:
            self.executor.shutdown(wait=False)
