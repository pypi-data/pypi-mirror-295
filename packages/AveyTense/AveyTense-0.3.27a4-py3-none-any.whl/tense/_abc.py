"""
**TensePy ABC** \n
\\@since 0.3.26rc3 \\
© 2024-Present Aveyzan // License: MIT
```ts \\
module tense._abc
```
Abstract base classes located in `tense.types_collection` module
"""

from __future__ import annotations
import sys

from . import _primal_types as pt
import collections.abc as abc2, enum, inspect as ins, zipfile as zi, tkinter as tk, subprocess as sb, types as ty, typing as tp, typing_extensions as tpe, abc, os

_pro = pt.Protocol
_var = pt.TypeVar
_con = pt.Concatenate
_uni = pt.Union
_cal = pt.Callable
_opt = pt.Optional
_par = pt.SpecVar

_T = _var("_T")
_T_sb = _var("_T_sb", str, bytes)
_T_sb_cov = _var("_T_sb_cov", str, bytes, covariant = True) # sb = str, bytes
_P = _par("_P")
_T_con = _var("_T_con", contravariant = True)
_T_cov = _var("_T_cov", covariant = True)
_T_cov2 = _var("_T_cov2", covariant = True)
_KT = _var("_KT")
_KT_cov = _var("_KT_cov", covariant = True)
_KT_con = _var("_KT_con", contravariant = True)
_VT = _var("_VT")
_VT_cov = _var("_VT_cov", covariant = True)
_T_yield_cov = _var("_T_yield_cov", covariant = True)
_T_send_con = _var("_T_send_con", contravariant = True)
_T_return_cov = _var("_T_return_cov", covariant = True)

###### ABCs REFERRED FROM collections.abc ######
# in order as in https://docs.python.org/3/library/collections.abc.html#collections-abstract-base-classes

@pt.runtime
class Containable(_pro[_T_con]):
    """
    \\@since 0.3.26rc1. [`collections.abc.Container`](https://docs.python.org/3/library/collections.abc.html#collections-abstract-base-classes)

    An ABC with one method `__contains__`, which equals invoking `value in self`. \\
    Type parameter there is contravariant, and equals type for `value` parameter.
    """
    def __contains__(self, value: _T_con) -> bool: ...

class InComparable(Containable[_T_cov]):
    """
    \\@since 0.3.26rc1. [`collections.abc.Container`](https://docs.python.org/3/library/collections.abc.html#collections-abstract-base-classes)

    Alias to `Containable`

    An ABC with one method `__contains__`, which equals invoking `value in self`. \\
    Type parameter there is contravariant, and equals type for `value` parameter.
    """
    ...

Container = InComparable[_T]
"\\@since 0.3.26rc3. *tense._abc.Container*"
ContainerAbc = abc2.Container[_T]
"\\@since 0.3.26rc3"
IterableAbc = abc2.Iterable[_T]
"\\@since 0.3.26rc3"
IteratorAbc = abc2.Iterator[_T]
"\\@since 0.3.26rc3"

@pt.runtime
class Hashable(_pro):
    """
    \\@since 0.3.26rc1. [`collections.abc.Hashable`](https://docs.python.org/3/library/collections.abc.html#collections-abstract-base-classes)

    An ABC with one method `__hash__`, which equals invoking `hash(self)`.
    """
    def __hash__(self) -> int: ...

@pt.runtime
class Iterable(_pro[_T_cov]): # type: ignore
    """
    \\@since 0.3.26b3. [`collections.abc.Iterable`](https://docs.python.org/3/library/collections.abc.html#collections-abstract-base-classes)

    An ABC with one method `__iter__`, which equals invoking `for x in self: ...`. \\
    Returned iterator type is addicted to covariant type parameter.
    """
    def __iter__(self) -> Iterator[_T_cov]: ...

class Iterator(Iterable[_T_cov]):
    """
    \\@since 0.3.26b3. [`collections.abc.Iterator`](https://docs.python.org/3/library/collections.abc.html#collections-abstract-base-classes)

    An ABC with methods `__next__` and `__iter__`: \\
    `next(self)` + `for x in self`
    """
    def __next__(self) -> _T_cov: ...

class Reversible(Iterable[_T_cov]):
    """
    \\@since 0.3.26rc2. [`collections.abc.Reversible`](https://docs.python.org/3/library/collections.abc.html#collections-abstract-base-classes)

    An ABC with one method `__reversed__`, which equals invoking `reversed(self)`. \\
    Returned type is addicted to covariant type parameter (iterator of type parameter). \\
    This ABC also inherits from `Iterable` class.
    """
    def __reversed__(self) -> Iterator[_T_cov]: ...

class Generator(abc2.Generator[_T_yield_cov, _T_send_con, _T_return_cov]):
    """
    \\@since 0.3.26rc3. [`collections.abc.Generator`](https://docs.python.org/3/library/collections.abc.html#collections-abstract-base-classes)
    """
    ...

class Coroutine(abc2.Coroutine[_T_yield_cov, _T_send_con, _T_return_cov]):
    """
    \\@since 0.3.26rc3. [`collections.abc.Coroutine`](https://docs.python.org/3/library/collections.abc.html#collections-abstract-base-classes)
    """
    ...

@pt.runtime
class Sizeable(_pro):
    """
    \\@since 0.3.26rc3. [`collections.abc.Sized`](https://docs.python.org/3/library/collections.abc.html#collections-abstract-base-classes)

    An ABC with one method `__len__`, which equals invoking `len(self)`.
    """
    def __len__(self) -> int: ...

Sized = Sizeable
"\\@since 0.3.26rc3. *tense.types_collection.Sizeable*"

@pt.runtime
class Buffer(_pro):
    """
    \\@since 0.3.26rc1. [`collections.abc.Buffer`](https://docs.python.org/3/library/collections.abc.html#collections-abstract-base-classes)

    An ABC with one method `__buffer__`.
    """
    def __buffer__(self, flags: ins.BufferFlags) -> memoryview: ...

