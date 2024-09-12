from collections.abc import Sequence

from typing_extensions import TypeIs, reveal_type


def is_sequence_of_int(x: Sequence) -> TypeIs[Sequence[int]]:
    return all(isinstance(v, int) for v in x)


def f(x: Sequence[int] | Sequence[str]) -> None:
    if is_sequence_of_int(x):
        reveal_type(x)
    else:
        reveal_type(x)
