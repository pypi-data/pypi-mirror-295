"""
**TensePy Exceptions**

\\@since 0.3.27a1 \\
© 2024-Present Aveyzan // License: MIT
```ts \\
module tense._exceptions
```
Exception classes for TensePy
"""
class MissingValueError(Exception):
    """
    \\@since 0.3.19 \\
    \\@author Aveyzan
    ```ts \\
    in module tense.types_collection
    // 0.3.26b3 - 0.3.26c3 in module tense.tcs
    // to 0.3.26b3 in module tense.primary
    ```
    Missing value (empty parameter)
    """
    ...
class IncorrectValueError(Exception):
    """
    \\@since 0.3.19 \\
    \\@author Aveyzan
    ```ts \\
    in module tense.types_collection
    // 0.3.26b3 - 0.3.26c3 in module tense.tcs
    // to 0.3.26b3 in module tense.primary
    ```
    Incorrect value of a parameter, having correct type
    """
    ...
class NotInitializedError(Exception):
    """
    \\@since 0.3.25 \\
    \\@author Aveyzan
    ```ts \\
    in module tense.types_collection
    // 0.3.26b3 - 0.3.26c3 in module tense.tcs
    // to 0.3.26b3 in module tense.primary
    ```
    Class was not instantiated
    """
    ...
class InitializedError(Exception):
    """
    \\@since 0.3.26b3 \\
    \\@author Aveyzan
    ```ts \\
    in module tense.types_collection
    ```
    Class was instantiated
    """
    ...
class NotReassignableError(Exception):
    """
    \\@since 0.3.26b3 \\
    \\@author Aveyzan
    ```ts \\
    in module tense.types_collection
    ```
    Attempt to re-assign a value
    """
    ...
class NotComparableError(Exception):
    """
    \\@since 0.3.26rc1 \\
    \\@author Aveyzan
    ```ts \\
    in module tense.types_collection
    ```
    Attempt to compare a value with another one
    """
    ...
class NotIterableError(Exception):
    """
    \\@since 0.3.26rc1 \\
    \\@author Aveyzan
    ```ts \\
    in module tense.types_collection
    ```
    Attempt to iterate
    """
    ...
class NotInvocableError(Exception):
    """
    \\@since 0.3.26rc1 \\
    \\@author Aveyzan
    ```ts \\
    in module tense.types_collection
    ```
    Attempt to call an object
    """
    ...