@pt.runtime
class Invocable(_pro[_T_cov]): # self() (to prevent name conflict with typing.Callable)
    """
    \\@since 0.3.26rc1. [`collections.abc.Callable`](https://docs.python.org/3/library/collections.abc.html#collections-abstract-base-classes)

    An ABC with one method `__call__`, which equals invoking `self(...)`. \\
    Returned type is addicted to covariant type parameter.
    """
    def __call__(self, *args, **kwds) -> _T_cov: ...

class LenOperable(Sizeable):
    """
    \\@since 0.3.26rc1. [`collections.abc.Sized`](https://docs.python.org/3/library/collections.abc.html#collections-abstract-base-classes)

    An ABC with one method `__len__`, which equals invoking `len(self)`.
    """
    ...

class Sequence(abc2.Sequence[_T_cov]):
    "\\@since 0.3.26rc2. [`collections.abc.Sequence`](https://docs.python.org/3/library/collections.abc.html#collections-abstract-base-classes)"
    ...

class MutableSequence(abc2.MutableSequence[_T_cov]):
    "\\@since 0.3.26rc2. [`collections.abc.MutableSequence`](https://docs.python.org/3/library/collections.abc.html#collections-abstract-base-classes)"
    ...

class Mapping(abc2.Mapping[_KT, _VT]):
    "\\@since 0.3.26rc2. [`collections.abc.Mapping`](https://docs.python.org/3/library/collections.abc.html#collections-abstract-base-classes)"
    ...

class MutableMapping(abc2.MutableMapping[_KT, _VT]):
    "\\@since 0.3.26rc2. [`collections.abc.MutableMapping`](https://docs.python.org/3/library/collections.abc.html#collections-abstract-base-classes)"
    ...

class Uniqual(abc2.Set[_T_cov]):
    "\\@since 0.3.26rc2. [`collections.abc.Set`](https://docs.python.org/3/library/collections.abc.html#collections-abstract-base-classes)"
    ...

class MutableUniqual(abc2.MutableSet[_T_cov]):
    "\\@since 0.3.26rc2. [`collections.abc.MutableSet`](https://docs.python.org/3/library/collections.abc.html#collections-abstract-base-classes)"
    ...

###### ABCs OUTSIDE collections.abc ######
# Most of them are also undefined in _typeshed module, which is uncertain module to import at all.

@pt.runtime
class ItemGetter(_pro[_T_con, _T_cov]): # v = self[key] (type determined by _T_cov)
    """
    \\@since 0.3.26rc3

    An ABC with one method `__getitem__`. Type parameters:
    - first equals type for `key`
    - second equals returned type

    This method is invoked whether we want to get value \\
    via index notation `self[key]`, as instance of the class.
    """
    def __getitem__(self, key: _T_con, /) -> _T_cov: ...

@pt.runtime
class ClassItemGetter(_pro): # v = self[key] (not instance)
    """
    \\@since 0.3.26rc3

    An ABC with one method `__class_getitem__`. No type parameters.

    This method is invoked whether we want to get value \\
    via index notation `self[key]`, as reference to the class.
    """
    def __class_getitem__(cls, item: pt.Any, /) -> pt.GenericAlias: ...

class SizeableItemGetter(Sizeable, ItemGetter[int, _T_cov]):
    """
    \\@since 0.3.27a3

    An ABC with methods `__len__` and `__getitem__`. Type parameters:
    - first equals returned type for `__getitem__`
    """
    ...

@pt.runtime
class ItemSetter(_pro[_T_con, _T_cov]): # self[key] = value
    """
    \\@since 0.3.26rc3

    An ABC with one method `__setitem__`. Type parameters:
    - first equals type for `key`
    - second equals type for `value`

    This method is invoked whether we want to set a new value for \\
    specific item accessed by `key`, as `self[key] = value`.
    """
    def __setitem__(self, key: _T_con, value: _T_cov) -> None: ...

@pt.runtime
class ItemDeleter(_pro[_T_con]): # del self[key]
    """
    \\@since 0.3.26rc3

    An ABC with one method `__delitem__`. Type parameters:
    - first equals type for `key`

    This method is invoked whether we want to delete specific item \\
    using `del` keyword as `del self[key]`.
    """
    def __delitem__(self, key: _T_con, /) -> None: ...

@pt.runtime
class Getter(_pro[_T_cov]):
    """
    \\@since 0.3.26

    An ABC with one method `__get__`. Type parameters:
    - first equals returned type
    """
    def __get__(self, instance: object, owner: _opt[type] = None, /) -> _T_cov: ...

@pt.runtime
class Setter(_pro[_T_con]):
    """
    \\@since 0.3.27a3

    An ABC with one method `__set__`. Type parameters:
    - first equals type for `value`
    """
    def __set__(self, instance: object, value: _T_con, /) -> None: ...

class KeysProvider(ItemGetter[_KT_con, _VT_cov]):
    """
    \\@since 0.3.26

    An ABC with one method `keys`. Type parameters:
    - first equals key
    - second equals value
    """
    def keys(self) -> Iterable[_KT_con]: ...

@pt.runtime
class ItemsProvider(_pro[_KT_cov, _VT_cov]):
    """
    \\@since 0.3.26

    An ABC with one method `items`. Type parameters:
    - first equals key
    - second equals value
    """
    def items(self) -> Uniqual[tuple[_KT_cov, _VT_cov]]: ...

@pt.runtime
class BufferReleaser(_pro):
    """
    \\@since 0.3.26

    An ABC with one method `__release_buffer__`. No type parameters
    """
    def __release_buffer__(self, buffer: memoryview, /) -> None: ...

@pt.runtime
class NewArgumentsGetter(_pro[_T_cov]):
    """
    \\@since 0.3.26

    An ABC with one method `__getnewargs__`. Type parameters:
    - first equals type for returned tuple
    """
    def __getnewargs__(self) -> tuple[_T_cov]: ...

