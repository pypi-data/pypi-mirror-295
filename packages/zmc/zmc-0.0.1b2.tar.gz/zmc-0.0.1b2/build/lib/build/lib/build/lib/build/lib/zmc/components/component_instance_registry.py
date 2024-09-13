"""ComponentInstanceRegistry module."""

import functools

from .base_component import BaseComponent

__all__ = ["ComponentInstanceRegistry"]


# TODO: handle unregistering instances?
# TODO: decorator around BaseComponent to automatically add subclasses to registry?
class ComponentInstanceRegistry:
    """Registry of all `BaseComponent` instances created in the program.

    Any instance of a component class (i.e. subclass of `BaseComponent`)
    decorated  with `@ComponentInstanceRegistry` will automatically register
    instances in a shared registry. These instances will be able to be accessed
    from the registry from anywhere in the program that has access to it.

    When an instance is created, it is added automatically to the registry with
    no additional work needed from the user. If another instance with the same
    id has already been registered, an error will be raised.

    To enroll a subclass of `BaseComponent` to the registry, simply decorate it
    with `@ComponentInstanceRegistry`:
    ```
    @ComponentInstanceregistry
    class SomeComponent(BaseComponent):
        ...
    ```

    Decorating a class that is not a subclass of `BaseComponent` will result in
    a `ValueError` being raised.
    """

    __instances = {}

    def __new__(cls, component_cls):
        if not issubclass(component_cls, BaseComponent):
            raise ValueError(
                "ComponentInstanceRegistry can only decorate subclasses of "
                f"BaseComponent, given: {component_cls}"
            )
        original_init = component_cls.__init__

        @functools.wraps(original_init)
        def wrapped_init(instance, *args, **kwargs):
            original_init(instance, *args, **kwargs)
            ComponentInstanceRegistry.__register_instance(instance)

        component_cls.__init__ = wrapped_init
        return component_cls

    @staticmethod
    def __register_instance(instance):
        if instance.id in ComponentInstanceRegistry.__instances:
            raise ValueError(
                "There is already a component instantiated with id, given:", instance.id
            )
        ComponentInstanceRegistry.__instances[instance.id] = instance

    @staticmethod
    def get_instance(component_id):
        """Get a component instance based on its id.

        Args:
            - component_id: id of the component being retrieved.

        Returns:
            The component instance if there is one with component_id as its id,
                otherwise None.
        """
        return ComponentInstanceRegistry.__instances.get(component_id, None)

    @staticmethod
    def clear_registry():
        """Clear the registry. This removes all registered instances."""
        ComponentInstanceRegistry.__instances.clear()
