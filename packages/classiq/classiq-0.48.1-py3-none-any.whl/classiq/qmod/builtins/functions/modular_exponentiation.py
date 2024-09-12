from classiq.qmod.qfunc import qfunc
from classiq.qmod.qmod_parameter import CInt
from classiq.qmod.qmod_variable import QArray, QBit, QNum


@qfunc(external=True)
def qft_no_swap(qbv: QArray[QBit]) -> None:
    """
    [Qmod Classiq-library function]

    Applies the Quantum Fourier Transform (QFT) without the swap gates.

    Args:
        qbv: The quantum number to which the QFT is applied.

    """
    pass


@qfunc(external=True)
def _check_msb(ref: CInt, x: QArray[QBit], aux: QBit) -> None:
    pass


@qfunc(external=True)
def _ctrl_x(ref: CInt, ctrl: QNum, aux: QBit) -> None:
    pass


@qfunc(external=True)
def qft_space_add_const(value: CInt, phi_b: QArray[QBit]) -> None:
    """
    [Qmod Classiq-library function]

    Adds a constant to a quantum number (in the Fourier space) using the Quantum Fourier Transform (QFT) Adder algorithm.
    Assuming that the input `phi_b` has `n` qubits, the result will be $\\phi_b+=value \\mod 2^n$.

    To perform the full algorithm, use:
    within_apply(lambda: QFT(phi_b), qft_space_add_const(value, phi_b))

    Args:
        value: The constant to add to the quantum number.
        phi_b: The quantum number (at the aft space) to which the constant is added.

    """
    pass


@qfunc(external=True)
def cc_modular_add(n: CInt, a: CInt, phi_b: QArray[QBit], c1: QBit, c2: QBit) -> None:
    """
    [Qmod Classiq-library function]

    Adds a constant `a` to a quantum number `phi_b` modulo the constant `n`, controlled by 2 qubits.
    The quantum number `phi_b` and the constant `a` are assumed to be in the QFT space.

    Args:
        n: The modulo number.
        a: The constant to add to the quantum number.
        phi_b: The quantum number to which the constant is added.
        c1: a control qubit.
        c2: a control qubit.

    """
    pass


@qfunc(external=True)
def c_modular_multiply(
    n: CInt, a: CInt, b: QArray[QBit], x: QArray[QBit], ctrl: QBit
) -> None:
    """
    [Qmod Classiq-library function]

    Performs out-of-place multiplication of a quantum number `x` by a classical number `a` modulo classical number `n`,
    controlled by a quantum bit `ctrl` and adds the result to a quantum array `b`. Applies $b += xa \\mod n$ if `ctrl=1`, and the identity otherwise.

    Args:
        n: The modulo number. Should be non-negative.
        a: The classical factor. Should be non-negative.
        b: The quantum number added to the multiplication result. Stores the result of the multiplication.
        x: The quantum factor.
        ctrl: The control bit.
    """
    pass


@qfunc(external=True)
def multiswap(x: QArray[QBit], y: QArray[QBit]) -> None:
    """
    [Qmod Classiq-library function]

    Swaps the qubit states between two arrays.
    Qubits of respective indices are swapped, and additional qubits in the longer array are left unchanged.

    Args:
        x: The first array
        y: The second array

    """
    pass


@qfunc(external=True)
def inplace_c_modular_multiply(n: CInt, a: CInt, x: QArray[QBit], ctrl: QBit) -> None:
    """
    [Qmod Classiq-library function]

    Performs multiplication of a quantum number `x` by a classical number `a` modulo classical number `n`,
    controlled by a quantum bit `ctrl`. Applies $x=xa \\mod n$ if `ctrl=1`, and the identity otherwise.

    Args:
        n: The modulo number. Should be non-negative.
        a: The classical factor. Should be non-negative.
        x: The quantum factor.
        ctrl: The control bit.
    """
    pass


@qfunc(external=True)
def modular_exp(n: CInt, a: CInt, x: QArray[QBit], power: QArray[QBit]) -> None:
    """
    [Qmod Classiq-library function]

    Raises a classical integer `a` to the power of a quantum number `x` modulo classical integer `n`
    times a quantum number `power`. Performs $power=(a^x \\mod n)*power$ in-place.
    (and specifically if at the input $power=1$, at the output $power=a^x \\mod n$).

    Args:
        n: The modulus number. Should be non-negative.
        a: The base of the exponentiation. Should be non-negative.
        x: The power of the exponentiation.
        power: A quantum number which multiplies the modular exponentiation and holds the output.

    """
    pass
