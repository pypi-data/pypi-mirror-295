#--------------------------------------------------------------------------------
# 참조 모듈 목록.
#--------------------------------------------------------------------------------
from __future__ import annotations
from typing import Any, Final, Callable, Iterator, Optional, Type, TypeVar, Union, Tuple, List, Dict, Set, cast
import builtins
import inspect
import json
import os
from dduk.core.builtins import Builtins
from dduk.core.environment import PlatformType, GetPlatformType
from dduk.core.path import Path
from dduk.utility import jsonutility
from .executetype import ExecuteType
from .manifestdata import ManifestData, MANIFEST_VERSION
from .predefinedsymbols import PredefinedSymbols
from .yamlwrapper import YAMLWrapper


#--------------------------------------------------------------------------------
# 전역 상수 목록.
#--------------------------------------------------------------------------------
MANIFESTFILENAME : str = f"manifest.yaml"
BACKSLASH : str = "\\"
SLASH : str = "/"
COLON : str = "."
PYEXTENSION : str = ".py"
PACKAGE : str = "PACKAGE"
MODULE : str = "MODULE"
CLASS : str = "CLASS"
FUNCTION : str = "FUNCTION"
CARRIAGERETURN : str = "\r"
LINEFEED : str = "\n"
EMPTY : str = ""
LINEFEED : str = "\n"
READ : str = "r"
WRITE : str = "w"
UTF8 : str = "utf-8"
ASTERISK : str = "*"
DOUBLEQUOTATION : str = "\""
DDUK : str = "dduk"
APPLICATION : str = "application"
SOURCE : str = "source"
BINARY : str = "binary"
SERVICE : str = "service"
SYMBOLS : str = "symbols"
ARGUMENTS : str = "arguments"


