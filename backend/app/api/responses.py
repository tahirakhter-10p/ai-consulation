from app.schemas.common import APIResponse, ErrorResponse

STANDARD_ERROR_RESPONSES = {
    400: {"model": ErrorResponse, "description": "Validation or domain error."},
    404: {"model": ErrorResponse, "description": "Requested resource was not found."},
    409: {"model": ErrorResponse, "description": "The operation conflicts with resource state."},
    500: {"model": ErrorResponse, "description": "Internal server error."},
    502: {"model": ErrorResponse, "description": "AI provider failure."},
}


def success_response[DataT](*, message: str, data: DataT) -> APIResponse[DataT]:
    """Build the documented standard success-response envelope."""

    return APIResponse(message=message, data=data)