class ItemManager(
    ItemGetter[_T_con, _T_cov],
    ItemSetter[_T_con, _T_cov],
    ItemDeleter[_T_con]
):
    """
    \\@since 0.3.26rc3

    An ABC with following methods:
    - `__getitem__` - two type parameters (key type, return type)
    - `__setitem__` - two type parameters (key type, return type)
    - `__delitem__` - one type parameter (key type)
    """
    ...

class Abstract(abc.ABC):
    "\\@since 0.3.26b3. Create ABC using inheritance"
    ...

@pt.runtime
class SubclassHooker(_pro):
    """
    \\@since 0.3.26

    An ABC with one method `__subclasshook__`. No type parameters.

    Description: \\
    "Abstract classes can override this to customize `issubclass()`. \\
    This is invoked early on by `abc.ABCMeta.__subclasscheck__()`. \\
    It should return True, False or NotImplemented. If it returns \\
    NotImplemented, the normal algorithm is used. Otherwise, it \\
    overrides the normal algorithm (and the outcome is cached)."
    """
    def __subclasshook__(cls, subclass: type, /) -> bool: ...

@pt.runtime
class LengthHintProvider(_pro):
    """
    \\@since 0.3.26rc3

    An ABC with one method `__length_hint__`. No type parameters.

    This method is invoked like in case of `list` built-in, just on behalf of specific class. \\
    It should equal invoking `len(self())`, as seen for `list`: "Private method returning \\
    an estimate of `len(list(it))`". Hard to explain this method, still, this class will be kept. 
    """
    def __length_hint__(self) -> int: ...

@pt.runtime
class FSPathProvider(_pro[_T_sb_cov]):
    """
    \\@since 0.3.27a3. See also [`os.PathLike`](https://docs.python.org/3/library/os.html#os.PathLike)

    An ABC with one method `__fspath__`. Type parameter \\
    needs to be either `str` or `bytes` unrelated to both. \\
    That type is returned via this method.
    """
    def __fspath__(self) -> _T_sb_cov: ...

PathLike = os.PathLike[_T_sb]
"\\@since 0.3.26rc3. See [`os.PathLike`](https://docs.python.org/3/library/os.html#os.PathLike)"

@pt.runtime
class BytearrayConvertible(_pro):
    """
    \\@since 0.3.26rc3

    An unofficial ABC with one method `__bytearray__`, which *has* to equal invoking `bytearray(self)`. \\
    Returned list type is addicted to covariant type parameter.

    In reality there is no such magic method as `__bytearray__`, but I encourage \\
    Python working team to think about it.
    """
    def __bytearray__(self) -> bytearray: ...

@pt.runtime
class ListConvertible(_pro[_T_cov]):
    """
    \\@since 0.3.26rc3

    An unofficial ABC with one method `__list__`, which *has* to equal invoking `list(self)`. \\
    Returned list type is addicted to covariant type parameter.

    In reality there is no such magic method as `__list__`, but I encourage \\
    Python working team to think about it. Equivalent for this class will be \\
    generic ABC `SupportsList`. Since 0.3.27a3 this method is called `__tlist__`
    """
    def __tlist__(self) -> list[_T_cov]:
        "\\@since 0.3.26rc3. Return `list(self)`"
        ...

@pt.runtime
class TupleConvertible(_pro[_T_cov]):
    """
    \\@since 0.3.26rc3

    An unofficial ABC with one method `__tuple__`, which *has* to equal invoking `tuple(self)`. \\
    Returned tuple type is addicted to covariant type parameter.

    In reality there is no such magic method as `__tuple__`, but I encourage \\
    Python working team to think about it. Equivalent for this class will be \\
    generic ABC `SupportsTuple`. Since 0.3.27a3 this method is called `__ttuple__`
    """
    def __ttuple__(self) -> tuple[_T_cov, ...]:
        "\\@since 0.3.26rc3. Return `tuple(self)`"
        ...

@pt.runtime
class SetConvertible(_pro[_T_cov]):
    """
    \\@since 0.3.26rc3

    An unofficial ABC with one method `__set_init__`, which *has* to equal invoking `set(self)`. \\
    Returned set type is addicted to covariant type parameter.

    In reality there is no such magic method as `__set_init__`, but I encourage \\
    Python working team to think about it. Other suggested idea: `__se__`, since \\
    `__set__` is already in use. Since 0.3.27a3 this method is called `__tset__`
    """
    def __tset__(self) -> set[_T_cov]:
        "\\@since 0.3.26rc3. Return `set(self)`"
        ...

@pt.runtime
class ReckonOperable(_pro):
    """
    \\@since 0.3.26rc1

    An unofficial ABC with one method `__reckon__`, which equals `tense.reckon(self)`. \\
    Returned type is always an integer.
    """
    def __reckon__(self) -> int:
        """
        \\@since 0.3.26rc1

        Return `reckon(self)`.
        """
        ...

@pt.runtime
class Absolute(_pro[_T_cov]):
    """
    \\@since 0.3.26rc1

    An ABC with one method `__abs__`, which equals invoking `abs(self)`. \\
    Returned type is addicted to covariant type parameter.
    """
    def __abs__(self) -> _T_cov: ...

@pt.runtime
class Truncable(_pro[_T_cov]):
    """
    \\@since 0.3.26rc1

    An ABC with one method `__trunc__`, which equals invoking `trunc(self)`. \\
    Returned type is addicted to covariant type parameter.
    """
    def __trunc__(self) -> _T_cov: ...

@pt.runtime
class BooleanConvertible(_pro):
    """
    \\@since 0.3.26rc1

    An ABC with one method `__bool__` which equals invoking `bool(self)`. \\
    To keep accordance with Python 2, there is also method `__nonzero__`, \\
    which you are encouraged to use the same way as `__bool__`. Preferred use::

        def __bool__(self): ... # some code
        def __nonzero__(self): return self.__bool__()
    """
    def __bool__(self) -> bool: ...
    def __nonzero__(self) -> bool: ...

