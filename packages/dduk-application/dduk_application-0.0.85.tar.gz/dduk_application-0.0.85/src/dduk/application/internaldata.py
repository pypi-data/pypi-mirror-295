#--------------------------------------------------------------------------------
# 참조 모듈 목록.
#--------------------------------------------------------------------------------
from __future__ import annotations
from typing import Any, Final, Callable, Iterator, Optional, Type, TypeVar, Union, Tuple, List, Dict, Set, cast
from dduk.core.builtins import Builtins
import os
import re
from dduk.utility import strutility


#--------------------------------------------------------------------------------
# 전역 상수 목록.
#--------------------------------------------------------------------------------
EMPTY : str = ""
NONE : str = "NONE"
COMMA : str = ","
SLASH : str = "/"
BACKSLASH : str = "\\"
COLON : str = ":"
SPACE : str = " "
DEBUG : str = "DEBUG"
# SYMBOL_NAMING_PATTERN : str = "^[A-Z_][A-Z0-9_]*$"


#--------------------------------------------------------------------------------
# 내부 애플리케이션 데이터 클래스.
#--------------------------------------------------------------------------------
class InternalData:
	#--------------------------------------------------------------------------------
	# 멤버 변수 목록.
	#--------------------------------------------------------------------------------
	__isBinary : bool
	__isDebugging : bool
	__executeFileName : str
	__rootPath : str
	__metaPath : str
	__sourcePath : str
	__resourcePath : str
	__workingspacePath : str
	__applicationDataPath : str
	__symbols : set[str]


	#--------------------------------------------------------------------------------
	# 생성됨.
	#--------------------------------------------------------------------------------
	def __init__(self) -> None:
		self.__isBinary = False
		self.__isDebugging = False
		self.__executeFileName = str()
		self.__rootPath = str()
		self.__metaPath = str()
		self.__sourcePath = str()
		self.__resourcePath = str()
		self.__workingspacePath = str()
		self.__applicationDataPath = str()
		self.__symbols = set()


 	#--------------------------------------------------------------------------------
	# 빌드 여부 설정.
	#--------------------------------------------------------------------------------
	def SetBinary(self, isBinary : bool) -> None:
		self.__isBinary = isBinary


	#--------------------------------------------------------------------------------
	# 디버그 모드 여부 설정.
	#--------------------------------------------------------------------------------
	def SetDebug(self, isDebugging : bool) -> None:
		self.__isDebugging = isDebugging


 	#--------------------------------------------------------------------------------
	# 실행 된 파일 이름.
	#--------------------------------------------------------------------------------
	def SetExecuteFileName(self, executeFileName : str) -> None:
		self.__executeFileName = executeFileName


	#--------------------------------------------------------------------------------
	# 루트 경로 설정.
	#--------------------------------------------------------------------------------
	def SetRootPath(self, rootPath : str) -> None:
		if not os.path.isdir(rootPath): os.makedirs(rootPath)
		self.__rootPath = rootPath.replace(BACKSLASH, SLASH)


	#--------------------------------------------------------------------------------
	# 메타 파일 경로 설정.
	#--------------------------------------------------------------------------------
	def SetMetaPath(self, metaPath : str) -> None:
		if not os.path.isdir(metaPath): os.makedirs(metaPath)
		self.__metaPath = metaPath.replace(BACKSLASH, SLASH)


	#--------------------------------------------------------------------------------
	# 소스 경로 설정.
	#--------------------------------------------------------------------------------
	def SetSourcePath(self, sourcePath : str) -> None:
		if not os.path.isdir(sourcePath): os.makedirs(sourcePath)
		self.__sourcePath = sourcePath.replace(BACKSLASH, SLASH)


	#--------------------------------------------------------------------------------
	# 리소스 경로 설정.
	#--------------------------------------------------------------------------------
	def SetResourcePath(self, resourcePath : str) -> None:
		if not os.path.isdir(resourcePath): os.makedirs(resourcePath)
		self.__resourcePath = resourcePath.replace(BACKSLASH, SLASH)


	#--------------------------------------------------------------------------------
	# 작업 디렉터리 경로 설정.
	#--------------------------------------------------------------------------------
	def SetWorkingspacePath(self, workingspacePath : str) -> None:
		if not os.path.isdir(workingspacePath): os.makedirs(workingspacePath)
		self.__workingspacePath = workingspacePath.replace(BACKSLASH, SLASH)


	#--------------------------------------------------------------------------------
	# 기존 심볼을 모두 지우고 새로운 심볼 목록 설정.
	#--------------------------------------------------------------------------------
	def SetSymbols(self, symbols : set[str]) -> None:
		self.RemoveAllSymbols()
		if not symbols:
			return

		for symbol in symbols:
			self.AddSymbol(symbol)


	#--------------------------------------------------------------------------------
	# 기존 심볼에 새로운 심볼 목록 추가.
	#--------------------------------------------------------------------------------
	def AddSymbols(self, symbols : set[str]) -> None:
		if not symbols:
			return

		for symbol in symbols:
			self.AddSymbol(symbol)


	#--------------------------------------------------------------------------------
	# 기존 심볼을 모두 지우고 새로운 심볼 목록 설정.
	#--------------------------------------------------------------------------------
	def AddSymbol(self, symbol : str) -> None:
		if not self.__symbols or not symbol:
			return

		# 입력 받은 문자열 정리.
		symbol = symbol.upper()
		
		# NONE, EMPTY, SPACE는 없는 것과 마찬가지이므로 제외.
		if symbol == NONE or symbol == EMPTY or symbol == SPACE:
			return

		# 기존 목록에 추가.
		self.__symbols.add(symbol)


	#--------------------------------------------------------------------------------
	# 대상 심볼을 제거.
	#--------------------------------------------------------------------------------
	def RemoveSymbol(self, symbol : str) -> None:
		if not self.__symbols or not symbol:
			return

		# 입력 받은 문자열 정리.
		symbol = symbol.upper()
		
		# NONE, EMPTY, SPACE는 없는 것과 마찬가지이므로 제외.
		if symbol == NONE or symbol == EMPTY or symbol == SPACE:
			return

		# 기존 목록에서 제거.
		# remove는 없는 요소를 지울 때 KeyError가 발생하지만 discard는 없으면 무시처리됨.
		self.__symbols.discard(symbol)


	#--------------------------------------------------------------------------------
	# 대상 심볼 목록을 모두 제거.
	#--------------------------------------------------------------------------------
	def RemoveSymbols(self, symbols : set[str]) -> None:
		if not self.__symbols or not symbols:
			return

		# NONE, EMPTY, SPACE는 없는 것과 마찬가지이므로 목록에서 제거.
		symbols.discard(NONE)
		symbols.discard(EMPTY)
		symbols.discard(SPACE)

		# 입력 받은 문자열 정리.
		# 기존 목록에서 제거.
		for symbol in symbols:
			self.RemoveSymbol(symbol)

	#--------------------------------------------------------------------------------
	# 심볼 목록을 모두 제거.
	#--------------------------------------------------------------------------------
	def RemoveAllSymbols(self) -> None:
		if not self.__symbols:
			return
		self.__symbols.clear()


	#--------------------------------------------------------------------------------
	# 빌드 후 실행 가능한 바이너리 파일에서 시작 되었는지 여부.
	#--------------------------------------------------------------------------------
	def IsBinary(self) -> bool:
		return self.__isBinary


	#--------------------------------------------------------------------------------
	# 현재 디버깅 상태인지 여부.
	#--------------------------------------------------------------------------------
	def IsDebugging(self) -> bool:
		return self.__isDebugging


	#--------------------------------------------------------------------------------
	# 실행된 파일 이름 반환.
	#--------------------------------------------------------------------------------
	def GetExecuteFileName(self) -> str:
		return self.__executeFileName


	#--------------------------------------------------------------------------------
	# 애플리케이션이 존재하는 경로 / 실행파일이 존재하는 경로.
	#--------------------------------------------------------------------------------
	def GetRootPath(self) -> str:
		return self.__rootPath


	#--------------------------------------------------------------------------------
	# 메타 경로 / 실행 파일 실행시 임시 메타 데이터 디렉터리 경로.
	#--------------------------------------------------------------------------------
	def GetMetaPath(self) -> str:
		return self.__metaPath
	

	#--------------------------------------------------------------------------------
	# 소스 경로 / 실행 파일 실행시 임시 소스 디렉터리 경로.
	#--------------------------------------------------------------------------------
	def GetSourcePath(self) -> str:
		return self.__sourcePath
	

	#--------------------------------------------------------------------------------
	# 리소스 경로 / 실행 파일 실행시 임시 리소스 디렉터리 경로.
	#--------------------------------------------------------------------------------
	def GetResourcePath(self) -> str:
		return self.__resourcePath


	#--------------------------------------------------------------------------------
	# 작업 디렉터리 경로.
	#--------------------------------------------------------------------------------
	def GetWorkingspacePath(self) -> str:
		return self.__workingspacePath
	

	#--------------------------------------------------------------------------------
	# 심볼 목록 반환.
	#--------------------------------------------------------------------------------
	def GetSymbols(self) -> list[str]:
		return list(self.__symbols)
	

	#--------------------------------------------------------------------------------
	# 심볼을 가지고 있는지 여부 반환.
	#--------------------------------------------------------------------------------
	def HasSymbol(self, symbolString : str) -> bool:
		symbolString = symbolString.upper()
		if symbolString not in self.__symbols:
			return False
		return True