from .api.case import TestCase as TC
from .running.runner import main
from .running.conf import App
from .utils.config import kconfig
from .utils.pytest_util import *
from .utils.allure_util import *
from .utils.log import logger

__version__ = "0.1.31"
__description__ = "API/安卓/IOS/WEB平台自动化测试框架"
