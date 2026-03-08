from rest_framework.response import Response


def api_response(message: str = "", data=None, code: int = None, http_status: int = 200) -> Response:
    """Return a standardized API response envelope.

    Args:
        message:     Human-readable description of the result.
        data:        Response payload — list or dict. Defaults to [].
        code:        Application-level code. Defaults to http_status.
        http_status: HTTP status code for the response.

    Usage:
        return api_response("Created successfully.", data=serializer.data, http_status=201)
        return api_response("Deleted.", http_status=204)
        return api_response("Login failed.", code=401, http_status=401)
    """
    return Response(
        {
            'code': code if code is not None else http_status,
            'message': message,
            'data': data if data is not None else [],
        },
        status=http_status,
    )
