from datetime import datetime

from pydantic import BaseModel, Field


class DateTimeModelMixin(BaseModel):
    created_at: datetime = Field(default_factory=datetime.utcnow,
                                 description="Timestamp when the document was created.")
    updated_at: datetime = Field(default_factory=datetime.utcnow,
                                 description="Timestamp when the document was last updated.")

    def update_timestamps(self):
        """Update the `updated_at` field with the current timestamp."""
        self.updated_at = datetime.utcnow()

    async def save(self, *args, **kwargs):
        """Override the save method to ensure timestamps are updated before saving."""
        self.update_timestamps()
        await super().save(*args, **kwargs)