@pt.runtime
class IntegerConvertible(_pro):
    """
    \\@since 0.3.26rc1

    An ABC with one method `__int__`, which equals invoking `int(self)`
    """
    def __int__(self) -> int: ...

@pt.runtime
class FloatConvertible(_pro):
    """
    \\@since 0.3.26rc1

    An ABC with one method `__float__`, which equals invoking `float(self)`
    """
    def __float__(self) -> float: ...

@pt.runtime
class ComplexConvertible(_pro):
    """
    \\@since 0.3.26rc1

    An ABC with one method `__complex__`, which equals invoking `complex(self)`
    """
    def __complex__(self) -> complex: ...

@pt.runtime
class BytesConvertible(_pro):
    """
    \\@since 0.3.26rc1

    An ABC with one method `__bytes__`, which equals invoking `bytes(self)`
    """
    def __bytes__(self) ->  bytes: ...

@pt.runtime
class UnicodeRepresentable(_pro):
    """
    \\@since 0.3.26rc3

    An ABC with one method `__unicode__`, which equals invoking `unicode(self)`
    """
    def __unicode__(self) -> str: ...

@pt.runtime
class BinaryRepresentable(_pro):
    """
    \\@since 0.3.26rc1

    An ABC with one method `__bin__`, which equals invoking `bin(self)`.

    In reality there is no such magic method as `__bin__`, but I encourage \\
    Python working team to think about it.
    """
    def __bin__(self) -> str: ...

@pt.runtime
class OctalRepresentable(_pro):
    """
    \\@since 0.3.26rc1

    An ABC with one method `__oct__`, which equals invoking `oct(self)`
    """
    def __oct__(self) -> str: ...

@pt.runtime
class HexadecimalRepresentable(_pro):
    """
    \\@since 0.3.26rc1

    An ABC with one method `__hex__`, which equals invoking `hex(self)`
    """
    def __hex__(self) -> str: ...

@pt.runtime
class StringConvertible(_pro):
    """
    \\@since 0.3.26rc1

    An ABC with one method `__str__`, which equals invoking `str(self)`
    """
    def __str__(self) -> str: ...

@pt.runtime
class Representable(_pro):
    """
    \\@since 0.3.26rc1

    An ABC with one method `__repr__`, which equals invoking `repr(self)`
    """
    def __repr__(self) -> str: ...

@pt.runtime
class Indexable(_pro):
    """
    \\@since 0.3.26rc1

    An ABC with one method `__index__`. This allows to use self inside slice expressions, \\
    those are: `slice(self, ..., ...)` and `iterable[self:...:...]` (`self` can be \\
    placed anywhere)
    """
    def __index__(self) -> int: ...

@pt.runtime
class Hashable(_pro):
    """
    \\@since 0.3.26rc1

    An ABC with one method `__hash__`, which equals invoking `hash(self)`.
    """
    def __hash__(self) -> int: ...

@pt.runtime
class Positive(_pro[_T_cov]):
    """
    \\@since 0.3.26rc1

    An ABC with one method `__pos__`, which equals `+self`. \\
    Returned type is addicted to covariant type parameter.
    """
    def __pos__(self) -> _T_cov: ...

@pt.runtime
class Negative(_pro[_T_cov]):
    """
    \\@since 0.3.26rc1

    An ABC with one method `__neg__`, which equals `-self`. \\
    Returned type is addicted to covariant type parameter.
    """
    def __neg__(self) -> _T_cov: ...

@pt.runtime
class Invertible(_pro[_T_cov]):
    """
    \\@since 0.3.26rc1

    An ABC with one method `__invert__`, which equals `~self`. \\
    Returned type is addicted to covariant type parameter.
    """
    def __invert__(self) -> _T_cov: ...

BufferOperable = Buffer
"\\@since 0.3.26rc1. *tense.types_collection.abc.Buffer*"

@pt.runtime
class LeastComparable(_pro[_T_con]):
    """
    \\@since 0.3.26b3

    Can be compared with `<`
    """
    def __lt__(self, other: _T_con) -> bool: ...

@pt.runtime
class GreaterComparable(_pro[_T_con]):
    """
    \\@since 0.3.26b3

    Can be compared with `>`
    """
    def __gt__(self, other: _T_con) -> bool: ...

@pt.runtime
class LeastEqualComparable(_pro[_T_con]):
    """
    \\@since 0.3.26b3

    Can be compared with `<=`
    """
    def __le__(self, other: _T_con) -> bool: ...

@pt.runtime
class GreaterEqualComparable(_pro[_T_con]):
    """
    \\@since 0.3.26b3

    Can be compared with `>=`
    """
    def __ge__(self, other: _T_con) -> bool: ...

@pt.runtime
class EqualComparable(_pro[_T_con]):
    """
    \\@since 0.3.26rc1

    Can be compared with `==`
    """
    def __eq__(self, other: _T_con) -> bool: ...

@pt.runtime
class InequalComparable(_pro[_T_con]):
    """
    \\@since 0.3.26rc1

    Can be compared with `!=`
    """
    def __ne__(self, other: _T_con) -> bool: ...


class Comparable(
    LeastComparable[pt.Any],
    GreaterComparable[pt.Any],
    LeastEqualComparable[pt.Any],
    GreaterEqualComparable[pt.Any],
    EqualComparable[pt.Any],
    InequalComparable[pt.Any],
    InComparable[pt.Any]
):
    """
    \\@since 0.3.26b3

    An ABC supporting any form of comparison with operators \\
    `>`, `<`, `>=`, `<=`, `==`, `!=`, `in` (last 3 missing before 0.3.26rc1)
    """
    ...

class ComparableWithoutIn(
    LeastComparable[pt.Any],
    GreaterComparable[pt.Any],
    LeastEqualComparable[pt.Any],
    GreaterEqualComparable[pt.Any],
    EqualComparable[pt.Any]
):
    """
    \\@since 0.3.27a2

    An ABC same as `Comparable`, but without the `in` keyword support
    """
    ...

