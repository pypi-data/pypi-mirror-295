#--------------------------------------------------------------------------------
# 참조 모듈 목록.
#--------------------------------------------------------------------------------
from __future__ import annotations
from typing import Any, Final, Callable, Iterator, Optional, Type, TypeVar, Union, Tuple, List, Dict, Set, cast
import builtins
import importlib
import os
# import signal
import sys
from types import ModuleType
import debugpy
from dduk.core.builtins import Builtins
from dduk.core.path import Path
from dduk.utility.logging.logger import Logger
from dduk.utility.logging.level import Level
from dduk.utility.strutility import GetTimestampString
from .application import Application
from .executetype import ExecuteType
from .internaldata import InternalData
from .internalrepository import InternalRepository
from .manifestdata import ManifestData
from .predefinedsymbols import PredefinedSymbols
from .preparer import MANIFESTFILENAME
from .yamlwrapper import YAMLWrapper


#--------------------------------------------------------------------------------
# 전역 상수 목록.
#--------------------------------------------------------------------------------
EMPTY : str = ""
SPACE : str = " "
LEFTSQUAREBRACKET : str = "["
FROZEN : str = "frozen"
BACKSLASH : str = "\\"
SLASH : str = "/"
UTF8 : str = "utf-8"
READ : str = "r"
WRITE : str = "w"


