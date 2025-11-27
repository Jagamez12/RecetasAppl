from http import HTTPStatus
from django.shortcuts import render
from rest_framework.views import APIView
from django.http.response import JsonResponse
from django.contrib.auth.models import User
from django.http import Http404, HttpResponseRedirect
from django.contrib.auth import authenticate
from django.conf import settings
from datetime import datetime, timedelta
import time
from jose import jwt
from dotenv import load_dotenv
import os
import uuid

from utilidades.utilidades import sendMail

from .models import *

class RegistroAPIView(APIView):
    def post(self, request):
        if request.data.get('nombre') == None or not request.data.get('nombre'):
            return JsonResponse({'estado':'error', 'mensaje':'El campo nombre es obligatorio.'}, status=HTTPStatus.BAD_REQUEST)
        if request.data.get('correo') == None or not request.data.get('correo'):
            return JsonResponse({'estado':'error', 'mensaje':'El campo correo es obligatorio.'}, status=HTTPStatus.BAD_REQUEST)
        if request.data.get('password') == None or not request.data.get('password'):
            return JsonResponse({'estado':'error', 'mensaje':'El campo password es obligatorio.'}, status=HTTPStatus.BAD_REQUEST)
        
        if User.objects.filter(email=request.data['correo']).exists():
            return JsonResponse({'estado':'error', 'mensaje':'el correo no esta disponible.'}, status=HTTPStatus.BAD_REQUEST)
        
        token = uuid.uuid4()
        url = f"{os.getenv('BASE_URL')}api/seguridad/verificacion/{token}"
         
        try:
            user = User.objects.create_user(
                username=request.data["correo"],
                email=request.data["correo"],
                password=request.data["password"],
                first_name = request.data["nombre"],
                is_active = False,
            )
            UsersMetadata.objects.create(
                user=user,
                token= token
            )
            
            html = f""" 
            <h3>Activacion de cuenta para RecetasAPP</h3>
            <p>Hola! {user.first_name}, nos complace que te unas a la comunidad de RecetasAPP, para activar tu cuenta
            ingresa en el siguiente link</p>
            
            <a href='{url}'>CLICK EN MI !!</a>
            """
            sendMail(html, "ACTIVACION DE LA CUENTA - RECEPTASAPP", request.data['correo'])
            
        except Exception as e:
            print(e)
            return JsonResponse({"estado":"error", "mensaje":"ocurrio un error inesperado"}, status=HTTPStatus.BAD_REQUEST)

        return JsonResponse({"estado":"ok", "mensaje":"Se creo el registro exitosamente."}, status=HTTPStatus.CREATED)
    
class ActivarCuentaAPIView(APIView):
    def get(self, request, token):
        if token is None or not token:
            return JsonResponse({"estado":"error", "mensaje":"Recurso no disponible."}, status=404)
        try: 
            data = UsersMetadata.objects.filter(token=token).get()
            UsersMetadata.objects.filter(token=token).update(token="")
            User.objects.filter(id=data.user_id).update(is_active = 1)
            
            return HttpResponseRedirect(f"{os.getenv('BASE_URL_FRONTEND')}")
        except UsersMetadata.DoesNotExist:
            raise Http404
        
class Login(APIView):
    
    def post(self, request):
        
        if request.data.get('correo') == None or not request.data.get('correo'):
            return JsonResponse({'estado':'error', 'mensaje':'El campo correo es obligatorio.'}, status=HTTPStatus.BAD_REQUEST)
        if request.data.get('password') == None or not request.data.get('password'):
            return JsonResponse({'estado':'error', 'mensaje':'El campo password es obligatorio.'}, status=HTTPStatus.BAD_REQUEST)
        try: 
            user = User.objects.filter(email = request.data["correo"]).get()
            
        except User.DoesNotExist:
            return JsonResponse({"estado":"error", "mensaje":"Recurso no disponible"}, status=HTTPStatus.NOT_FOUND)
        
        auth = authenticate(request, username = request.data["correo"], password = request.data.get("password"))
        
        if auth is not None:
            fecha_dia = datetime.now()
            fecha_expiracion = fecha_dia + timedelta(days=1)
            fecha_expiracion_numero = int(datetime.timestamp(fecha_expiracion))
            payload = {"id":user.id, "ISS":os.getenv("BASE_URL"), "iat": int(time.time()), "exp":fecha_expiracion_numero}
            try:
                token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS512')
                return JsonResponse({"id":user.id, "first_name": user.first_name, "token":token}, status=HTTPStatus.OK)
            except Exception as e:
                print(e)
                return JsonResponse({"estado":"error", "mensaje":"Ocurrio un error inesperado."}, status=HTTPStatus.BAD_REQUEST)
        else: 
            return JsonResponse({"estado":"error", "mensaje":"Las credenciales ingresadas no son correctas."}, status= HTTPStatus.BAD_REQUEST)
        
