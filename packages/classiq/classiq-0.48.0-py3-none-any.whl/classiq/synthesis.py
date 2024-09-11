from typing import NewType

import pydantic

from classiq.interface.executor.execution_preferences import ExecutionPreferences
from classiq.interface.generator.model.constraints import Constraints
from classiq.interface.generator.model.preferences.preferences import Preferences
from classiq.interface.model.model import Model, SerializedModel

from classiq._internals import async_utils
from classiq._internals.api_wrapper import ApiWrapper

SerializedQuantumProgram = NewType("SerializedQuantumProgram", str)


async def synthesize_async(
    serialized_model: SerializedModel,
) -> SerializedQuantumProgram:
    model = pydantic.parse_raw_as(Model, serialized_model)
    quantum_program = await ApiWrapper.call_generation_task(model)
    return SerializedQuantumProgram(quantum_program.json(indent=2))


def synthesize(serialized_model: SerializedModel) -> SerializedQuantumProgram:
    """
    Synthesize a model with the Classiq engine to receive a quantum program.
    [More details](https://docs.classiq.io/latest/reference-manual/synthesis/)

    Args:
        serialized_model: A model object serialized as a string.

    Returns:
        SerializedQuantumProgram: Quantum program serialized as a string. (See: QuantumProgram)
    """
    return async_utils.run(synthesize_async(serialized_model))


def set_preferences(
    serialized_model: SerializedModel, preferences: Preferences
) -> SerializedModel:
    """
    Updates the preferences of a (serialized) model and returns the updated model.

    Args:
        serialized_model: The model in serialized form.
        preferences: The new preferences to be set for the model.

    Returns:
        SerializedModel: The updated model with the new preferences applied.
    """
    model = pydantic.parse_raw_as(Model, serialized_model)
    model.preferences = preferences
    return model.get_model()


def set_constraints(
    serialized_model: SerializedModel, constraints: Constraints
) -> SerializedModel:
    """
    Updates the constraints of a (serialized) model and returns the updated model.

    Args:
        serialized_model: The model in serialized form.
        constraints: The new constraints to be set for the model.

    Returns:
        SerializedModel: The updated model with the new constraints applied.
    """
    model = pydantic.parse_raw_as(Model, serialized_model)
    model.constraints = constraints
    return model.get_model()


def set_execution_preferences(
    serialized_model: SerializedModel, execution_preferences: ExecutionPreferences
) -> SerializedModel:
    """
    Attaching the execution preferences to the model.

    Args:
        serialized_model: A serialization of the defined model.
        execution_preferences: The execution preferences we want to attach to the model.
    Returns:
        SerializedModel: The model with the attached execution preferences.

    For more examples please see: [set_execution_preferences](https://docs.classiq.io/latest/reference-manual/executor/?h=set_execution_preferences#usage)

    """

    model = pydantic.parse_raw_as(Model, serialized_model)
    model.execution_preferences = execution_preferences
    return model.get_model()


__all__ = [
    "SerializedModel",
    "SerializedQuantumProgram",
    "synthesize",
    "set_preferences",
    "set_constraints",
    "set_execution_preferences",
]
