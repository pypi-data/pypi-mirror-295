from pydantic import BaseModel, Field
import uuid


class JobEvent(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    topic: str
    data: str

    class Config:
        json_schema_extra = {
            "example": {
                "topic": "process_folder",
                "data": '{"folder_id": "1234567890", "force": false}',
            }
        }

    @classmethod
    def from_json(cls, json_str: str) -> "JobEvent":
        return cls.model_validate_json(json_str)

    def to_json(self) -> str:
        return self.model_dump_json(exclude_none=True)
