#--------------------------------------------------------------------------------
# 참조 모듈 목록.
#--------------------------------------------------------------------------------
from __future__ import annotations
from typing import Any, Final, Callable, Iterator, Optional, Type, TypeVar, Union, Tuple, List, Dict, Set, cast
from enum import Enum


#--------------------------------------------------------------------------------
# 미리 선언된 내장 심볼 목록.
#--------------------------------------------------------------------------------
class PredefinedSymbols(Enum):

	# 바이너리 빌드 상태.
	SYMBOL_BUILD = "BUILD"
	SYMBOL_BINARY = "BINARY"

	# 서비스 상태.
	SYMBOL_SERVICE = "SERVICE"

	# 소스 상태.
	SYMBOL_SOURCE = "SOURCE"

	# 로그 파일 사용.
	SYMBOL_LOG = "LOG"

	# 서브프로세스 사용.
	SYMBOL_SUBPROCESS = "SUBPROCESS"


	#--------------------------------------------------------------------------------
	# 변환.
	#--------------------------------------------------------------------------------
	@staticmethod
	def Convert(value : str) -> PredefinedSymbols:
		valueLower : str = value.lower()
		for symbol in PredefinedSymbols:
			if valueLower == symbol.value.lower():
				return symbol
		return None
