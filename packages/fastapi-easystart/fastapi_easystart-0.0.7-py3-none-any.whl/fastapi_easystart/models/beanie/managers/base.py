from typing import Type, List, Dict

from fastapi_easystart.models.beanie.mixin import CustomBaseModelMixin

# Use a descriptive type for models that extend CustomBaseModelMixin
ModelType = Type[CustomBaseModelMixin]


class BaseModelManager:
    """
    A generic manager class for handling CRUD operations on Beanie models.

    Attributes:
        model (ModelType): The Beanie model class this manager is responsible for.
    """

    def __init__(self, model: ModelType):
        """
        Initializes the manager with the given model class.

        Args:
            model (ModelType): The Beanie model class.
        """
        self.model = model

    async def create(self, **data) -> CustomBaseModelMixin:
        """
        Creates a new instance of the model with the given data.

        Args:
            **data: The data to create the model instance.

        Returns:
            CustomBaseModelMixin: The created model instance.
        """
        return await self.model.create(**data)

    async def get(self, model_id: str) -> CustomBaseModelMixin:
        """
        Retrieves a model instance by its ID.

        Args:
            model_id (str): The ID of the model instance to retrieve.

        Returns:
            CustomBaseModelMixin: The model instance with the given ID.

        Raises:
            ValueError: If no model instance with the given ID is found.
        """
        instance = await self.model.get(model_id)
        if instance is None:
            raise ValueError(f"Instance with id {model_id} not found.")
        return instance

    async def list(self, query: Dict = None) -> List[CustomBaseModelMixin]:
        """
        Lists model instances based on the given query.

        Args:
            query (Dict): The query to filter the model instances. Defaults to an empty dictionary if None is provided.

        Returns:
            List[CustomBaseModelMixin]: A list of model instances matching the query.
        """
        if query is None:
            query = {}
        return await self.model.list(query)

    async def update(self, model_id: str, **data) -> CustomBaseModelMixin:
        """
        Updates a model instance with the given ID and data.

        Args:
            model_id (str): The ID of the model instance to update.
            **data: The data to update the model instance with.

        Returns:
            CustomBaseModelMixin: The updated model instance.

        Raises:
            ValueError: If no model instance with the given ID is found.
        """
        instance = await self.model.update(model_id, **data)
        if instance is None:
            raise ValueError(f"Instance with id {model_id} not found.")
        return instance

    async def delete(self, model_id: str) -> bool:
        """
        Deletes a model instance with the given ID.

        Args:
            model_id (str): The ID of the model instance to delete.

        Returns:
            bool: True if the model instance was successfully deleted, False otherwise.
        """
        return await self.model.delete(model_id)
