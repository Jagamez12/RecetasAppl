from rest_framework.views import APIView
from django.http.response import JsonResponse
from http import HTTPStatus
from .models import Contacto
from utilidades.utilidades import sendMail


class ContactoAPIView(APIView): 
# Create your views here.
    def post(self, request):
        print("POST request received with data:", request.data)
        if request.data.get('nombre') is None or request.data['nombre']=='':
            return JsonResponse({'estatus': 'error', 'mensaje': 'El campo nombre es obligatorio'}, status=HTTPStatus.BAD_REQUEST)
        if request.data.get('correo') is None or request.data['correo']=='':
            return JsonResponse({'estatus': 'error', 'mensaje': 'El campo correo es obligatorio'}, status=HTTPStatus.BAD_REQUEST)
        if request.data.get('mensaje') is None or request.data['mensaje']=='':
            return JsonResponse({'estatus': 'error', 'mensaje': 'El campo mensaje es obligatorio'}, status=HTTPStatus.BAD_REQUEST)
        try:
            
            nuevo_contacto = Contacto.objects.create(
                nombre=request.data['nombre'],
                correo=request.data['correo'],
                telefono=request.data.get('telefono', ''),
                mensaje=request.data['mensaje']
            )
            nuevo_contacto.save()
            
            html = f""" 
                    <h1> Nuevo mensaje de contacto </h1>
                    <ul>
                        <li>Nombre: {request.data['nombre']}</li>
                        <li>Correo: {request.data['correo']}</li>
                        <li>Telefono: {request.data.get('telefono', 'No proporcionado')}</li>
                        <li>Mensaje: {request.data['mensaje']}</li>
                    </ul>
                    <p>Este mensaje fue enviado desde la aplicacion de recetas.</p>
                    """
            sendMail(html, "Nuevo mensaje de contacto", request.data['correo'])
            
            return JsonResponse({'estatus': 'ok', 'mensaje': 'Contacto creado exitosamente'}, status=HTTPStatus.CREATED)
        except Exception as e:
            print("Error al crear contacto:", str(e))
            return JsonResponse({'estatus': 'error', 'mensaje': 'Ocurrió un error al crear el contacto', 'error': str(e)}, status=HTTPStatus.INTERNAL_SERVER_ERROR)
        
             
        
    def get(self, request):
        contactos = Contacto.objects.all().values('id', 'nombre', 'correo', 'telefono', 'mensaje', 'fecha_creacion')
        return JsonResponse({'estatus': 'ok', 'contactos': list(contactos)}, status=HTTPStatus.OK)
    