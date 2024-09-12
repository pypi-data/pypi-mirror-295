#--------------------------------------------------------------------------------
# 참조 모듈 목록.
#--------------------------------------------------------------------------------
from __future__ import annotations
from typing import Any, Final, Callable, Iterator, Optional, Type, TypeVar, Union, Tuple, List, Dict, Set, cast
from dduk.core.builtins import Builtins
from enum import Enum
import logging


#--------------------------------------------------------------------------------
# 로그 종류.
#--------------------------------------------------------------------------------
class Level(Enum):
	NONE = logging.NOTSET
	DEBUG = logging.DEBUG
	INFO = logging.INFO
	WARNING = logging.WARNING
	ERROR = logging.ERROR
	EXCEPTION = logging.ERROR
	CRITICAL = logging.CRITICAL

	#--------------------------------------------------------------------------------
	# 로그 이름.
	#--------------------------------------------------------------------------------
	@staticmethod
	def GetLevelName(logLevel : Level) -> str:
		return logging.getLevelName(logLevel.value)