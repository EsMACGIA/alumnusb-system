from rest_framework.views import exception_handler
from rest_framework.exceptions import ValidationError


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    exception = exception_handler(exc, context)
    # Now add the HTTP status code to the response.
    errors = exception.data
    list_errors = []
    for key,value in errors.items():
      print(key,value)
      if hasattr(value[0],'code'):
        if value[0].code == 'required':
          list_errors.append('El campo {} es requerido'.format(key))
        if value[0].code == 'blank':
          list_errors.append('El campo {} no puede estar en blanco'.format(key))
        if value[0].code == 'unique':
          if key == 'username': # Ver si se puede cambiar este mensaje de error en otra parte del codigo
            list_errors.append('Ya existe un usuario con este username')
          else:
            list_errors.append(value[0])
        if value[0].code == 'null':
          list_errors.append('El campo {} no puede ser nulo'.format(key))
        if value[0].code == 'max_length':
          list_errors.append('{}: {}'.format(key,value[0]))
        if value[0].code == 'invalid_choice':
          list_errors.append('{} para el campo {}'.format(value[0][:-1],key))
      else:
          list_errors.append(value)
    response = {
      'status_code' : exception.status_code,
      'error' : list_errors
    }
    exception.data = response
    return exception