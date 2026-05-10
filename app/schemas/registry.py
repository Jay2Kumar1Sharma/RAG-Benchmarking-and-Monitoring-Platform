from pydantic import BaseModel


class ComponentListResponse(BaseModel):
    components: list[str]

