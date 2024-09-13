"""InstanceRegistry module."""

__all__ = ["InstanceRegistry"]


# TODO: consider emulating dict `get` functionality. Might just mean implement a
#       few special functions and removing `get_instance`. If we do this, we
#       should maybe remove `get_dict` func and replace it with `copy`.
class InstanceRegistry:
    """Registry for instances.

    Any instance registered is associated with an id that is retrieved by
    calling `id_fn`. This function is either passed in during registry
    initialization or defaults to calling `instance.id`. If a type is passed in
    at initialization, then all registered intances will be asserted to be
    instances of said type.

    All registered instances are required to have unique ids. Trying to register
    an instance with an id that has already been registered will result in an
    error being raised.

    Args:
        - id_fn: function that returns id of instance. Defaults to `instance.id`
        - instance_type: expected type of instances.
    """

    def __init__(self, *, id_fn=lambda x: x.id, instance_type=None):
        self.__instances = {}
        self.__id_fn = id_fn
        self.__instance_type = instance_type

    def register(self, instance):
        """Register an instance.

        Args:
            - instance: the instance being registered

        Raises:
            ValueError: an instance with that id has already been registered.
            ValueError: if  `instance_type` was passed in but type of instance
                does not match.
        """
        if self.__instance_type and not isinstance(
            instance, self.__instance_type
        ):
            raise ValueError(
                f"Expected to register an instance of {self.__instance_type}, "
                f"given: {instance.__class__}"
            )

        instance_id = self.__id_fn(instance)
        if instance_id in self.__instances:
            raise ValueError(
                "There is already an instance with the same id, given:",
                instance_id,
            )
        self.__instances[instance_id] = instance

    def deregister(self, instance_id):
        """Deregister an instance if it is registered.

        Args:
            - instance_id: the id of an instance already registered
        """
        if instance_id in self.__instances:
            del self.__instances[instance_id]

    def get_instance(self, instance_id, default=None):
        """Get an instance based on its id.

        Args:
            - instance_id: Id of the instance being retrieved.
            - default: What to return if there is no instance with id
                instance_id

        Returns:
            The instance if there is one with an id of instance_id, otherwise
                default (which is None unless explicitely set).
        """
        return self.__instances.get(instance_id, default)

    def clear(self):
        """Clear the registry. This removes all registered instances."""
        self.__instances.clear()

    def get_dict(self):
        """Dict representation of the registry."""
        return dict(self.__instances)

    def __len__(self):
        return len(self.__instances)