#--------------------------------------------------------------------------------
# 준비자 클래스.
# - 데이터를 파이썬 코드로 변형해서 저장하므로 이후 추가 비용 없이 파일 이름만 알고 있으면 불러와 사용 가능.
# - 단, 이미 모듈이 리로드 되었다는 전제.
#--------------------------------------------------------------------------------
class Preparer:
	#--------------------------------------------------------------------------------
	# 멤버 변수 목록.
	#--------------------------------------------------------------------------------


	#--------------------------------------------------------------------------------
	# 생성됨.
	#--------------------------------------------------------------------------------
	def __init__(self) -> None:
		pass


	#--------------------------------------------------------------------------------
	# 준비.
	#--------------------------------------------------------------------------------
	def Prepare(self, executeType : ExecuteType) -> None:
		#--------------------------------------------------------------------------------
		# 프리페어 표시.
		Builtins.Print("__PREPARE__")

		# 플랫폼 종류 얻기.
		platformType : PlatformType = GetPlatformType()

		# 호출 스택 조사.
		stack = inspect.stack()
		if len(stack) < 2:
			raise Exception("Inspector Exception.")
		
		# 루트 경로와 루트 이름 생성.
		currrentFrame = inspect.stack()[1]
		startFilePath =  currrentFrame.filename
		rootPath = Path.GetRootPath(startFilePath)
		rootPath = rootPath.replace(BACKSLASH, SLASH)
		rootName = os.path.basename(rootPath)
		# rootName = rootName.lower()

		# 임시 디렉터리 생성.
		applicationDataPath = Path.GetApplicationDataPath()
		cachePath : str = os.path.join(applicationDataPath, "dduk-python", "dduk-application", rootName).replace(BACKSLASH, SLASH)
		metaPath : str = os.path.join(cachePath, "meta").replace(BACKSLASH, SLASH)
		os.makedirs(metaPath, exist_ok = True)

		# 파일 경로 생성.
		manifestFilePath : str = f"{metaPath}/{MANIFESTFILENAME}"

		# 기존 파일 제거.
		if os.path.exists(manifestFilePath):
			os.remove(manifestFilePath)

		# 매니페스트 데이터 생성.
		manifestData = ManifestData()
		manifestData.Name = rootName
		manifestData.Version = MANIFEST_VERSION
		manifestData.Type = executeType

		# 메인패키지, 모듈, 함수 설정.
		# 사용자레벨에서 따로 옵션 구분을 할 필요가 없기 때문에 일단은 고정 처리.
		manifestData.MainPackageName = "src"
		manifestData.MainModuleName = "__main__"
		manifestData.MainFunctionName = "Main"

		# 비주얼 스튜디오 코드로부터 셋팅 가져오기.
		vscodeSettingsFilePath = f"{rootPath}/.vscode/settings.json"
		settings : dict = self.GetSettingsFromVSCodeSettingFile(vscodeSettingsFilePath, manifestData.Type)
		if settings:
			# 심볼 목록.
			# 대문자로 일괄 변경 한 뒤 중복을 피해서 설정.
			if SYMBOLS in settings:
				manifestData.Symbols.clear()
				symbols : list[str] = settings[SYMBOLS]
				for symbol in symbols:
					symbol = symbol.upper()
					if symbol in manifestData.Symbols:
						continue
					manifestData.Symbols.append(symbol)
			# 인자 목록.
			if manifestData.Type == ExecuteType.SOURCE:
				if ARGUMENTS in settings:
					arguments : list[str] = settings[ARGUMENTS]
					manifestData.Arguments.clear()
					manifestData.Arguments.extend(arguments)

		# 바이너리.
		if manifestData.Type == ExecuteType.BINARY:
			Builtins.Print("__BINARY__")
			if not PredefinedSymbols.SYMBOL_BINARY in manifestData.Symbols:
				manifestData.Symbols.append(PredefinedSymbols.SYMBOL_BINARY.value)
		# 서비스.
		elif manifestData.Type == ExecuteType.SERVICE:
			Builtins.Print("__SERVICE__")
			if not PredefinedSymbols.SYMBOL_SERVICE in manifestData.Symbols:
				manifestData.Symbols.append(PredefinedSymbols.SYMBOL_SERVICE.value)
		# 소스.
		elif manifestData.Type == ExecuteType.SOURCE:
			Builtins.Print("__SOURCE__")
			if not PredefinedSymbols.SYMBOL_SOURCE in manifestData.Symbols:
				manifestData.Symbols.append(PredefinedSymbols.SYMBOL_SOURCE.value)
		else:
			raise Exception("Unavailable execution type.")


		# 파일 기록.
		YAMLWrapper.SaveYAMLToFile(manifestFilePath, manifestData)


	#--------------------------------------------------------------------------------
	# .vscode/settings.json 파일에서 상황에 맞는 데이터 가져오기.
	#--------------------------------------------------------------------------------
	def GetSettingsFromVSCodeSettingFile(self, vscodeSettingsFilePath : str, executeType : ExecuteType) -> dict:
		try:
			if not os.path.exists(vscodeSettingsFilePath):
				return dict()
			with builtins.open(vscodeSettingsFilePath, READ, encoding = UTF8) as file:
				string = file.read()
				jsonText = jsonutility.RemoveAllCommentsInString(string)
				vscodeSettings = json.loads(jsonText)
		except Exception as exception:
			Builtins.Print(exception)
			return dict()
		
		try:
			if not vscodeSettings:
				raise ValueError(f"not found settings.json")
			if DDUK not in vscodeSettings:
				raise ValueError(f"\"{DDUK}\" property not found in settings.json")
			else:
				ddukSettings = vscodeSettings[DDUK]
			if APPLICATION not in ddukSettings:
				raise ValueError(f"\"{APPLICATION}\" property not found in settings.json")
			else:
				applicationSettings = ddukSettings[APPLICATION]

			# 소스 모드 설정.
			if executeType == ExecuteType.SOURCE:
				if SOURCE in applicationSettings:
					return applicationSettings[SOURCE]
				else:
					raise ValueError(f"\"{SOURCE}\" property not found in settings.json")
			# 빌드 모드 설정.
			elif executeType == ExecuteType.BINARY:
				if BINARY in applicationSettings:
					return applicationSettings[BINARY]
				else:
					raise ValueError(f"\"{BINARY}\" property not found in settings.json")
			# 서비스 모드 설정.
			elif executeType == ExecuteType.SERVICE:
				if SERVICE in applicationSettings:
					return applicationSettings[SERVICE]
				else:
					raise ValueError(f"\"{SERVICE}\" property not found in settings.json")
		except Exception as exception:
			Builtins.Print(exception)
			return dict()		