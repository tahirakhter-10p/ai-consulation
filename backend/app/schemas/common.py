from pydantic import BaseModel, ConfigDict, Field


class APIResponse[DataT](BaseModel):
    """Standard successful API response envelope."""

    success: bool = True
    message: str
    data: DataT


class ErrorDetail(BaseModel):
    """One validation error in the standard error response envelope."""

    field: str
    message: str


class ErrorResponse(BaseModel):
    """Standard failed API response envelope."""

    success: bool = False
    message: str
    errors: list[ErrorDetail] = Field(default_factory=list)


class ORMResponseModel(BaseModel):
    """Base response model that can be created from SQLAlchemy entities."""

    model_config = ConfigDict(from_attributes=True)
