"""
**TensePy Databases** \n
\\@since 0.3.27a4 \\
© 2024-Present Aveyzan // License: MIT
```ts \\
module tense.databases
```
Connection with SQL. *Experimental*: not recommended to use it yet.
"""

from tense import *
from . import types_collection as tc

class _TenseSQLDataTypes(tc.Enum):
    "\\@since 0.3.27a4. Internal auxiliary enumerator class containing every date type possible to assign to columns"
    TINYINT = 0
    SMALLINT = 1
    MEDIUMINT = 2
    INT = 3
    INTEGER = 4
    BIGINT = 5
    TINYINT_UNSIGNED = 10
    SMALLINT_UNSIGNED = 11
    MEDIUMINT_UNSIGNED = 12
    INT_UNSIGNED = 13
    INTEGER_UNSIGNED = 14
    BIGINT_UNSIGNED = 15
    BOOL = 20
    BOOLEAN = 21
    DECIMAL = 30
    DEC = 31
    NUMERIC = 32
    FIXED = 33
    FLOAT = 35
    DOUBLE = 36
    DATE = 40
    DATETIME = 41
    TIMESTAMP = 42
    TIME = 43
    YEAR = 44
    CHAR = 50
    VARCHAR = 51
    BINARY = 55
    VARBINARY = 56
    TINYBLOB = 60
    BLOB = 61
    MEDIUMBLOB = 62
    LONGBLOB = 63
    TINYTEXT = 65
    TEXT = 66
    MEDIUMTEXT = 67
    LONGTEXT = 68
    ENUM = 70
    SET = 71

class _TenseSQLAdditionalOptions(tc.Enum):
    AUTO_INCREMEMT = 0
    NULL = 1
    NOT_NULL = 2
    PRIMARY_KEY = 3
    FOREIGN_KEY = 4
    KEY = 5

_DataType = _TenseSQLDataTypes
_NullType = tc.Union[bool, _TenseSQLAdditionalOptions]

def _errorMessage(code: int, v: tc.Optional[str]):
    if code == 100:
        return f"String in parameter '{v}' may only contain letters a-z, A-Z and digits 0-9."
    elif code == 101:
        return f"Expected string or None in parameter '{v}'"
    elif code == 102:
        return f"Expected integer or None in parameter '{v}'"
    elif code == 103:
        return f"Expected parameter '{v}' have positive integer value"
    else:
        return f"{v}"


class TenseSQL:
    """
    \\@since 0.3.27a4
    ```ts \\
    in module tense.databases
    ```
    Class for SQL (Structured Query Language)
    """
    from . import types_collection as __tc
    import inspect as __ins, re as __re
    __host = None
    __user = None
    __password = None
    __database = None
    __port = None
    __socket = None
    __tables = None
    def __init__(
        # reference: see PHP mysqli class constructor
        self, 
        host: __tc.Optional[str] = None, 
        user: __tc.Optional[str] = None, 
        password: __tc.Optional[str] = None, 
        database: __tc.Optional[str] = None, 
        port: __tc.Optional[int] = None, 
        socket: __tc.Optional[str] = None
    ):
        a = ("host", "user", "password", "database", "socket")
        i = 0
        for p in (host, user, password, database, socket):
            if not Tense.isString(p) and not Tense.isNone(p):
                err, s = (TypeError, _errorMessage(101, a[i]))
                raise err(s)
            i += 1
        if not Tense.isInteger(port) and not Tense.isNone(port):
            err, s = (TypeError, _errorMessage(102, "port"))
            raise err(s)
        elif port < 0:
            err, s = (ValueError, _errorMessage(103, "port"))
            raise err(s)
        i = 0
        for p in (host, user, password, database, socket):
            if Tense.isString(p):
                if self.__re.match(r"[^0-9a-zA-Z]", p):
                    err, s = (ValueError, _errorMessage(100, a[i]))
                    raise err(s)
            i += 1
        self.__host = host
        self.__user = user
        self.__password = password
        self.__database = database
        self.__port = port
        self.__socket = socket
    
    def createTable(self, name: str, /, *columns: tuple[str, tc.Union[tuple[_DataType, tc.Any]]]): ...
        
del tc
