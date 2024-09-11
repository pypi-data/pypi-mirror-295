from classiq.qmod.qfunc import qfunc
from classiq.qmod.qmod_parameter import CInt
from classiq.qmod.qmod_variable import QNum
from classiq.qmod.quantum_callable import QCallable


@qfunc(external=True)
def qpe_flexible(unitary_with_power: QCallable[CInt], phase: QNum) -> None:
    """
    [Qmod Classiq-library function]

    Implements the Quantum Phase Estimation (QPE) algorithm,  which estimates the phase (eigenvalue) associated with an eigenstate of a given unitary operator $U$.
    This is a flexible version that allows the user to provide a callable that generates the unitary operator $U^k$ for a given integer $k$, offering greater flexibility in handling different quantum circuits using some powering rule.

    Args:
        unitary_with_power: A callable that returns the unitary operator $U^k$ given an integer $k$. This callable is used to control the application of powers of the unitary operator.
        phase: The quantum variable that represents the estimated phase (eigenvalue), assuming initialized to zero.

    Further reading in Classiq Library:
    Link: [qpe library reference](https://github.com/Classiq/classiq-library/blob/main/functions/qmod_library_reference/classiq_open_library/qpe/qpe.ipynb)
    """
    pass


@qfunc(external=True)
def qpe(unitary: QCallable, phase: QNum) -> None:
    """
    [Qmod Classiq-library function]

    Implements the standard Quantum Phase Estimation (QPE) algorithm, which estimates the phase (eigenvalue) associated with an eigenstate of a given unitary operator $U$.

    Args:
        unitary: A callable representing the unitary operator $U$, whose eigenvalue is to be estimated.
        phase: The quantum variable that represents the estimated phase (eigenvalue), assuming initialized to zero.

    Further reading in Classiq Library:
    Link: [qpe library reference](https://github.com/Classiq/classiq-library/blob/main/functions/qmod_library_reference/classiq_open_library/qpe/qpe.ipynb)
    """
    pass
