#--------------------------------------------------------------------------------
# 참조 모듈 목록.
#--------------------------------------------------------------------------------
from __future__ import annotations
from typing import Any, Final, Callable, Iterator, Optional, Type, TypeVar, Union, Tuple, List, Dict, Set, cast
import platform
from enum import Enum, auto
from .builtins import Builtins


#--------------------------------------------------------------------------------
# 플랫폼 타입.
#--------------------------------------------------------------------------------
class PlatformType(Enum):
	UNKNOWN = auto()
	
	# windows.
	WINDOWS = auto()

	# linux.
	LINUX = auto()
	ANDROID = auto()

	# apple.
	MACOS = auto()
	IOS = auto()
	IPADOS = auto()
	WATCHOS = auto()
	TVOS = auto()
	VISIONOS = auto()

	# web.
	WEBGL = auto()
	WEBGPU = auto()


#--------------------------------------------------------------------------------
# 현재 시스템의 플랫폼 타입 반환.
#--------------------------------------------------------------------------------
def GetPlatformType() -> PlatformType:
	systemName : str = platform.system()
	systemName = systemName.upper()
	if systemName == "WINDOWS":
		return PlatformType.WINDOWS
	elif systemName == "DARWIN":
		return PlatformType.MACOS
	elif systemName == "LINUX":
		return PlatformType.LINUX
	else:
		return PlatformType.UNKNOWN