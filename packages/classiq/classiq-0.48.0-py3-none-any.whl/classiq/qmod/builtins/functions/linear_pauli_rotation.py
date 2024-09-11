from typing_extensions import Annotated

from classiq.qmod.builtins.enums import Pauli
from classiq.qmod.qfunc import qfunc
from classiq.qmod.qmod_parameter import CArray, CReal
from classiq.qmod.qmod_variable import QArray, QBit
from classiq.qmod.quantum_callable import QCallable


@qfunc(external=True)
def _single_pauli(
    slope: CReal,
    offset: CReal,
    q1_qfunc: QCallable[Annotated[CReal, "theta"], Annotated[QBit, "target"]],
    x: QArray[QBit],
    q: QBit,
) -> None:
    pass


@qfunc(external=True)
def linear_pauli_rotations(
    bases: CArray[Pauli],
    slopes: CArray[CReal],
    offsets: CArray[CReal],
    x: QArray[QBit],
    q: QArray[QBit],
) -> None:
    """
    [Qmod Classiq-library function]

    Performs a rotation on a series of $m$ target qubits,
    where the rotation angle is a linear function of an $n$-qubit
    control register.

    Corresponds to the braket notation:

    $$
    \\left|x\right\rangle _{n}\\left|q\right\rangle
    _{m}\rightarrow\\left|x\right\rangle
    _{n}\\prod_{k=1}^{m}\\left(\\cos\\left(\frac{a_{k}}{2}x+\frac{b_{k}}{2}\right)-
    i\\sin\\left(\frac{a_{k}}{2}x+\frac{b_{k}}{2}\right)P_{k}\right)\\left|q_{k}\right\rangle
    $$

    where $\\left|x\right\rangle$ is the control register,
    $\\left|q\right\rangle$ is the target register, each $P_{k}$ is one of
    the three Pauli matrices $X$, $Y$, or $Z$, and $a_{k}$, $b_{k}$ are
    the user given slopes and offsets, respectively.

    Args:
        bases: List of Pauli Enums.
        slopes: Rotation slopes for each of the given Pauli bases.
        offsets:  Rotation offsets for each of the given Pauli bases.
        x: Quantum state to apply the rotation based on its value.
        q: List of indicator qubits for each of the given Pauli bases.

    Notice that bases, slopes, offset and q should be of the same size.



    Links:
       [linear_pauli_rotations](https://docs.classiq.io/latest/explore/functions/qmod_library_reference/classiq_open_library/linear_pauli_rotations/linear_pauli_rotations)
    """

    pass
