from enum import Enum
from typing import List, Optional

from experta import Fact, Field

from facts.components import ComponentType


class ErrorCode(Enum):
    E_1300 = 0
    E_1303 = 1
    E_1304 = 2
    E_1313 = 3
    E_1365 = 4
    E_1366 = 5
    E_1367 = 6
    E_1431 = 7
    E_1432 = 8
    E_1471 = 9
    E_1472 = 10
    E_1473 = 11
    E_1476 = 12
    E_1641 = 13
    E_1642 = 14
    E_1700 = 15
    E_1701 = 16
    E_1890 = 17
    E_2500 = 18
    E_5011 = 19
    E_5012 = 20
    E_5050 = 21
    E_5100 = 22
    E_5200 = 23
    E_5205 = 24
    E_5206 = 25
    E_5400 = 26
    E_5700 = 27
    E_5B00 = 28
    E_5B01 = 29
    E_5C02 = 30
    E_6000 = 31
    E_6001 = 32
    E_6004 = 33
    E_6500 = 34
    E_6800 = 35
    E_6801 = 36
    E_6830 = 37
    E_6831 = 38
    E_6832 = 39
    E_6833 = 41
    E_6900 = 42
    E_6901 = 43
    E_6902 = 44
    E_6910 = 45
    E_6911 = 46
    E_6920 = 47
    E_6921 = 48
    E_6930 = 49
    E_6931 = 50
    E_6932 = 51
    E_6933 = 52
    E_6936 = 53
    E_6937 = 54
    E_6938 = 55
    E_6940 = 56
    E_6941 = 57
    E_6942 = 58
    E_6943 = 59
    E_6944 = 60
    E_6945 = 61
    E_6946 = 62
    E_6A80 = 63
    E_6A81 = 64
    E_6D01 = 65
    E_7500 = 66
    E_7600 = 67
    E_7700 = 68
    E_7800 = 69
    E_C000 = 70
    E_1470 = 71  # rip bozo


class Error(Fact):
    """Represents the error returned by a device or component"""
    pass
