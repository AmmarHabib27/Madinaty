from rest_framework.renderers import JSONRenderer

_STATUS_MESSAGES = {
    400: 'Something went wrong. Please check the provided information and try again.',
    401: 'Authentication required. Please log in.',
    403: 'You do not have permission to perform this action.',
    404: 'The requested resource was not found.',
    405: 'This action is not allowed.',
    429: 'Too many requests. Please try again later.',
    500: 'Something went wrong. Please try again later.',
}


class StandardJSONRenderer(JSONRenderer):
    """Wrap every DRF response in {"code": ..., "message": ..., "data": ...}.

    Responses already in the standard envelope (produced by api_response())
    are passed through unchanged.

    For error responses:
    - If data contains a 'detail' key, it becomes the message and is removed from data.
    - Otherwise a generic message is derived from the HTTP status code.
    """

    def render(self, data, accepted_media_type=None, renderer_context=None):
        response = renderer_context.get('response') if renderer_context else None
        http_status = response.status_code if response else 200

        # Already a standard envelope — pass through unchanged.
        if isinstance(data, dict) and {'code', 'message', 'data'}.issubset(data.keys()):
            return super().render(data, accepted_media_type, renderer_context)

        message = ''
        if isinstance(data, dict) and 'detail' in data:
            message = str(data.pop('detail'))

        if not message:
            message = _STATUS_MESSAGES.get(http_status, '')

        envelope = {
            'code': http_status,
            'message': message,
            'data': data if data is not None else [],
        }

        return super().render(envelope, accepted_media_type, renderer_context)
