#--------------------------------------------------------------------------------
# 참조 모듈 목록.
#--------------------------------------------------------------------------------
from __future__ import annotations
from typing import Any, Final, Callable, Iterator, Optional, Type, TypeVar, Union, Tuple, List, Dict, Set, cast
import builtins
import importlib
import os
import sys
import unittest
from dduk.core.path import Path
from dduk.utility.logging.level import Level
from dduk.utility.logging.logger import Logger
from dduk.utility.strutility import GetTimestampString
from .application import Application
from .internaldata import InternalData
from .internalrepository import InternalRepository


#--------------------------------------------------------------------------------
# 전역 상수 목록.
#--------------------------------------------------------------------------------
SLASH : str = "/"
BACKSLASH : str = "\\"
EMPTY : str = ""


#--------------------------------------------------------------------------------
# 테스트 런처 클래스.
#--------------------------------------------------------------------------------
class TestsLauncher:
	#--------------------------------------------------------------------------------
	# 실행.
	# - 매니페스트 로드 하지 않음.
	# - Application 및 로그는 강제 사용 처리.
	#--------------------------------------------------------------------------------
	def Launch(self, pattern = "test_*.py") -> int:
		#--------------------------------------------------------------------------------
		# 테스트 표시.
		builtins.print("__TESTS__")

		#--------------------------------------------------------------------------------
		# 내부 데이터 클래스 생성.
		internalData = InternalRepository.Get(InternalData)

		#--------------------------------------------------------------------------------
		# 경로 설정.
		internalData.SetBinary(False)
		internalData.SetDebug(False)
		applicationDataBasePath : str = Path.GetApplicationDataPathWithRelativePaths("dduk-python", "dduk-application")

		# 테스트 실행으로 간주.
		# 현재 __main__ 으로 실행되는 코드 대상을 기준으로 한 경로.
		# 따라서 반드시 메인 스크립트는 src 안에 있어야 한다.
		currentFilePath = os.path.abspath(sys.modules["__main__"].__file__).replace(BACKSLASH, SLASH)
		testsPath : str = os.path.dirname(currentFilePath).replace(BACKSLASH, SLASH)
		rootPath : str = os.path.dirname(testsPath).replace(BACKSLASH, SLASH)
		rootName = os.path.basename(rootPath)
		sourcePath : str = os.path.join(rootPath, "src").replace(BACKSLASH, SLASH)
		resourcePath : str = os.path.join(rootPath, "res").replace(BACKSLASH, SLASH)
		workingspacePath : str = os.path.join(rootPath, "workingspace").replace(BACKSLASH, SLASH)
		applicationDataPath = os.path.join(applicationDataBasePath, rootName).replace(BACKSLASH, SLASH)
		metaPath : str = os.path.join(applicationDataPath, "meta").replace(BACKSLASH, SLASH)
		logsPath : str = os.path.join(rootPath, "logs").replace(BACKSLASH, SLASH)

		#--------------------------------------------------------------------------------
		# 경로 설정.
		internalData.SetRootPath(rootPath)
		internalData.SetMetaPath(metaPath)
		internalData.SetSourcePath(sourcePath)
		internalData.SetResourcePath(resourcePath)
		internalData.SetWorkingspacePath(workingspacePath)

		#--------------------------------------------------------------------------------
		# 경로 출력.
		builtins.print(f"isBuild: {Application.IsBinary()}")
		builtins.print(f"rootPath: {Application.GetRootPath()}")
		builtins.print(f"metaPath: {Application.GetMetaPath()}")
		builtins.print(f"sourcePath: {Application.GetSourcePath()}")
		builtins.print(f"resourcePath: {Application.GetResourcePath()}")
		builtins.print(f"workingspacePath: {Application.GetWorkingspacePath()}")

		#--------------------------------------------------------------------------------
		# 테스트 로거 생성.
		# 순서 : DEBUG < INFO < WARNING < ERROR < CRITICAL.
		timestamp = GetTimestampString(EMPTY, EMPTY, EMPTY)
		testLoggerName : str = rootName.lower()
		logFilePath = f"{logsPath}/tests-{timestamp}.log"
		minimumLevel : Level = Level.DEBUG
		logger = Logger(testLoggerName, logFilePath, minimumLevel)
		InternalRepository.Link(logger)

		#--------------------------------------------------------------------------------
		# 패키지 임포트.
		# 이상한 코드지만 현재 패키지의 부모를 추가해야 현재 패키지가 등록된다.
		if rootPath not in sys.path:
			sys.path.append(rootPath)

		# 현재 패키지의 부모 디렉터리가 추가되어있지 않으면 현재 패키지를 임포트할 수 없다.
		try:
			importlib.import_module("src")
		except ModuleNotFoundError:
			raise ImportError(f"Failed to import the src package. Make sure that src is a valid package.")
		try:
			importlib.import_module("tests")
		except ModuleNotFoundError:
			raise ImportError(f"Failed to import the tests package. Make sure that src is a valid package.")

		#--------------------------------------------------------------------------------
		# 시작.
		try:
			# 패키지 실행.
			# 실행된 프로젝트 소스 폴더 내의 __main__.py를 찾아서 그 안의 Main()을 호출.
			testsModuleFilePath : str = os.path.join(testsPath, "__main__.py")
			if not os.path.isfile(testsModuleFilePath):
				raise FileNotFoundError(testsModuleFilePath)
			mainModuleSpecification = importlib.util.spec_from_file_location("tests.__main__", testsModuleFilePath)
			mainModule = importlib.util.module_from_spec(mainModuleSpecification)
			mainModule.__package__ = "tests"
			mainModuleSpecification.loader.exec_module(mainModule)
			
			# 테스트 로더 생성.
			loader = unittest.TestLoader()

			# tests 폴더 내의 test_ 로 시작하는 모든 스크립트 파일을 기준으로 테스트 스위트 생성.
			suite = loader.discover(start_dir = testsPath, pattern = pattern)

			# 테스트 실행기 생성 및 실행.
			runner = unittest.TextTestRunner()
			runner.run(suite)
			return 0
		except Exception as exception:
			builtins.print(exception)