#--------------------------------------------------------------------------------
# 런처 클래스.
#--------------------------------------------------------------------------------
class Launcher:
	#--------------------------------------------------------------------------------
	# 실행.
	#--------------------------------------------------------------------------------
	def Launch(self) -> int:
		#--------------------------------------------------------------------------------
		# 런치 표시.
		Builtins.Print("__LAUNCH__")
		
		#--------------------------------------------------------------------------------
		# 내부 데이터 클래스 생성.
		internalData = InternalRepository.Get(InternalData)

		#--------------------------------------------------------------------------------
		# 경로 설정.
		isBinary : bool = Launcher.VerifyBinary()
		internalData.SetBinary(isBinary)
		applicationDataBasePath : str = Path.GetApplicationDataPathWithRelativePaths("dduk-python", "dduk-application")

		# 바이너리 실행 일 때.
		if internalData.IsBinary():
			# 실행파일에서 생성되는 임시 루트 경로.
			# 캐시패스는 리소스를 위한 캐시 디렉터리로 실제 실행 파일의 위치가 아님. 
			# 또한 윈도우에서는 8.3형식에 의해 마음대로 캐시폴더의 경로를 짧은 형태로 수정할 수 있어서 캐시 디렉터리 이름만 가져와 덧붙이는 식으로 방어처리.
			userPath = os.path.expanduser("~")
			cacheName : str = os.path.basename(sys._MEIPASS)
			cachePath : str = os.path.join(userPath, "AppData", "Local", "Temp", cacheName).replace(BACKSLASH, SLASH)
			rootPath : str = os.path.dirname(sys.executable).replace(BACKSLASH, SLASH)
			sourcePath : str = os.path.join(cachePath, "src").replace(BACKSLASH, SLASH)
			resourcePath : str = os.path.join(cachePath, "res").replace(BACKSLASH, SLASH)
			workingspacePath : str = rootPath.replace(BACKSLASH, SLASH) # 빌드시 작업 디렉터리 경로는 루트 경로와 동일.
			metaPath : str = os.path.join(cachePath, "meta").replace(BACKSLASH, SLASH)

		# 소스 실행 일 때.
		else:
			# 현재 실행되는 코드 대상을 기준으로 한 경로.
			# 따라서 반드시 메인 스크립트는 src 안에 있어야 한다.
			executeModule = sys.modules["__main__"]
			currentFilePath = os.path.abspath(executeModule.__file__).replace(BACKSLASH, SLASH)
			sourcePath : str = os.path.dirname(currentFilePath).replace(BACKSLASH, SLASH)
			rootPath : str = os.path.dirname(sourcePath).replace(BACKSLASH, SLASH)
			rootName = os.path.basename(rootPath)
			resourcePath : str = os.path.join(rootPath, "res").replace(BACKSLASH, SLASH)
			workingspacePath : str = os.path.join(rootPath, "workingspace").replace(BACKSLASH, SLASH)
			applicationDataPath = os.path.join(applicationDataBasePath, rootName).replace(BACKSLASH, SLASH)
			metaPath : str = os.path.join(applicationDataPath, "meta").replace(BACKSLASH, SLASH)
		
		#--------------------------------------------------------------------------------
		# 실행을 위한 준비 데이터 불러오기. (YAML 파일 로드)
		manifestFilePath : str = f"{metaPath}/{MANIFESTFILENAME}"
		Builtins.Print(f"manifestFilePath: {manifestFilePath}")
		YAMLWrapper.SetConstructor("!!python/object:dduk.application.manifestdata.ManifestData", YAMLWrapper.ManifestDataConstructor)
		YAMLWrapper.SetConstructor("!!python/object/apply:dduk.application.executetype.ExecuteType", YAMLWrapper.ExecuteTypeConstructor)
		YAMLWrapper.SetConstructor("!!python/object/apply:dduk.application.predefinedsymbols.PredefinedSymbols", YAMLWrapper.PredefinedSymbolsConstructor)
		manifestData : ManifestData = YAMLWrapper.LoadYAMLFromFile(manifestFilePath)
		InternalRepository.Link(manifestData)

		projectName = manifestData.Name
		applicationDataPath = os.path.join(applicationDataBasePath, projectName)

		# 모든 심볼 제거.
		internalData.RemoveAllSymbols()

		# 바이너리.
		if manifestData.Type == ExecuteType.BINARY:
			Builtins.Print("__BINARY__")
			logsPath = os.path.join(applicationDataPath, "logs").replace(BACKSLASH, SLASH)
		# 서비스.
		elif manifestData.Type == ExecuteType.SERVICE:
			Builtins.Print("__SERVICE__")
			logsPath = os.path.join(applicationDataPath, "logs").replace(BACKSLASH, SLASH)
		# 소스.
		elif manifestData.Type == ExecuteType.SOURCE:
			Builtins.Print("__SOURCE__")
			logsPath = os.path.join(rootPath, "logs")
		# 그 외.
		else:
			raise Exception("Unavailable execution type.")
		
		#--------------------------------------------------------------------------------
		# 심볼 설정.
		# 준비 데이터로부터 심볼목록을 불러와 설정.
		Builtins.Print("__PREPARED__")
		internalData.AddSymbols(manifestData.Symbols)

		#--------------------------------------------------------------------------------
		# 디버깅 설정. (서비스와 빌드는 디버깅 할 수 없다고 간주한다.)
		if manifestData.Type == ExecuteType.SOURCE:
			isDebug : bool = Launcher.VerifyDebug()
			internalData.SetDebug(isDebug)
		else:
			internalData.SetDebug(False)

		#--------------------------------------------------------------------------------
		# 실행 인수 : 실행된 파일 이름 설정.
		if sys.argv:
			Builtins.Print("__EXECUTE__")
			executeFileName = sys.argv[0]
			internalData.SetExecuteFileName(executeFileName)

		#--------------------------------------------------------------------------------
		# 실행 인수 : 입력된 데이터 설정.
		# 준비 데이터로부터 심볼목록을 불러와 설정.
		Builtins.Print("__ARGUMENT__")
		if manifestData.Type == ExecuteType.SOURCE:
			sys.argv.clear()
			sys.argv.append(executeFileName)
			sys.argv.extend(manifestData.Arguments)

		#--------------------------------------------------------------------------------
		# 경로 설정.
		internalData.SetRootPath(rootPath)
		internalData.SetMetaPath(metaPath)
		internalData.SetSourcePath(sourcePath)
		internalData.SetResourcePath(resourcePath)
		internalData.SetWorkingspacePath(workingspacePath)

		#--------------------------------------------------------------------------------
		# 경로 출력.
		Builtins.Print(f"isBuild: {Application.IsBinary()}")
		Builtins.Print(f"rootPath: {Application.GetRootPath()}")
		Builtins.Print(f"metaPath: {Application.GetMetaPath()}")
		Builtins.Print(f"sourcePath: {Application.GetSourcePath()}")
		Builtins.Print(f"resourcePath: {Application.GetResourcePath()}")
		Builtins.Print(f"workingspacePath: {Application.GetWorkingspacePath()}")

		#--------------------------------------------------------------------------------
		# 로거 생성.
		# 순서 : DEBUG < INFO < WARNING < ERROR < CRITICAL.
		loggerName : str = manifestData.Name.lower()
		minimumLevel : Level = Level.NONE
		timestamp = GetTimestampString(EMPTY, EMPTY, EMPTY)
		executeTypeName : str = manifestData.Type.name.lower()
		logFilePath = f"{logsPath}/{executeTypeName}-{timestamp}.log"

		try:
			# 빌드.
			if manifestData.Type == ExecuteType.BINARY:
				minimumLevel = Level.WARNING
			# 서비스.
			elif manifestData.Type == ExecuteType.SERVICE:
				minimumLevel = Level.INFO
			# 소스.
			else:
				if isDebug:
					minimumLevel = Level.DEBUG
				else:
					minimumLevel = Level.INFO

			# 등록.
			logger = Logger(loggerName, logFilePath, minimumLevel)
			InternalRepository.Link(logger)

			# 기본 룰 설정.
			# 맨 앞이 "[" 인 경우 앞에 공백을 붙이지 않는다.
			Application.SetMessageModifier(lambda message: message if message.startswith(LEFTSQUAREBRACKET) else SPACE + message)
		except Exception as exception:
			Builtins.Print(exception)

		#--------------------------------------------------------------------------------
		# 패키지 임포트.
		# 이상한 코드지만 메인 패키지의 부모를 추가해야 메인패키지가 등록된다.
		if isBinary:
			if cachePath not in sys.path:
				sys.path.append(cachePath)
		else:
			if rootPath not in sys.path:
				sys.path.append(rootPath)

		# 메인 패키지의 부모 디렉터리가 추가되어있지 않으면 메인 패키지를 임포트할 수 없다.
		try:
			importlib.import_module("src")
		except ModuleNotFoundError:
			raise ImportError(f"ImportError: src")

		# # 시그널 등록.
		# signal.signal(signal.SIGINT, lambda sight, frame: sys.exit(0))

		#--------------------------------------------------------------------------------
		# 시작.
		try:
			# 잔여 인자 출력.
			if sys.argv:
				Application.Log("__SYMBOLS__")
				index = 0
				for symbol in manifestData.Symbols:
					Application.Log(f"- [{index}] {symbol}")
					index += 1
			if sys.argv:
				Application.Log("__ARGUMENTS__")
				index = 0
				for arg in sys.argv:
					Application.Log(f"- [{index}] {arg}")
					index += 1

			# 메인 패키지 동적 로드.
			# 실행된 프로젝트 소스 폴더 내의 __main__.py를 찾아서 호출.
			mainPackageName : str = manifestData.MainPackageName
			mainModuleName : str = manifestData.MainModuleName
			mainFunctionName : str = manifestData.MainFunctionName
			mainModuleFilePath : str = Application.GetSourcePathWithRelativePath(f"{mainModuleName}.py")
			if not os.path.isfile(mainModuleFilePath):
				raise FileNotFoundError(f"FileNotFoundError: {mainModuleFilePath}")
			mainModuleSpecification = importlib.util.spec_from_file_location(f"{mainPackageName}.{mainModuleName}", mainModuleFilePath)
			if not mainModuleSpecification:
				raise Exception(f"Exception: Not Readable Main Modue. ({mainModuleFilePath})")
			mainModule = importlib.util.module_from_spec(mainModuleSpecification)
			mainModule.__package__ = mainPackageName
			mainModuleSpecification.loader.exec_module(mainModule)

			# 메인 함수 실행.
			if not builtins.hasattr(mainModule, mainFunctionName):
				raise AttributeError(f"AttributeError: Not Found Main Attribute. ({mainModuleFilePath})")
			mainFunction = builtins.getattr(mainModule, mainFunctionName)
			exitcode = mainFunction(sys.argv)
			return exitcode				
		# except KeyboardInterrupt as exception:
		# 	# if application.IsBuild():
		# 	# 	return 0
		# 	# else:
		# 	# 	Application.LogException(exception)
		# 	return 0
		except Exception as exception:
			Application.LogException(exception)


	#--------------------------------------------------------------------------------
	# 실행 환경 체크 : 바이너리 파일에서 실행했는지 상태 확인.
	# - pyinstaller : FROZEN
	#--------------------------------------------------------------------------------
	@staticmethod
	def VerifyBinary() -> bool:
		try:
			isVerify = builtins.getattr(sys, FROZEN, False)
			return isVerify
		except Exception as exception:
			Builtins.Print(exception)
			return False


	#--------------------------------------------------------------------------------
	# 실행 환경 체크 : 디버그 세션에 연결 된 상태 확인.
	# - pydevd : PyCharm, 3dsmax
	# - ptvsd : 3dsmax
	# - debugpy : VSCode
	#--------------------------------------------------------------------------------
	@staticmethod
	def VerifyDebug() -> bool:
		try:
			isVerify = debugpy.is_client_connected()
			return isVerify
		except Exception as exception:
			Builtins.Print(exception)
			return False