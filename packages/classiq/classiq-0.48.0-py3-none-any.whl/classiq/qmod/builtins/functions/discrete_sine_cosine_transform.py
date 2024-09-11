from classiq.qmod.qfunc import qfunc
from classiq.qmod.qmod_variable import QArray, QBit, QNum


@qfunc(external=True)
def _qct_d_operator(x: QNum, q: QBit) -> None:
    pass


@qfunc(external=True)
def _qct_pi_operator(x: QArray[QBit], q: QBit) -> None:
    pass


@qfunc(external=True)
def qct_qst_type1(x: QArray[QBit]) -> None:
    """
    [Qmod Classiq-library function]

    Applies the quantum discrete cosine (DCT) and sine (DST)
    transform of type 1 to the qubit array `x`.
    Corresponds to the matrix (with $n\\equiv$`x.len`):

    $$
    \\left(
    \begin{array}{ccc|c}
    {} &{} &{} \\
      {}&{\rm DCT}^{(1)}(2^{n-1}+1) & {}& 0\\
      {} &{} &{} \\
      \\hline
      {} & 0 & {} & i{\rm DST}^{(1)}(2^{n-1}-1)
    \\end{array}
    \right)
    $$

    Args:
        x: The qubit array to apply the transform to.

    Links:
        - [Quantum Sine and Cosine Transforms](https://docs.classiq.io/latest/reference-manual/qmod/library-reference/open-library-functions/qct_qst/qct_qst/)
    """
    pass


@qfunc(external=True)
def qct_qst_type2(x: QArray[QBit], q: QBit) -> None:
    """
    [Qmod Classiq-library function]

    Applies the quantum discrete cosine (DCT) and sine (DST)
    transform of type 2 to the qubit array `x` concatenated with `q`, with `q` being the MSB.
    Corresponds to the matrix (with $n\\equiv$`x.len`+1):

    $$
    \\left(
    \begin{array}{c|c}
      {\rm DCT}^{(2)}(2^{n-1}) & 0\\
      \\hline
      0 & -{\rm DST}^{(2)}(2^{n-1})
    \\end{array}
    \right)
    $$

    Args:
        x: The LSB part of the qubit array to apply the transform to.
        q: The MSB of the qubit array to apply the transform to.

    Links:
        - [Quantum Sine and Cosine Transforms](https://docs.classiq.io/latest/reference-manual/qmod/library-reference/open-library-functions/qct_qst/qct_qst/)
    """
    pass


@qfunc(external=True)
def qct_type2(x: QArray[QBit]) -> None:
    """
    [Qmod Classiq-library function]

    Applies the quantum discrete cosine (DCT)
    transform of type 2, ${\rm DCT}^{(2)}$, to the qubit array `x`.

    Args:
        x: The qubit array to apply the transform to.

    Links:
        - [Quantum Sine and Cosine Transforms](https://docs.classiq.io/latest/reference-manual/qmod/library-reference/open-library-functions/qct_qst/qct_qst/)
    """
    pass


@qfunc(external=True)
def qst_type2(x: QArray[QBit]) -> None:
    """
    [Qmod Classiq-library function]

    Applies the quantum discrete sine (DST)
    transform of type 2, ${\rm DST}^{(2)}$, to the qubit array `x`.

    Args:
        x: The qubit array to apply the transform to.

    Links:
        - [Quantum Sine and Cosine Transforms](https://docs.classiq.io/latest/reference-manual/qmod/library-reference/open-library-functions/qct_qst/qct_qst/)
    """
    pass
