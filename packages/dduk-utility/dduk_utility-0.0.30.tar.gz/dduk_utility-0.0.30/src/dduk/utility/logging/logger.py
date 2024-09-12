#--------------------------------------------------------------------------------
# 참조 모듈 목록.
#--------------------------------------------------------------------------------
from __future__ import annotations
from typing import Any, Final, Callable, Iterator, Optional, Type, TypeVar, Union, Tuple, List, Dict, Set, cast
from dduk.core.builtins import Builtins
import logging
import os
from queue import Queue
from logging import Logger as InternalLogger
from logging import handlers, StreamHandler, FileHandler, Formatter
from logging.handlers import QueueHandler, QueueListener
from ..ansicode import ANSICODE
from ..strutility import GetTimestampString, GetSplitFilePath
from .level import Level


#--------------------------------------------------------------------------------
# 전역 상수 목록.
#--------------------------------------------------------------------------------
EMPTY : str = ""
NONE : str = "NONE"
COLON : str = ":"
SPACE : str = " "
SLASH : str = "/"
HYPHEN : str = "-"
COMMA : str = ","
UTF8 : str = "utf-8"


#--------------------------------------------------------------------------------
# 로거.
#--------------------------------------------------------------------------------
class Logger:
	#--------------------------------------------------------------------------------
	# 멤버 변수 목록.
	#--------------------------------------------------------------------------------
	__ansicode : ANSICODE
	__internalLogger : InternalLogger


	#--------------------------------------------------------------------------------
	# 내부 로거 반환.
	#--------------------------------------------------------------------------------
	@property
	def InternalLogger(self) -> InternalLogger:
		return self.__internalLogger


	#--------------------------------------------------------------------------------
	# 생성됨.
	#--------------------------------------------------------------------------------
	def __init__(self, loggerName : str, logFilePath : str, mininumLevel : Level) -> None:

		# 생성.
		self.__ansicode = ANSICODE()
		self.__internalLogger = logging.getLogger(loggerName)

		# 로그 수준 설정.
		self.__internalLogger.setLevel(mininumLevel.value)

		# 로깅 큐 추가.
		# 로그 파일 기록이 자꾸 씹히는 이슈 있어서 사용. (하지만 개선 효과 없음)
		logQueue = Queue()
		ququeHandler = QueueHandler(logQueue)
		self.__internalLogger.addHandler(ququeHandler)

		# 로그 출력 양식 설정.
		formatter : Formatter = Formatter("[%(asctime)s][%(levelname)s]%(message)s")

		# 로그파일 설정.
		logPath = os.path.dirname(logFilePath)
		if not os.path.isdir(logPath):
			os.makedirs(logPath)

		fileHandler : StreamHandler = FileHandler(logFilePath, encoding = UTF8)
		fileHandler.setLevel(mininumLevel.value)
		fileHandler.setFormatter(formatter)
		# self.__internalLogger.addHandler(fileHandler)

		# 큐 시작.
		queueListener = QueueListener(logQueue, fileHandler)
		queueListener.start()


	#--------------------------------------------------------------------------------
	# 로그 출력.
	#--------------------------------------------------------------------------------
	def LogToConsole(self, text : str, level : Level) -> None:
		if level.value == logging.FATAL or level.value == logging.CRITICAL: self.__ansicode.Print(f"<bg_red><white><b>{text}</b></white></bg_red>")
		elif level.value == logging.ERROR: self.__ansicode.Print(f"<red>{text}</red>")
		elif level.value == logging.WARN or level.value == logging.WARNING: self.__ansicode.Print(f"<yellow>{text}</yellow>")
		elif level.value == logging.INFO: self.__ansicode.Print(f"{text}")
		elif level.value == logging.DEBUG: self.__ansicode.Print(f"<magenta>{text}</magenta>")
		else: self.__ansicode.Print(text)


	#--------------------------------------------------------------------------------
	# 로그 출력.
	#--------------------------------------------------------------------------------
	def LogToFile(self, text : str, level : Level) -> None:
		if level == Level.DEBUG: # logging.DEBUG:
			self.__internalLogger.debug(text)
		elif level == Level.INFO: # logging.INFO:
			self.__internalLogger.info(text)
		elif level == Level.WARNING: # logging.WARN or logging.WARNING:
			self.__internalLogger.warning(text)
		elif level == Level.ERROR: # logging.ERROR:
			self.__internalLogger.error(text)
		elif level == Level.CRITICAL: # logging.FATAL or logging.CRITICAL:
			self.__internalLogger.critical(text)
