"""Various tests for the functions defined in `guppylang.prelude.quantum`."""

import pytest

from hugr.ext import Package

import guppylang.decorator
from guppylang.decorator import guppy
from guppylang.module import GuppyModule
from guppylang.prelude.angles import angle

from guppylang.prelude.builtins import py
import guppylang.prelude.quantum as quantum
from guppylang.prelude.quantum import (
    cx,
    cz,
    h,
    t,
    s,
    x,
    y,
    z,
    tdg,
    sdg,
    zz_max,
    phased_x,
    qubit,
    rx,
    rz,
    zz_phase,
    discard,
    measure,
    measure_return,
    dirty_qubit,
    reset,
)


def compile_quantum_guppy(fn) -> Package:
    """A decorator that combines @guppy with HUGR compilation.

    Modified version of `tests.util.compile_guppy` that loads the quantum module.
    """
    assert not isinstance(
        fn,
        GuppyModule,
    ), "`@compile_quantum_guppy` does not support extra arguments."

    module = GuppyModule("module")
    module.load(angle)
    module.load_all(quantum)
    guppylang.decorator.guppy(module)(fn)
    return module.compile()


def test_dirty_qubit(validate):
    @compile_quantum_guppy
    def test() -> tuple[bool, bool]:
        q1, q2 = qubit(), dirty_qubit()
        q1, q2 = cx(q1, q2)
        return (measure(q1), measure(q2))

    validate(test)


def test_1qb_op(validate):
    @compile_quantum_guppy
    def test(q: qubit) -> qubit:
        q = h(q)
        q = t(q)
        q = s(q)
        q = x(q)
        q = y(q)
        q = z(q)
        q = tdg(q)
        q = sdg(q)
        return q

    validate(test)


def test_2qb_op(validate):
    @compile_quantum_guppy
    def test(q1: qubit, q2: qubit) -> tuple[qubit, qubit]:
        q1, q2 = cx(q1, q2)
        q1, q2 = cz(q1, q2)
        q1, q2 = zz_max(q1, q2)
        return (q1, q2)

    validate(test)


def test_measure_ops(validate):
    """Compile various measurement-related operations."""

    @compile_quantum_guppy
    def test(q1: qubit, q2: qubit) -> tuple[bool, bool]:
        q1, b1 = measure_return(q1)
        q1 = discard(q1)
        q2 = reset(q2)
        b2 = measure(q2)
        return (b1, b2)

    validate(test)


def test_parametric(validate):
    """Compile various parametric operations."""

    @compile_quantum_guppy
    def test(q1: qubit, q2: qubit, a1: angle, a2: angle) -> tuple[qubit, qubit]:
        q1 = rx(q1, a1)
        q2 = rz(q2, a2)
        q1 = phased_x(q1, a1, a2)
        q1, q2 = zz_phase(q1, q2, a1)
        return (q1, q2)
