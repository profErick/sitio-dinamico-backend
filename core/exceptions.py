"""
Custom exception handler for consistent JSON error responses.
"""
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status


def custom_exception_handler(exc, context):
    """
    Custom exception handler that returns consistent JSON error responses.
    """
    # Call REST framework's default exception handler first
    response = exception_handler(exc, context)

    # Customize the response
    if response is not None:
        custom_response_data = {
            'error': True,
            'status_code': response.status_code,
            'message': 'Error en la solicitud',
            'details': response.data
        }

        # Handle validation errors
        if response.status_code == status.HTTP_400_BAD_REQUEST:
            custom_response_data['message'] = 'Error de validación'
            if isinstance(response.data, dict):
                # Flatten validation errors
                details = {}
                for key, value in response.data.items():
                    if isinstance(value, list):
                        details[key] = value[0] if value else 'Campo inválido'
                    else:
                        details[key] = value
                custom_response_data['details'] = details

        # Handle not found errors
        elif response.status_code == status.HTTP_404_NOT_FOUND:
            custom_response_data['message'] = 'Recurso no encontrado'
            custom_response_data['details'] = {'detail': 'El recurso solicitado no existe'}

        # Handle permission errors
        elif response.status_code == status.HTTP_403_FORBIDDEN:
            custom_response_data['message'] = 'Permiso denegado'
            custom_response_data['details'] = {'detail': 'No tienes permiso para realizar esta acción'}

        response.data = custom_response_data

    else:
        # Handle unexpected errors (500)
        custom_response_data = {
            'error': True,
            'status_code': status.HTTP_500_INTERNAL_SERVER_ERROR,
            'message': 'Error interno del servidor',
            'details': {'detail': 'Ha ocurrido un error inesperado. Por favor, intenta más tarde.'}
        }
        response = Response(custom_response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return response


