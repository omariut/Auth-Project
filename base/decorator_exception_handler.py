from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import BadRequest,ImproperlyConfigured,ObjectDoesNotExist,ValidationError

def exception_handler(func):
    def inner_function(request, *args, **kwargs):
        try:
            return func(request, *args, **kwargs)

        except ValueError as err:
            return Response(data={'error':str(err)}, status=status.HTTP_400_BAD_REQUEST)


        except ImproperlyConfigured as err:
            return Response(data={'error':str(err)}, status=status.HTTP_400_BAD_REQUEST)


        except ObjectDoesNotExist as err:
            return Response(data={'error':str(err)}, status=status.HTTP_400_BAD_REQUEST)


        except ValidationError as err:
            return Response(data={'error':str(err)}, status=status.HTTP_400_BAD_REQUEST)


        except Exception as err:
            return Response(data={'error':str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


        

    return inner_function

