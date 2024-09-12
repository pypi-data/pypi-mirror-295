#--------------------------------------------------------------------------------
# 참조 모듈 목록.
#--------------------------------------------------------------------------------
from __future__ import annotations
from typing import Any, Final, Callable, Iterator, Optional, Type, TypeVar, Union, Tuple, List, Dict, Set, cast
import builtins
import os
import setuptools


#--------------------------------------------------------------------------------
# 상수 목록.
#--------------------------------------------------------------------------------
UTF8 : str = "utf-8"
READ : str = "r"


#--------------------------------------------------------------------------------
# 참조 메타 데이터 목록.
#--------------------------------------------------------------------------------
NAME : str = "dduk-core"
VERSION : str = "0.0.39" # 접두어 v 붙여도 알아서 정규화하면서 제거됨.
AUTHOR : str = "ddukbaek2"
AUTHOR_EMAIL : str = "ddukbaek2@gmail.com"
DESCRIPTION : str = "ddukbaek2 core library"
LONG_DESCRIPTION_CONTENT_TYPE : str = "text/markdown"
URL : str = "https://ddukbaek2.com"
PYTHON_REQUIRES : str = ">=3.7"
LONGDESCRIPTION : str = str()
with open(file = "README.md", mode = READ, encoding = UTF8) as file: LONGDESCRIPTION = file.read()


#--------------------------------------------------------------------------------
# 빌드.
#--------------------------------------------------------------------------------
setuptools.setup(
	name = NAME,
	version = VERSION,
	author = AUTHOR,
	author_email = AUTHOR_EMAIL,
	description = DESCRIPTION,
	long_description = LONGDESCRIPTION,
	long_description_content_type = LONG_DESCRIPTION_CONTENT_TYPE,
	url = URL,
	packages = setuptools.find_packages(where = "src"),
	include_package_data = True,
	package_dir = { "": "src" },
	package_data = {
		"": [
			"res/*"
		],
	},
	scripts = [

	],
	entry_points = {
		"console_scripts": [
			# "dduk-core=dduk.core.commands:Command"
		]
	},
	install_requires = [
	],
	classifiers = [
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent"
	],
	python_requires = PYTHON_REQUIRES
)