@pt.runtime
class BitwiseAndOperable(_pro[_T_con, _T_cov]):
    """
    \\@since 0.3.26rc1

    An ABC with one method `_And__`, which equals `self & other`. \\
    Returned type is addicted to covariant type parameter as the second \\
    type parameter; first is type for `other` parameter.
    """
    def __and__(self, other: _T_con) -> _T_cov: ...

@pt.runtime
class BitwiseOrOperable(_pro[_T_con, _T_cov]):
    """
    \\@since 0.3.26rc1

    An ABC with one method `__or__`, which equals `self | other`. \\
    Returned type is addicted to covariant type parameter as the second \\
    type parameter; first is type for `other` parameter.
    """
    def __or__(self, other: _T_con) -> _T_cov: ...

@pt.runtime
class BitwiseXorOperable(_pro[_T_con, _T_cov]):
    """
    \\@since 0.3.26rc1

    An ABC with one method `__xor__`, which equals `self ^ other`. \\
    Returned type is addicted to covariant type parameter as the second \\
    type parameter; first is type for `other` parameter.
    """
    def __xor__(self, other: _T_con) -> _T_cov: ...

@pt.runtime
class BitwiseLeftOperable(_pro[_T_con, _T_cov]):
    """
    \\@since 0.3.26rc1

    An ABC with one method `__lshift__`, which equals `self << other`. \\
    Returned type is addicted to covariant type parameter as the second \\
    type parameter; first is type for `other` parameter.
    """
    def __lshift__(self, other: _T_con) -> _T_cov: ...

@pt.runtime
class BitwiseRightOperable(_pro[_T_con, _T_cov]):
    """
    \\@since 0.3.26rc1

    An ABC with one method `__rshift__`, which equals `self >> other`. \\
    Returned type is addicted to covariant type parameter as the second \\
    type parameter; first is type for `other` parameter.
    """
    def __lshift__(self, other: _T_con) -> _T_cov: ...

class BitwiseOperable(
    BitwiseAndOperable[pt.Any, pt.Any],
    BitwiseOrOperable[pt.Any, pt.Any],
    BitwiseXorOperable[pt.Any, pt.Any],
    BitwiseLeftOperable[pt.Any, pt.Any],
    BitwiseRightOperable[pt.Any, pt.Any]
):
    """
    \\@since 0.3.26rc1

    Can be used with `&`, `|`, `^`, `<<` and `>>` operators
    """
    ...

@pt.runtime
class BitwiseAndReassignable(_pro[_T_con, _T_cov]):
    """
    \\@since 0.3.26rc1

    An ABC with one method `__iand__`, which equals `self &= other`. \\
    Returned type is addicted to covariant type parameter as the second \\
    type parameter; first is type for `other` parameter.
    """
    def __iand__(self, other: _T_con) -> _T_cov: ...

@pt.runtime
class BitwiseOrReassignable(_pro[_T_con, _T_cov]):
    """
    \\@since 0.3.26rc1

    An ABC with one method `__ior__`, which equals `self |= other`. \\
    Returned type is addicted to covariant type parameter as the second \\
    type parameter; first is type for `other` parameter.
    """
    def __ior__(self, other: _T_con) -> _T_cov: ...

@pt.runtime
class BitwiseXorReassignable(_pro[_T_con, _T_cov]):
    """
    \\@since 0.3.26rc1

    An ABC with one method `__ixor__`, which equals `self ^= other`. \\
    Returned type is addicted to covariant type parameter as the second \\
    type parameter; first is type for `other` parameter.
    """
    def __ixor__(self, other: _T_con) -> _T_cov: ...

@pt.runtime
class BitwiseLeftReassignable(_pro[_T_con, _T_cov]):
    """
    \\@since 0.3.26rc1

    An ABC with one method `__ilshift__`, which equals `self <<= other`. \\
    Returned type is addicted to covariant type parameter as the second \\
    type parameter; first is type for `other` parameter.
    """
    def __ilshift__(self, other: _T_con) -> _T_cov: ...

@pt.runtime
class BitwiseRightReassignable(_pro[_T_con, _T_cov]):
    """
    \\@since 0.3.26rc1

    An ABC with one method `__irshift__`, which equals `self >>= other`. \\
    Returned type is addicted to covariant type parameter as the second \\
    type parameter; first is type for `other` parameter.
    """
    def __irshift__(self, other: _T_con) -> _T_cov: ...

class BitwiseReassignable(
    BitwiseAndOperable[pt.Any, pt.Any],
    BitwiseOrOperable[pt.Any, pt.Any],
    BitwiseXorOperable[pt.Any, pt.Any],
    BitwiseLeftReassignable[pt.Any, pt.Any],
    BitwiseRightReassignable[pt.Any, pt.Any]):
    """
    \\@since 0.3.26rc1

    Can be used with `&=`, `|=`, `^=`, `<<=` and `>>=` operators
    """
    ...

class BitwiseCollection(
    BitwiseReassignable,
    BitwiseOperable
):
    """
    \\@since 0.3.26rc1

    Can be used with `&`, `|` and `^` operators, including their \\
    augmented forms: `&=`, `|=` and `^=`, with `~` use following::

        class Example(BitwiseCollection, Invertible[_T]): ...
    """
    ...

class UnaryOperable(Positive[pt.Any], Negative[pt.Any], Invertible[pt.Any]):
    """
    \\@since 0.3.26rc1

    Can be used with `+`, `-` and `~` operators preceding the type
    """
    ...

class Indexed(ItemGetter[_T_con, _T_cov]):
    """
    \\@since 0.3.26rc2
    
    An ABC with one method `__getitem__`, which equals `self[key]`. \\
    Returned type is addicted to covariant type parameter as the second \\
    type parameter; first is type for `key` parameter.
    """
    ...

@pt.runtime
class AsyncIterable(_pro[_T_cov]):
    """
    \\@since 0.3.26b3

    An ABC with magic method `__aiter__`. Returned type is addicted to covariant type parameter.
    """
    def __aiter__(self) -> abc2.AsyncIterator[_T_cov]: ...

