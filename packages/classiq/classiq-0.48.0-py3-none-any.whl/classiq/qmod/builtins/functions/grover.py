from typing_extensions import Annotated

from classiq.qmod.qfunc import qfunc
from classiq.qmod.qmod_parameter import CInt
from classiq.qmod.qmod_variable import QArray, QBit
from classiq.qmod.quantum_callable import QCallable


@qfunc(external=True)
def phase_oracle(
    predicate: QCallable[QArray[QBit], QBit], target: QArray[QBit]
) -> None:
    """
    [Qmod Classiq-library function]

    Creates a phase oracle operator based on a predicate function.

    Applies a predicate function and marks "good" and "bad" states with a phase flip.
    If the predicate is marked as $\\chi$, and the oracle is marked as $S_\\chi$, then:


    $$
    S_\\chi\\lvert x \rangle =
    \begin{cases}
    -\\lvert x \rangle & \text{if } \\chi(x) = 1 \\
     \\phantom{-} \\lvert x \rangle & \text{if } \\chi(x) = 0
    \\end{cases}
    $$

    Args:
        predicate: A predicate function that takes a QArray of QBits and sets a single QBit |1> if the predicate is true, and |0> otherwise.
        target: The target QArray of QBits to apply the phase oracle to.

    Usage Examples:
        [Grover Algorithm](https://docs.classiq.io/latest/explore/functions/qmod_library_reference/classiq_open_library/grover_operator/grover_operator/)

        [Hidden shift](https://docs.classiq.io/latest/explore/algorithms/algebraic/hidden_shift/hidden_shift/)
    """
    pass


@qfunc(external=True)
def reflect_about_zero(packed_vars: QArray[QBit]) -> None:
    """
    [Qmod Classiq-library function]

    Reflects the state about the |0> state (i.e. applies a (-1) phase to all states
    besides the |0> state). Implements the operator $S_0$:

    $$
    \begin{equation}
    S_0|{x}\rangle = (-1)^{(x\ne0)}|{x}\rangle= (2|{0}\rangle\\langle{0}|-I)|{x}\rangle
    \\end{equation}
    $$

    Args:
        packed_vars: The quantum state to reflect.
    """
    pass


@qfunc(external=True)
def grover_diffuser(
    space_transform: QCallable[QArray[QBit]], packed_vars: QArray[QBit]
) -> None:
    """
    [Qmod Classiq-library function]

    Reflects the given state about the A|0> state, where A
    is the `space_transform` parameter. It is defined as:

    $$
    \begin{equation}
    D = A S_0 A^{\\dagger}
    \\end{equation}
    $$

    where $S_0$ is the reflection about the |0> state (see `reflect_about_zero`).

    Args:
        space_transform: The operator which encodes the axis of reflection.
        packed_vars: The state to which to apply the diffuser.
    """
    pass


@qfunc(external=True)
def grover_operator(
    oracle: QCallable[QArray[QBit]],
    space_transform: QCallable[QArray[QBit]],
    packed_vars: QArray[QBit],
) -> None:
    """
    [Qmod Classiq-library function]

    Applies the grover operator, defined by:

    $$
    Q=S_{\\psi_0}S_{\\psi_1}
    $$

    where $S_{\\psi_1}$ is a reflection about marked states, and $S_{\\psi_0}$ is a reflection
    about a given state defined by $|\\psi_0\rangle = A|0\rangle$.


    Args:
        oracle: A unitary operator which adds a phase of (-1) to marked states.
        space_transform: The operator which creates $|\\psi_0\rangle$, the initial state, used by the diffuser to reflect about it.
        packed_vars: The state to which to apply the grover operator.


    For further reading, see:

    - [The Grover Operator notebook](../explore/functions/qmod_library_reference/classiq_open_library/grover_operator/grover_operator/)
    - [Wikipedia page](https://en.wikipedia.org/wiki/Grover%27s_algorithm).

    """
    pass


@qfunc(external=True)
def grover_search(
    reps: CInt, oracle: QCallable[QArray[QBit]], packed_vars: QArray[QBit]
) -> None:
    """
    [Qmod Classiq-library function]

    Applies Grover search algorithm.

    Args:
        reps: Number of repetitions of the grover operator.
        oracle: An oracle that marks the solution.
        packed_vars: Packed form of the variable to apply the grover operator on.

    Returns: None

    Links:
         [Grover Algorithm](https://docs.classiq.io/latest/explore/functions/qmod_library_reference/classiq_open_library/grover_operator/grover_operator/)

    """
    pass


@qfunc(external=True)
def hadamard_transform(target: QArray[QBit]) -> None:
    """
    [Qmod Classiq-library function]

    Applies Hadamard transform to the target qubits.

    Corresponds to the braket notation:

    $$
     H^{\\otimes n} |x\rangle = \frac{1}{\\sqrt{2^n}} \\sum_{y=0}^{2^n - 1} (-1)^{x \\cdot y} |y\rangle
    $$

    Args:
        target:  qubits to apply to Hadamard transform to.

    """
    pass


@qfunc(external=True)
def apply_to_all(
    gate_operand: QCallable[Annotated[QBit, "target"]], target: QArray[QBit]
) -> None:
    """
    [Qmod Classiq-library function]

    Applies the single-qubit operand `gate_operand` to each qubit in the qubit
    array `target`.

    Args:
        gate_operand: The single-qubit gate to apply to each qubit in the array.
        target: The qubit array to apply the gate to.
    """
    pass
