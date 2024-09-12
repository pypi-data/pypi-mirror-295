#--------------------------------------------------------------------------------
# 참조 모듈 목록.
#--------------------------------------------------------------------------------
from __future__ import annotations
from typing import Any, Final, Callable, Iterator, Optional, Type, TypeVar, Union, Tuple, List, Dict, Set, cast
import builtins
from enum import Enum, auto


#--------------------------------------------------------------------------------
# IDE 종류.
#--------------------------------------------------------------------------------
class IDEType(Enum):
	#--------------------------------------------------------------------------------
	# 멤버 변수 목록.
	#--------------------------------------------------------------------------------
	UNKNOWN = auto() # 1. 정체불명.
	VISUALSTUDIO = auto() # 2. 비주얼스튜디오.
	VSCODE = auto() # 2. 비주얼스튜디오코드.
	PYCHARM = auto() # 4. 파이참.


	#--------------------------------------------------------------------------------
	# 열거체의 요소 값을 요소 이름으로 변경.
	#--------------------------------------------------------------------------------
	@staticmethod
	def ToName(ideType : IDEType) -> str:
		return ideType.name.upper()


	#--------------------------------------------------------------------------------
	# 요소 이름을 열거체의 요소 값으로 변경.
	#--------------------------------------------------------------------------------
	@staticmethod
	def ToValue(ideTypeName : str) -> IDEType:
		try:
			ideTypeNameUpper = ideTypeName.upper()
			return IDEType[ideTypeNameUpper]
		except Exception as exception:
			raise ValueError(ideTypeNameUpper)