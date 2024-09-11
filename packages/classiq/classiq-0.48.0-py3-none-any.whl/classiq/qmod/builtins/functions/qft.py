from classiq.qmod.qfunc import qfunc
from classiq.qmod.qmod_variable import QArray, QBit


@qfunc(external=True)
def qft(target: QArray[QBit]) -> None:
    """
    [Qmod Classiq-library function]

    Performs the Quantum Fourier Transform (QFT) on `target` in-place.
    Implements the following transformation:

    $$
    y_{k} = \\frac{1}{\\sqrt{N}} \\sum_{j=0}^{N-1} x_j e^{2\\pi i \\frac{jk}{N}}
    $$

    Args:
        target: The quantum object to be transformed

    Further reading in Classiq Library:
    Link: [qft library reference](https://github.com/Classiq/classiq-library/blob/main/functions/qmod_library_reference/classiq_open_library/qft/qft.ipynb)
    """
    pass
