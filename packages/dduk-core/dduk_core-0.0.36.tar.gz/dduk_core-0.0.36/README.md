# dduk-core


## 개요
- 파이썬 dduk 라이브러리 시리즈에서 의존하는 공통 라이브러리.   


## 개발환경
- OS: Windows 10 Pro / Windows 11 Pro   
- Python: 3.12.4 (64-Bit)   
- IDE: Visual Studio Code 1.92.1 (System Setup)   
    - Korean Language Pack for Visual Studio Code   
    - Python   
    - Python Debugger   
    - Pylance   


## 배치파일
- environment.bat   
- run.bat {venv|tests|clear|build|distribution}   
- variable.bat   
- venv.bat {create|destroy|enable|disable|update}   


## 주요 기능
~~~python
# 플랫폼 검사 기능.
from dduk.core import PlatformType, GetPlatformType
platformType : PlatformType = GetPlatformType()
if platformType == PlatformType.WINDOWS:
    print("This is Windows OS")
~~~
~~~python
# 공유 객체 기능. (Singleton)
from dduk.core import SharedClass
class NewClass(SharedClass): pass
instance1 = NewClass()
instance2 = NewClass()
if instance1 == instance2:
    print("Equals Two Instances")
~~~
~~~python
# 단일 객체 저장소 기능. (Singleton)
from dduk.core import Repository
class NewClass(SharedClass): pass
instance1 = Repository.Get(NewClass) # new
instance2 = Repository.Get(NewClass) # get
if instance1 == instance2:
    print("Equals Two Instances")
~~~