@pt.runtime
class AsyncNextOperable(_pro[_T_cov]):
    """
    \\@since 0.3.26b3

    An ABC with magic method `__anext__`. Returned type must be an awaitable \\
    of type represented by covariant type parameter.
    """
    async def __anext__(self) -> abc2.Awaitable[_T_cov]: ...

@pt.runtime
class AsyncExitOperable(_pro[_T_cov]):
    """
    \\@since 0.3.26b3

    An ABC with magic method `__aexit__`. Returned type must be an awaitable \\
    of type represented by covariant type parameter.
    """
    async def __aexit__(self, exc_type: _opt[type[Exception]] = None, exc_value: _opt[Exception] = None, traceback: _opt[ty.TracebackType] = None) -> abc2.Awaitable[_T_cov]: ...

@pt.runtime
class AsyncEnterOperable(_pro[_T_cov]):
    """
    \\@since 0.3.26b3

    An ABC with magic method `__aenter__`. Returned type must be an awaitable \\
    of type represented by covariant type parameter.
    """
    async def __aenter__(self) -> abc2.Awaitable[_T_cov]: ...

@pt.runtime
class ExitOperable(_pro):
    """
    \\@since 0.3.26b3

    An ABC with magic method `__exit__`. Returned type is addicted to covariant type parameter.
    """
    def __exit__(self, exc_type: _opt[type[Exception]] = None, exc_value: _opt[Exception] = None, traceback: _opt[ty.TracebackType] = None) -> bool: ...

@pt.runtime
class EnterOperable(_pro[_T_cov]):
    """
    \\@since 0.3.26b3

    An ABC with magic method `__enter__`. Returned type is addicted to covariant type parameter.
    """
    def __enter__(self) -> _T_cov: ...

@pt.runtime
class Ceilable(_pro[_T_cov]):
    """
    \\@since 0.3.26b3

    An ABC with magic method `__ceil__`, which equals `ceil(self)`. \\
    Returned type is addicted to covariant type parameter.
    """
    def __ceil__(self) -> _T_cov: ...

@pt.runtime
class Floorable(_pro[_T_cov]):
    """
    \\@since 0.3.26b3

    An ABC with magic method `__floor__`, which equals `floor(self)`. \\
    Returned type is addicted to covariant type parameter.
    """
    def __floor__(self) -> _T_cov: ...

@pt.runtime
class Roundable(_pro[_T_cov]):
    """
    \\@since 0.3.26b3

    An ABC with magic method `__round__`, which equals `round(self)`. \\
    Returned type is addicted to covariant type parameter.
    """
    def __round__(self, ndigits: pt.Optional[int] = None) -> _T_cov: ...

@pt.runtime
class NextOperable(_pro[_T_cov]):
    """
    \\@since 0.3.26b3

    An ABC with magic method `__next__`, which equals `next(self)`. \\
    Returned type is addicted to covariant type parameter.
    """
    def __next__(self) -> _T_cov: ...

CeilOperable = Ceilable[_T]
FloorOperable = Floorable[_T]
RoundOperable = Roundable[_T]

@pt.runtime
class AdditionOperable(_pro[_T_con, _T_cov]):
    """
    \\@since 0.3.26rc1
    
    An ABC with magic method `__add__`, which equals `self + other`. \\
    Returned type is addicted to covariant type parameter as the second \\
    type parameter; first is type for `other` parameter.
    """
    def __add__(self, other: _T_con) -> _T_cov: ...

@pt.runtime
class SubtractionOperable(_pro[_T_con, _T_cov]):
    """
    \\@since 0.3.26rc1
    
    An ABC with magic method `__sub__`, which equals `self - other`. \\
    Returned type is addicted to covariant type parameter as the second \\
    type parameter; first is type for `other` parameter.
    """
    def __sub__(self, other: _T_con) -> _T_cov: ...

@pt.runtime
class MultiplicationOperable(_pro[_T_con, _T_cov]):
    """
    \\@since 0.3.26rc1
    
    An ABC with magic method `__mul__`, which equals `self * other`. \\
    Returned type is addicted to covariant type parameter as the second \\
    type parameter; first is type for `other` parameter.
    """
    def __mul__(self, other: _T_con) -> _T_cov: ...

@pt.runtime
class MatrixMultiplicationOperable(_pro[_T_con, _T_cov]):
    """
    \\@since 0.3.26rc1
    
    An ABC with magic method `__matmul__`, which equals `self @ other`. \\
    Returned type is addicted to covariant type parameter as the second \\
    type parameter; first is type for `other` parameter.
    """
    def __matmul__(self, other: _T_con) -> _T_cov: ...

@pt.runtime
class TrueDivisionOperable(_pro[_T_con, _T_cov]):
    """
    \\@since 0.3.26rc1
    
    An ABC with magic method `__truediv__`, which equals `self / other`. \\
    Returned type is addicted to covariant type parameter as the second \\
    type parameter; first is type for `other` parameter.
    """
    def __truediv__(self, other: _T_con) -> _T_cov: ...

@pt.runtime
class FloorDivisionOperable(_pro[_T_con, _T_cov]):
    """
    \\@since 0.3.26rc1
    
    An ABC with magic method `__floordiv__`, which equals `self // other`. \\
    Returned type is addicted to covariant type parameter as the second \\
    type parameter; first is type for `other` parameter.
    """
    def __floordiv__(self, other: _T_con) -> _T_cov: ...

@pt.runtime
class DivmodOperable(_pro[_T_con, _T_cov]):
    """
    \\@since 0.3.26rc1
    
    An ABC with magic method `__divmod__`, which equals `divmod(self, other)`. \\
    Returned type is addicted to covariant type parameter as the second type parameter \\
    first is type for `other` parameter.
    """
    def __divmod__(self, other: _T_con) -> _T_cov: ...

