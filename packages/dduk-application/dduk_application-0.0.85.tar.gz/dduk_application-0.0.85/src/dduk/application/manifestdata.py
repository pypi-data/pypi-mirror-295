#--------------------------------------------------------------------------------
# 참조 모듈 목록.
#--------------------------------------------------------------------------------
from __future__ import annotations
from typing import Any, Final, Callable, Iterator, Optional, Type, TypeVar, Union, Tuple, List, Dict, Set, cast
import builtins
from .executetype import ExecuteType


#--------------------------------------------------------------------------------
# 상수 목록.
#--------------------------------------------------------------------------------
MANIFEST_VERSION : str = "1.0.0"


#--------------------------------------------------------------------------------
# 매니페스트 데이터. (준비된 데이터)
#--------------------------------------------------------------------------------
class ManifestData:
	#--------------------------------------------------------------------------------
	# 멤버 변수 목록.
	#--------------------------------------------------------------------------------
	Name : str
	Version : str
	Type : ExecuteType
	Symbols : list[str] # 실제로는 set이 맞지만 yaml에서 set을 표현할 수 없어 list로 대체.
	Arguments : list[str]
	MainPackageName : str 	# 실행 될 패키지 이름 : src.
	MainModuleName : str	# 실행 될 모듈 이름 : __main__.py 
	MainFunctionName : str	# 실행 될 함수 이름 : def Main(arguments : list[str]) -> int:


	#--------------------------------------------------------------------------------
	# 생성됨.
	#--------------------------------------------------------------------------------
	def __init__(self) -> None:
		self.Name = str()
		self.Version = MANIFEST_VERSION
		self.Type = ExecuteType.UNKNOWN
		self.Symbols = list()
		self.Arguments = list()
		self.MainPackageName = str()
		self.MainModuleName = str()
		self.MainFunctionName = str()