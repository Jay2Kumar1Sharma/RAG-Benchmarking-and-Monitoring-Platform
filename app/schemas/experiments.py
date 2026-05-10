from pydantic import BaseModel, Field


class ExperimentCreate(BaseModel):
    name: str
    description: str | None = None
    parameters: dict[str, object] = Field(default_factory=dict)


class ExperimentResponse(BaseModel):
    id: str
    name: str
    description: str | None = None
    parameters: dict[str, object] = Field(default_factory=dict)
    status: str

