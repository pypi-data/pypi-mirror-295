from guppylang.decorator import guppy
from guppylang.module import GuppyModule
from guppylang.prelude.builtins import inout
from guppylang.prelude.quantum import measure, qubit, quantum

module = GuppyModule("test")
module.load_all(quantum)


@guppy.declare(module)
def foo(q1: qubit @inout) -> None: ...


@guppy.declare(module)
def use(q: qubit) -> None: ...


@guppy(module)
def test(q: qubit @inout) -> None:
    foo(q)
    use(q)


module.compile()