@pt.runtime
class ModuloOperable(_pro[_T_con, _T_cov]):
    """
    \\@since 0.3.26rc1
    
    An ABC with magic method `__mod__`, which equals `self % other`. \\
    Returned type is addicted to covariant type parameter as the second \\
    type parameter; first is type for `other` parameter.
    """
    def __mod__(self, other: _T_con) -> _T_cov: ...

@pt.runtime
class ExponentiationOperable(_pro[_T_con, _T_cov]):
    """
    \\@since 0.3.26rc1
    
    An ABC with magic method `__pow__`, which equals `self ** other`. \\
    Returned type is addicted to covariant type parameter as the second \\
    type parameter; first is type for `other` parameter.
    """
    def __pow__(self, other: _T_con) -> _T_cov: ...

@pt.runtime
class ReflectedAdditionOperable(_pro[_T_con, _T_cov]):
    """
    \\@since 0.3.26rc1
    
    An ABC with magic method `__radd__`, which equals `other + self`. \\
    Returned type is addicted to covariant type parameter as the second \\
    type parameter; first is type for `other` parameter.
    """
    def __radd__(self, other: _T_con) -> _T_cov: ...

@pt.runtime
class ReflectedSubtractionOperable(_pro[_T_con, _T_cov]):
    """
    \\@since 0.3.26rc1
    
    An ABC with magic method `__rsub__`, which equals `other - self`. \\
    Returned type is addicted to covariant type parameter as the second \\
    type parameter; first is type for `other` parameter.
    """
    def __rsub__(self, other: _T_con) -> _T_cov: ...

@pt.runtime
class ReflectedMultiplicationOperable(_pro[_T_con, _T_cov]):
    """
    \\@since 0.3.26rc1
    
    An ABC with magic method `__rmul__`, which equals `other * self`. \\
    Returned type is addicted to covariant type parameter as the second \\
    type parameter; first is type for `other` parameter.
    """
    def __rmul__(self, other: _T_con) -> _T_cov: ...

@pt.runtime
class ReflectedMatrixMultiplicationOperable(_pro[_T_con, _T_cov]):
    """
    \\@since 0.3.26rc1
    
    An ABC with magic method `__rmatmul__`, which equals `other @ self`. \\
    Returned type is addicted to covariant type parameter as the second \\
    type parameter; first is type for `other` parameter.
    """
    def __rmatmul__(self, other: _T_con) -> _T_cov: ...

@pt.runtime
class ReflectedTrueDivisionOperable(_pro[_T_con, _T_cov]):
    """
    \\@since 0.3.26rc1
    
    An ABC with magic method `__rtruediv__`, which equals `other / self`. \\
    Returned type is addicted to covariant type parameter as the second \\
    type parameter; first is type for `other` parameter.
    """
    def __rtruediv__(self, other: _T_con) -> _T_cov: ...

@pt.runtime
class ReflectedFloorDivisionOperable(_pro[_T_con, _T_cov]):
    """
    \\@since 0.3.26rc1
    
    An ABC with magic method `__rfloordiv__`, which equals `other // self`. \\
    Returned type is addicted to covariant type parameter as the second \\
    type parameter; first is type for `other` parameter.
    """
    def __rfloordiv__(self, other: _T_con) -> _T_cov: ...

@pt.runtime
class ReflectedDivmodOperable(_pro[_T_con, _T_cov]):
    """
    \\@since 0.3.26rc1
    
    An ABC with magic method `__rdivmod__`, which equals `divmod(other, self)`. \\
    Returned type is addicted to covariant type parameter as the second type parameter; \\
    first is type for `other` parameter.
    """
    def __rdivmod__(self, other: _T_con) -> _T_cov: ...

@pt.runtime
class ReflectedModuloOperable(_pro[_T_con, _T_cov]):
    """
    \\@since 0.3.26rc1
    
    An ABC with magic method `__rmod__`, which equals `other % self`. \\
    Returned type is addicted to covariant type parameter as the second \\
    type parameter; first is type for `other` parameter.
    """
    def __rmod__(self, other: _T_con) -> _T_cov: ...

@pt.runtime
class ReflectedExponentiationOperable(_pro[_T_con, _T_cov]):
    """
    \\@since 0.3.26rc1
    
    An ABC with magic method `__rpow__`, which equals `other ** self`. \\
    Returned type is addicted to covariant type parameter as the second \\
    type parameter; first is type for `other` parameter.
    """
    def __rpow__(self, other: _T_con) -> _T_cov: ...

@pt.runtime
class AdditionReassignable(_pro[_T_con, _T_cov]):
    """
    \\@since 0.3.26rc1
    
    An ABC with magic method `__iadd__`, which equals `self += other`. \\
    Returned type is addicted to covariant type parameter as the second \\
    type parameter; first is type for `other` parameter.
    """
    def __iadd__(self, other: _T_con) -> _T_cov: ...

@pt.runtime
class SubtractionReassignable(_pro[_T_con, _T_cov]):
    """
    \\@since 0.3.26rc1
    
    An ABC with magic method `__isub__`, which equals `self -= other`. \\
    Returned type is addicted to covariant type parameter as the second \\
    type parameter; first is type for `other` parameter.
    """
    def __isub__(self, other: _T_con) -> _T_cov: ...

@pt.runtime
class MultiplicationReassignable(_pro[_T_con, _T_cov]):
    """
    \\@since 0.3.26rc1
    
    An ABC with magic method `__imul__`, which equals `self *= other`. \\
    Returned type is addicted to covariant type parameter as the second \\
    type parameter; first is type for `other` parameter.
    """
    def __imul__(self, other: _T_con) -> _T_cov: ...

@pt.runtime
class MatrixMultiplicationReassignable(_pro[_T_con, _T_cov]):
    """
    \\@since 0.3.26rc1
    
    An ABC with magic method `__imatmul__`, which equals `self @= other`. \\
    Returned type is addicted to covariant type parameter as the second \\
    type parameter; first is type for `other` parameter.
    """
    def __imatmul__(self, other: _T_con) -> _T_cov: ...

