#--------------------------------------------------------------------------------
# 참조 모듈 목록.
#--------------------------------------------------------------------------------
from __future__ import annotations
from typing import Any, Final, Callable, Iterator, Optional, Type, TypeVar, Union, Tuple, List, Dict, Set, cast
import builtins
import sys
import os
from importlib.resources import open_text, open_binary


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
READ : str = "r"
WRITE : str = "w"
UTF8 : str = "utf-8"
PACKAGENAME : str = "dduk.application.res"


#--------------------------------------------------------------------------------
# 설치.
#--------------------------------------------------------------------------------
def Setup(rootPath : str) -> None:
	builtins.print("dduk.application.command.Setup()")
	# open_text(PACKAGENAME, )


#--------------------------------------------------------------------------------
# 도움말.
#--------------------------------------------------------------------------------
def Help() -> None:
	builtins.print("Usage: dduk-application|dduk_applicationddukapplication|dduk-app|dduk_app|ddukapp|dap")
	builtins.print("ddukapp setup: 현재 작업 디렉터리를 기준으로 프로젝트 템플릿 생성.")


#--------------------------------------------------------------------------------
# 메인.
#--------------------------------------------------------------------------------
def Main() -> None:

	# 작업 디렉터리의 경로 추출.
	rootPath :str = os.getcwd()
	rootPath = rootPath.replace(BACKSLASH, SLASH)

	# 실행파일 추출.
	executeFileName : str = sys.argv[0]
	builtins.print(f"{executeFileName}")

	# 인자가 없으면 명령어.
	sys.argv = sys.argv[1:]	
	if not sys.argv:
		Help()
		return

	# 명령이름 추출.
	command = sys.argv[0]
	command = command.lower()
	if command == "setup":
		Setup(rootPath)
	else:
		builtins.print(f"ERROR: {command}")