from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar, Union, final

if TYPE_CHECKING:
    from typing import Final, Literal, TypeAlias

__all__: tuple[str, ...] = (
    "Optional",
    "Undefined",
    "UndefinedType",
)

T = TypeVar("T")


@final
class UndefinedType:
    __slots__: tuple[str, ...] = ()

    def __repr__(self) -> Literal["Undefined"]:
        return "Undefined"

    def __hash__(self) -> Literal[0xDEADBEEF]:
        return 0xDEADBEEF

    def __bool__(self) -> Literal[False]:
        return False


Undefined: Final[UndefinedType] = UndefinedType()
Optional: TypeAlias = Union[T, UndefinedType]
