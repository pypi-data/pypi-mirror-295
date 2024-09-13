"""Component implementations submodule.

Any component implementation should be exposed through here.
"""

from ..component_instance_registry import ComponentInstanceRegistry

from .graph_component import GraphComponent as Graph
from .single_boolean_component import SingleBooleanComponent
from .single_text_component import SingleTextComponent
from .single_number_component import SingleNumberComponent
from .button_component import ButtonComponent as Button


__all__ = ["Button", "Graph", "NumericInput", "Slider", "TextInput", "Toggle"]


@ComponentInstanceRegistry
class Slider(SingleNumberComponent):
    """Slider class which contains a single value.

    A slider has a value of a single number that can be accessed as an
    attribute: `slider.value`.
    """


@ComponentInstanceRegistry
class NumericInput(SingleNumberComponent):
    """Numeric class, representing a freeform or dropdown number component.

    The class has a single value that can be accessed as an attribute:
    `numeric_input.value`.
    """


@ComponentInstanceRegistry
class TextInput(SingleTextComponent):
    """Text class, representing a freeform or dropdown text component.

    The class has a single value that can be accessed as an attribute:
    `text_input.value`.
    """


@ComponentInstanceRegistry
class Toggle(SingleBooleanComponent):
    """Toggle class containing a single boolean value.

    The class has a single boolean value that can be accessed as an attribute:
    `toggle.value`.
    """
