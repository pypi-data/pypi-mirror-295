from guppylang.decorator import guppy
from guppylang.module import GuppyModule
from guppylang.prelude.builtins import inout
from guppylang.prelude.quantum import measure, qubit, quantum

module = GuppyModule("test")
module.load_all(quantum)


@guppy.struct(module)
class MyStruct:
    q: qubit


@guppy.declare(module)
def use(q: qubit) -> None: ...


@guppy(module)
def test(s: MyStruct @inout, b: bool) -> None:
    if b:
        use(s.q)


module.compile()
