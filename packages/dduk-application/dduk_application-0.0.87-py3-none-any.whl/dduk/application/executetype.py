#--------------------------------------------------------------------------------
# 참조 모듈 목록.
#--------------------------------------------------------------------------------
from __future__ import annotations
from typing import Any, Final, Callable, Iterator, Optional, Type, TypeVar, Union, Tuple, List, Dict, Set, cast
import builtins
from enum import Enum, auto


#--------------------------------------------------------------------------------
# 애플리케이션의 실행 종류.
#--------------------------------------------------------------------------------
class ExecuteType(Enum):
	#--------------------------------------------------------------------------------
	# 멤버 변수 목록.
	#--------------------------------------------------------------------------------
	UNKNOWN = auto() # 1. 정체불명.
	BINARY = auto() # 2. 바이너리.
	SERVICE = auto() # 3. 서비스.
	SOURCE = auto() # 4. 소스.


	#--------------------------------------------------------------------------------
	# 열거체의 요소 값을 요소 이름으로 변경.
	#--------------------------------------------------------------------------------
	@staticmethod
	def ToName(executeType : ExecuteType) -> str:
		return executeType.name.upper()


	#--------------------------------------------------------------------------------
	# 요소 이름을 열거체의 요소 값으로 변경.
	#--------------------------------------------------------------------------------
	@staticmethod
	def ToValue(executeTypeName : str) -> ExecuteType:
		try:
			executeTypeNameUpper = executeTypeName.upper()
			return ExecuteType[executeTypeNameUpper]
		except Exception as exception:
			raise ValueError(executeTypeNameUpper)