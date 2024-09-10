from typing import List, Dict, TypeVar, Type, Optional, Annotated

from beanie import Document
from bson import ObjectId
from pydantic import Field, ConfigDict

from fastapi_easystart.models.beanie.managers.base import BaseModelManager
from fastapi_easystart.models.beanie.mixin.date_and_time import DateTimeModelMixin

# Define a type variable for the model class
ModelType = TypeVar('ModelType', bound='CustomBaseModelMixin')


class CustomBaseModelMixin(DateTimeModelMixin, Document):
    id: Annotated[ObjectId, Field(default_factory=ObjectId, alias='_id')]

    # Use a class variable to store the manager instance
    objects: BaseModelManager

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
    )

    @classmethod
    async def get(cls: Type[ModelType], model_id: str) -> ModelType:
        """
        Retrieves a model instance by its ID.

        Args:
            model_id (str): The ID of the model instance to retrieve.

        Returns:
            ModelType: The model instance with the given ID.

        Raises:
            ValueError: If no model instance with the given ID is found.
        """
        instance = await cls.get(ObjectId(model_id))
        if instance is None:
            raise ValueError(f"Instance with id {model_id} not found.")
        return instance

    @classmethod
    async def list(cls: Type[ModelType], query: Optional[Dict] = None) -> List[ModelType]:
        """
        Lists model instances based on the given query.

        Args:
            query (Optional[Dict]): The query to filter the model instances. Defaults to an empty dictionary if None is provided.

        Returns:
            List[ModelType]: A list of model instances matching the query.
        """
        if query is None:
            query = {}
        return await cls.find(query).to_list()

    @classmethod
    async def create(cls: Type[ModelType], **data) -> ModelType:
        """
        Creates a new instance of the model with the given data.

        Args:
            **data: The data to create the model instance.

        Returns:
            ModelType: The created model instance.
        """
        document = cls(**data)
        await document.insert()
        return document

    @classmethod
    async def update(cls: Type[ModelType], model_id: str, **data) -> ModelType:
        """
        Updates a model instance with the given ID and data.

        Args:
            model_id (str): The ID of the model instance to update.
            **data: The data to update the model instance with.

        Returns:
            ModelType: The updated model instance.

        Raises:
            ValueError: If no model instance with the given ID is found.
        """
        document = await cls.get(model_id)
        if document:
            await cls.update_one({"_id": ObjectId(model_id)}, {"$set": data})
            return await cls.get(model_id)
        raise ValueError(f"Instance with id {model_id} not found.")

    @classmethod
    async def delete(cls: Type[ModelType], model_id: str) -> bool:
        """
        Deletes a model instance with the given ID.

        Args:
            model_id (str): The ID of the model instance to delete.

        Returns:
            bool: True if the model instance was successfully deleted, False otherwise.
        """
        document = await cls.get(model_id)
        if document:
            await cls.delete_one({"_id": ObjectId(model_id)})
            return True
        return False
