from classiq.qmod.qfunc import qfunc
from classiq.qmod.qmod_variable import Output, QArray, QBit


@qfunc(external=True)
def swap_test(state1: QArray[QBit], state2: QArray[QBit], test: Output[QBit]) -> None:
    """
    [Qmod Classiq-library function]

    Tests the overlap (in terms of fidelity) of two quantum states.
    The fidelity of `state1` and `state2` is calculated from the probability of measuring `test` qubit in the state 0 as follows:

    $$
        |\\langle state1 | state2 \\rangle |^2 = 2*Prob(test=0)-1
    $$

    Args:
        state1: A quantum state to check its overlap with state2.
        state2: A quantum state to check its overlap with state1.
        test: A qubit for which the probability of measuring 0 is $0.5*(|\\langle state1 | state2 \\rangle |^2+1)$

    Example:
        Further reading in the Classiq library is found [here](https://docs.classiq.io/latest/explore/algorithms/swap_test/swap_test/).
    """
    pass
