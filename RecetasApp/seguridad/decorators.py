from functools import wraps
import time
from django.conf import settings
from django.http.response import JsonResponse
from http import HTTPStatus
from jose import jwt

def logueado(redirect_url=None):
    def metodo(func):
        @wraps(func)
        def _decorator(request,*args, **kwargs):
            req = args[0]
            if not req.headers.get("Authorization") or req.headers.get("Authorization") == None:
                return JsonResponse({'estado':'error','mensaje':'Sin autorizacion.'}, status=HTTPStatus.UNAUTHORIZED)
            header = req.headers.get("Authorization").split(" ")
            try:
                resuelto = jwt.decode(header[1], settings.SECRET_KEY, algorithms=['HS512'])
            except Exception as e:
                return JsonResponse({'estado':'error','mensaje':'Sin autorizacion.'}, status=HTTPStatus.UNAUTHORIZED)
            
            if int(resuelto["exp"]) < int(time.time()):
                return JsonResponse({'estado':'error','mensaje':'Sin autorizacion.'}, status=HTTPStatus.UNAUTHORIZED)
            return func(request, *args, **kwargs)
        return _decorator
    return metodo