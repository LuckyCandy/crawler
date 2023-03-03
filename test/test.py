from common.settings import LOG_PATH
from utils.logger import get_logger

logger = get_logger()
logger.error("Hello %s", "Damon")
