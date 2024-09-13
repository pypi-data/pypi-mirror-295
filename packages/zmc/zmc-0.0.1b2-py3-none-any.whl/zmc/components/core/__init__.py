"""Core components submodule"""

from .base_component import BaseComponent, _BaseComponentMeta
from .data_sender_base_component import DataSenderBaseComponent
from .value_receiver_base_component import ValueReceiverBaseComponent
from .single_value_component import SingleValueComponent

__all__ = [
    "BaseComponent",
    "DataSenderBaseComponent",
    "ValueReceiverBaseComponent",
]


# Remove files which are added to the namespace because of imports but are not
# meant to be accessed directly by the user.
# pylint:disable=undefined-variable
# mypy: ignore-errors
del (
    base_component,
    data_sender_base_component,
    value_receiver_base_component,
    single_value_component,
)
