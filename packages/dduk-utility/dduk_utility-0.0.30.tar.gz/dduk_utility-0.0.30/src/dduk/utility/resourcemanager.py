#--------------------------------------------------------------------------------
# 참조 모듈 목록.
#--------------------------------------------------------------------------------
from __future__ import annotations
from typing import Any, Final, Callable, Iterator, Optional, Type, TypeVar, Union, Tuple, List, Dict, Set, cast
from importlib.abc import Traversable # python3.7+
import importlib.resources as Resources # python3.7+
import os
from logging import Logger, handlers, Handler, StreamHandler, FileHandler, Formatter, LogRecord
# import pkg_resources # setuptools 의 종속성 존재.
from dduk.core.builtins import Builtins


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
STRICT : str = "strict"


#--------------------------------------------------------------------------------
# 패키지 리소스 매니저.
#--------------------------------------------------------------------------------
class ResourceManager:
	#--------------------------------------------------------------------------------
	# 멤버 변수 목록.
	#--------------------------------------------------------------------------------
	__packageName : str


	#--------------------------------------------------------------------------------
	# 패키지 설정.
	#--------------------------------------------------------------------------------
	@staticmethod
	def SetPackageName(packageName):
		ResourceManager.__packageName = packageName


	#--------------------------------------------------------------------------------
	# 리소스 존재 여부.
	# - 디렉토리 체크는 불가능.
	#--------------------------------------------------------------------------------
	@staticmethod
	def Exists(resourceFilePath : str) -> bool:
		try:
			isExists = Resources.is_resource(ResourceManager.__packageName, resourceFilePath)
			return isExists
		
		except Exception as exception:
			return False


	#--------------------------------------------------------------------------------
	# 불러오기.
	#--------------------------------------------------------------------------------
	@staticmethod
	def LoadBytes(resourceFilePath : str) -> bytes:
		try:
			data : bytes = Resources.read_binary(ResourceManager.__packageName, resourceFilePath, encoding = UTF8, errors = STRICT)
			return data			
		except Exception as exception:
			return bytes() # 0 bytes.
		

	#--------------------------------------------------------------------------------
	# 불러오기.
	#--------------------------------------------------------------------------------
	@staticmethod
	def LoadStr(resourceFilePath : str) -> str:
		try:
			text = Resources.read_text(ResourceManager.__packageName, resourceFilePath, encoding = UTF8, errors = STRICT)
			return text			
		except Exception as exception:
			return EMPTY