@pt.runtime
class TrueDivisionReassingable(_pro[_T_con, _T_cov]):
    """
    \\@since 0.3.26rc1
    
    An ABC with magic method `__itruediv__`, which equals `self /= other`. \\
    Returned type is addicted to covariant type parameter as the second \\
    type parameter; first is type for `other` parameter.
    """
    def __itruediv__(self, other: _T_con) -> _T_cov: ...

@pt.runtime
class FloorDivisionReassignable(_pro[_T_con, _T_cov]):
    """
    \\@since 0.3.26rc1
    
    An ABC with magic method `__ifloordiv__`, which equals `self //= other`. \\
    Returned type is addicted to covariant type parameter as the second \\
    type parameter; first is type for `other` parameter.
    """
    def __ifloordiv__(self, other: _T_con) -> _T_cov: ...

@pt.runtime
class ModuloReassignable(_pro[_T_con, _T_cov]):
    """
    \\@since 0.3.26rc1
    
    An ABC with magic method `__imod__`, which equals `self %= other`. \\
    Returned type is addicted to covariant type parameter as the second \\
    type parameter; first is type for `other` parameter.
    """
    def __imod__(self, other: _T_con) -> _T_cov: ...

@pt.runtime
class ExponentiationReassignable(_pro[_T_con, _T_cov]):
    """
    \\@since 0.3.26rc1
    
    An ABC with magic method `__ipow__`, which equals `self **= other`. \\
    Returned type is addicted to covariant type parameter as the second \\
    type parameter; first is type for `other` parameter.
    """
    def __ipow__(self, other: _T_con) -> _T_cov: ...

class ReflectedArithmeticOperable(
    ReflectedAdditionOperable[pt.Any, pt.Any],
    ReflectedSubtractionOperable[pt.Any, pt.Any],
    ReflectedMultiplicationOperable[pt.Any, pt.Any],
    ReflectedMatrixMultiplicationOperable[pt.Any, pt.Any],
    ReflectedTrueDivisionOperable[pt.Any, pt.Any],
    ReflectedFloorDivisionOperable[pt.Any, pt.Any],
    ReflectedDivmodOperable[pt.Any, pt.Any],
    ReflectedModuloOperable[pt.Any, pt.Any]
):
    """
    \\@since 0.3.26rc1

    An ABC supporting every kind (except bitwise) of reflected arithmetic operations with following operators:
    ```py \\
        + - * @ / // % ** divmod
    ```
    where left operand is `other` and right is `self`
    """
    ...

class ArithmeticOperable(
    AdditionOperable[pt.Any, pt.Any],
    SubtractionOperable[pt.Any, pt.Any],
    MultiplicationOperable[pt.Any, pt.Any],
    MatrixMultiplicationOperable[pt.Any, pt.Any],
    TrueDivisionOperable[pt.Any, pt.Any],
    FloorDivisionOperable[pt.Any, pt.Any],
    DivmodOperable[pt.Any, pt.Any],
    ModuloOperable[pt.Any, pt.Any],
    ExponentiationOperable[pt.Any, pt.Any],
    ReflectedArithmeticOperable
):
    """
    \\@since 0.3.26rc1

    An ABC supporting every kind (except bitwise) of arithmetic operations, including their \\
    reflected equivalents, with following operators:
    ```py \\
        + - * @ / // % ** divmod
    ```
    Both `self` and `other` can be either left or right operands.
    """
    ...

class ArithmeticReassignable(
    AdditionReassignable[pt.Any, pt.Any],
    SubtractionReassignable[pt.Any, pt.Any],
    MultiplicationReassignable[pt.Any, pt.Any],
    MatrixMultiplicationReassignable[pt.Any, pt.Any],
    TrueDivisionReassingable[pt.Any, pt.Any],
    FloorDivisionReassignable[pt.Any, pt.Any],
    ModuloReassignable[pt.Any, pt.Any],
    ExponentiationReassignable[pt.Any, pt.Any]
):
    """
    \\@since 0.3.26rc1

    An ABC supporting every kind (except bitwise) of augmented/re-assigned arithmetic operations \\
    with following operators:
    ```py \\
        += -= *= @= /= //= %= **=
    ```
    """
    ...

class ArithmeticCollection(
    ArithmeticOperable,
    ArithmeticReassignable
):
    """
    \\@since 0.3.26rc1

    An ABC supporting every kind (except bitwise) of augmented/re-assigned and normal arithmetic operations \\
    with following operators:
    ```py \\
        + - * @ / // % ** divmod += -= *= @= /= //= %= **=
    ```
    """
    ...

class OperatorCollection(
    ArithmeticCollection,
    BitwiseCollection,
    UnaryOperable,
    Comparable
):
    """
    \\@since 0.3.26rc1

    An ABC supporting every kind of augmented/re-assigned, reflected and normal arithmetic operations \\
    with following operators:
    ```py \\
        + - * @ / // % ** divmod & | ^ += -= *= @= /= //= %= **= &= |= ^=
    ```
    unary assignment with `+`, `-` and `~`, and comparison with following operators:
    ```py \\
        > < >= <= == != in
    ```
    """
    ...

if SizeableItemGetter is None:
    try:
        import _typeshed as shed
        class LenGetItemOperable(shed.SupportsLenAndGetItem[_T_cov]):
            """
            \\@since 0.3.26rc2
            
            An ABC with `__getitem__` and `__len__` methods. Those are typical in sequences.
            """
            ...
    except:
        class LenGetItemOperable(LenOperable, ItemGetter[int, _T_cov]):
            """
            \\@since 0.3.26rc2
            
            An ABC with `__getitem__` and `__len__` methods. Those are typical in sequences.
            """
            ...
    
@pt.runtime
class Formattable(_pro):
    """
    \\@since 0.3.26rc1

    An ABC with one method `__format__`, which equals invoking `format(self)`.
    """
    def __format__(self, format_spec: str = "") -> str: ...

del abc2, pt, ins, sb, tk, zi, enum, ty, tp, tpe, abc, os