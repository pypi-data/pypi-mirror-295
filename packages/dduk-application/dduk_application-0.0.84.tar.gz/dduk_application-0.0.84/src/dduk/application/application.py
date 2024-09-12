#--------------------------------------------------------------------------------
# 참조 모듈 목록.
#--------------------------------------------------------------------------------
from __future__ import annotations
from typing import Any, Final, Callable, Iterator, Optional, Type, TypeVar, Union, Tuple, List, Dict, Set, cast
from enum import Enum
import sys
import traceback
from dduk.core.builtins import Builtins
from dduk.utility.logging.logger import Logger
from dduk.utility.logging.level import Level
from dduk.utility.strutility import GetTimestampString
from .internaldata import InternalData
from .internalrepository import InternalRepository
from .predefinedsymbols import PredefinedSymbols


#--------------------------------------------------------------------------------
# 전역 상수 목록.
#--------------------------------------------------------------------------------
EMPTY : str = ""
NONE : str = "NONE"
HYPHEN : str = "-"
COMMA : str = ","
SLASH : str = "/"
BACKSLASH : str = "\\"
COLON : str = ":"
SPACE : str = " "
DEFAULT_LOGGERNAME : str = "dduk-application"


#--------------------------------------------------------------------------------
# 애플리케이션 클래스.
#--------------------------------------------------------------------------------
class Application:
	#--------------------------------------------------------------------------------
	# 클래스 멤버 변수 목록.
	#--------------------------------------------------------------------------------
	__MessageModifier : Callable[[str], str] = None


	#--------------------------------------------------------------------------------
	# 종료 함수.
	#--------------------------------------------------------------------------------
	@staticmethod
	def Exit(exitcode : int) -> None:
		sys.exit(exitcode)


	#--------------------------------------------------------------------------------
	# 메시지 수정자 설정.
	#--------------------------------------------------------------------------------
	@staticmethod
	def SetMessageModifier(messageModifier : Callable[[str], str]):
		Application.__MessageModifier = messageModifier


	#--------------------------------------------------------------------------------
	# 로그 출력.
	#--------------------------------------------------------------------------------
	@staticmethod
	def Print(message : str, level : Level) -> None:
		# 메시지가 혹시라도 str이 아닌 다른 객체일 경우를 대비하여 변환.
		message = str(message)
		logger : Logger = InternalRepository.Get(Logger)

		# 콘솔에 출력. (마이크로세컨드는 일단 제외)
		# timestamp = GetTimestampString(HYPHEN, SPACE, COLON, True, COMMA)
		timestamp = GetTimestampString(HYPHEN, SPACE, COLON)
		levelName = Level.GetLevelName(level)

		# 메시지 수정자가 있을 경우 메시지에 개입하여 수정.
		try:
			if Application.__MessageModifier:
				message = Application.__MessageModifier(message)
			else:
				message = message
		except Exception as exception:
			message = message
			
		# 로그 콘솔 출력.
		logger.LogToConsole(f"[{timestamp}][{levelName}]{message}", level)

		# 로그 파일 출력.
		useLogFile : bool = Application.HasSymbolWithPredefinedSymbol(PredefinedSymbols.SYMBOL_LOG)
		if useLogFile:
			logger.LogToFile(message, level)


	#--------------------------------------------------------------------------------
	# 디버그 출력.
	#--------------------------------------------------------------------------------
	@staticmethod
	def LogDebug(message : Union[str, Exception]) -> None:
		if Builtins.IsInstanceType(message, Exception):
			message = str(message)
		Application.Print(message, Level.DEBUG)


	#--------------------------------------------------------------------------------
	# 인포 출력.
	#--------------------------------------------------------------------------------
	@staticmethod
	def Log(message : Union[str, Exception]) -> None:
		if Builtins.IsInstanceType(message, Exception):
			message = str(message)
		Application.Print(message, Level.INFO)


	#--------------------------------------------------------------------------------
	# 워닝 출력.
	#--------------------------------------------------------------------------------
	@staticmethod
	def LogWarning(message : Union[str, Exception]) -> None:
		if Builtins.IsInstanceType(message, Exception):
			message = str(message)
		Application.Print(message, Level.WARNING)


	#--------------------------------------------------------------------------------
	# 에러 출력.
	#--------------------------------------------------------------------------------
	@staticmethod
	def LogError(message : Union[str, Exception]) -> None:
		if Builtins.IsInstanceType(message, Exception):
			message = str(message)
		Application.Print(message, Level.ERROR)


	#--------------------------------------------------------------------------------
	# 익셉션 출력.
	#--------------------------------------------------------------------------------
	@staticmethod
	def LogException(exception : Union[str, Exception]) -> None:
		if Builtins.IsInstanceType(message, str):
			message = Exception(message)
		Application.Print(exception, Level.EXCEPTION)


	#--------------------------------------------------------------------------------
	# 익셉션 출력 및 앱 터트리기.
	#--------------------------------------------------------------------------------
	@staticmethod
	def LogExceptionWithExit(exception : Exception, useTraceback : bool = True) -> None:
		if useTraceback:
			traceback.print_exc()
			tb = exception.__traceback__
			while tb:
				filename = tb.tb_frame.f_code.co_filename
				lineno = tb.tb_lineno
				funcname = tb.tb_frame.f_code.co_name
				result = traceback.format_exc()
				result = result.strip()
				line = result.splitlines()[-1]
				Application.Print(f"Exception in {filename}, line {lineno}, in {funcname}", Level.EXCEPTION)
				Application.Print(f"\t{line}", Level.EXCEPTION)
				tb = tb.tb_next
		else:
			Application.Print(exception, Level.EXCEPTION)

		# 종료.
		Application.Exit(1)
	
	#--------------------------------------------------------------------------------
	# 크리티컬 출력.
	#--------------------------------------------------------------------------------
	@staticmethod
	def LogCritical(message : str) -> None:
		Application.Print(message, Level.CRITICAL)
	

	#--------------------------------------------------------------------------------
	# 빌드 된 바이너리 실행 파일인지 여부.
	#--------------------------------------------------------------------------------
	@staticmethod
	def IsBinary() -> bool:
		internalData = InternalRepository.Get(InternalData)
		return internalData.IsBinary()


	#--------------------------------------------------------------------------------
	# 디버그 상태인지 여부.
	#--------------------------------------------------------------------------------
	@staticmethod
	def IsDebugging() -> bool:
		internalData = InternalRepository.Get(InternalData)
		return internalData.IsDebugging()


	#--------------------------------------------------------------------------------
	# 실행된 파일 이름 반환.
	#--------------------------------------------------------------------------------
	@staticmethod
	def GetExecuteFileName() -> str:
		internalData = InternalRepository.Get(InternalData)
		return internalData.GetExecuteFileName()


	#--------------------------------------------------------------------------------
	# 애플리케이션이 존재하는 경로 / 프로젝트가 존재하는 경로.
	#--------------------------------------------------------------------------------
	@staticmethod
	def GetRootPath() -> str:
		internalData = InternalRepository.Get(InternalData)
		return internalData.GetRootPath()


	#--------------------------------------------------------------------------------
	# 메타 파일이 존재하는 경로.
	#--------------------------------------------------------------------------------
	@staticmethod
	def GetMetaPath() -> str:
		internalData = InternalRepository.Get(InternalData)
		return internalData.GetMetaPath()
	
	
	#--------------------------------------------------------------------------------
	# 소스 경로 / 실행 파일 실행시 임시 소스 디렉터리 경로.
	#--------------------------------------------------------------------------------
	@staticmethod
	def GetSourcePath() -> str:
		internalData = InternalRepository.Get(InternalData)
		return internalData.GetSourcePath()
	

	#--------------------------------------------------------------------------------
	# 리소스 경로 / 실행 파일 실행시 임시 리소스 디렉터리 경로.
	#--------------------------------------------------------------------------------
	@staticmethod
	def GetResourcePath() -> str:
		internalData = InternalRepository.Get(InternalData)
		return internalData.GetResourcePath()


	#--------------------------------------------------------------------------------
	# 작업 디렉터리 경로.
	#--------------------------------------------------------------------------------
	@staticmethod
	def GetWorkingspacePath() -> str:
		internalData = InternalRepository.Get(InternalData)
		return internalData.GetWorkingspacePath()
	

	#--------------------------------------------------------------------------------
	# 애플리케이션이 존재하는 경로에 상대 경로를 입력하여 절대 경로를 획득.
	#--------------------------------------------------------------------------------
	@staticmethod
	def GetRootPathWithRelativePath(relativePath : str) -> str:
		internalData = InternalRepository.Get(InternalData)
		rootPath = internalData.GetRootPath()
		if not relativePath:
			return rootPath
		relativePath = relativePath.replace(BACKSLASH, SLASH)
		absolutePath = f"{rootPath}/{relativePath}"
		return absolutePath


	#--------------------------------------------------------------------------------
	# 메타파일이 존재하는 경로에 상대 경로를 입력하여 절대 경로를 획득.
	#--------------------------------------------------------------------------------
	@staticmethod
	def GetMetaPathWithRelativePath(relativePath : str) -> str:
		internalData = InternalRepository.Get(InternalData)
		metaPath = internalData.GetMetaPath()
		if not relativePath:
			return metaPath
		relativePath = relativePath.replace(BACKSLASH, SLASH)
		absolutePath = f"{metaPath}/{relativePath}"
		return absolutePath


	#--------------------------------------------------------------------------------
	# 소스가 존재하는 경로에 상대 경로를 입력하여 절대 경로를 획득.
	#--------------------------------------------------------------------------------
	@staticmethod
	def GetSourcePathWithRelativePath(relativePath : str) -> str:
		internalData = InternalRepository.Get(InternalData)
		sourcePath = internalData.GetSourcePath()
		if not relativePath:
			return sourcePath
		relativePath = relativePath.replace(BACKSLASH, SLASH)
		absolutePath = f"{sourcePath}/{relativePath}"
		return absolutePath
	

	#--------------------------------------------------------------------------------
	# 리소스가 존재하는 경로에 상대 경로를 입력하여 절대 경로를 획득.
	#--------------------------------------------------------------------------------
	@staticmethod
	def GetResourcePathWithRelativePath(relativePath : str) -> str:
		internalData = InternalRepository.Get(InternalData)
		resourcePath = internalData.GetResourcePath()
		if not relativePath:
			return resourcePath
		relativePath = relativePath.replace(BACKSLASH, SLASH)
		absolutePath = f"{resourcePath}/{relativePath}"
		return absolutePath
	

	#--------------------------------------------------------------------------------
	# 작업 디렉터리 경로에 상대 경로를 입력하여 절대 경로를 획득.
	# - 작업 디렉터리 경로.
	# - 프로젝트 일 때 : src와 동일 계층의 workingspace 디렉터리 이다.
	# - 실행 파일 일 때 : 실행 파일과 동일 디렉터리 이다.
	#--------------------------------------------------------------------------------
	@staticmethod
	def GetWorkingspacePathWithRelativePath(relativePath : str) -> str:
		internalData = InternalRepository.Get(InternalData)
		workingspacePath = internalData.GetWorkingspacePath()
		if not relativePath:
			return workingspacePath
		relativePath = relativePath.replace(BACKSLASH, SLASH)
		absolutePath = f"{workingspacePath}/{relativePath}"
		return absolutePath


	#--------------------------------------------------------------------------------
	# 심볼 목록 반환.
	#--------------------------------------------------------------------------------
	@staticmethod
	def GetSymbols() -> list[str]:
		internalData = InternalRepository.Get(InternalData)
		return internalData.GetSymbols()
	

	#--------------------------------------------------------------------------------
	# 심볼을 가지고 있는지 여부 반환.
	#--------------------------------------------------------------------------------
	@staticmethod
	def HasSymbol(symbolString : str) -> bool:
		internalData = InternalRepository.Get(InternalData)
		return internalData.HasSymbol(symbolString)
	

	#--------------------------------------------------------------------------------
	# 심볼을 가지고 있는지 여부 반환.
	# - 인자로 들어가는 열거체의 값은 반드시 문자열이어야 한다.
	#--------------------------------------------------------------------------------
	@staticmethod
	def HasSymbolWithEnum(symbol : Enum) -> bool:
		if isinstance(symbol.value, str):
			internalData = InternalRepository.Get(InternalData)
			return internalData.HasSymbol(symbol.value)
		else:
			Application.LogError(f"{symbol}.value is not str type.")
			return False
	

	#--------------------------------------------------------------------------------
	# 심볼을 가지고 있는지 여부 반환.
	#--------------------------------------------------------------------------------
	@staticmethod
	def HasSymbolWithPredefinedSymbol(symbol : PredefinedSymbols) -> bool:
		return Application.HasSymbolWithEnum(symbol)