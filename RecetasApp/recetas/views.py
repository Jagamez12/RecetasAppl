from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import JsonResponse

from categorias.models import Categoria
from .serializers import RecetasSerializer
from .models import Recetas
from django.core.files.storage import FileSystemStorage
from django.conf import settings
import os
from datetime import datetime
from django.utils.text import slugify
from jose import jwt
from django.conf import settings

from seguridad.decorators import logueado


class RecetasAPIView(APIView):
    
    
    def get(self, request):
        recetas = Recetas.objects.all()
        data_json = RecetasSerializer(recetas, many=True)
        return JsonResponse({'estatus':'ok' ,'data': data_json.data}, status=200)
    
    @logueado()
    def post(self, request):
        try:
            data = request.data
            if Recetas.objects.filter(nombre=data.get('nombre')).exists():
                return JsonResponse({'estatus':'error', 'mensage': 'La receta ya existe'}, status=400)
            
            categoria = Categoria.objects.filter(id=data.get('categoria_id')).first()
            if not categoria:
                return JsonResponse({'estatus':'error', 'mensage': 'Categoria no encontrada'}, status=404)
            
            if request.FILES['foto'].content_type not in ['image/jpeg', 'image/png']:
                return JsonResponse({'estatus':'error', 'mensaje':'El archivo debe ser una imagen'}, status=400)
            
            fs = FileSystemStorage()
            foto = f"{datetime.timestamp(datetime.now())}_{os.path.splitext(str(request.FILES['foto']))[1]}"
            fs.save(f"recetas/{foto}", request.FILES['foto'])
            fs.url(request.FILES['foto'])
            
            header_payload = request.headers.get('Authorization').split(" ")
            resuelto = jwt.decode(header_payload[1], settings.SECRET_KEY, algorithms=['HS512'])
            
            
            
            Recetas.objects.create(
                nombre=data.get('nombre'),
                descripcion=data.get('descripcion'),
                tiempo_preparacion=data.get('tiempo_preparacion'),
                categoria=categoria,
                foto=foto,
                usuario_id = resuelto['id']
            )
            return JsonResponse({'estatus':'ok', 'mensage': 'Receta creada correctamente'}, status=201)
        except Exception as e:
            return JsonResponse({'estatus':'error', 'mensaje':'Ocurrio un error al crear la receta', 'error': str(e)}, status=500)    

class RecetaDetailAPIView(APIView):
    
    
    def get(self, request, id):
        try:
            receta = Recetas.objects.filter(id=id).get()
            data = RecetasSerializer(receta)
            return JsonResponse({'estatus':'ok', 'data': data.data}, status=200)
        except Recetas.DoesNotExist:
            return JsonResponse({'estatus':'error', 'mensage': 'Receta no encontrada'}, status=404)
        except Exception as e:
            return JsonResponse({'estatus':'error', 'mensage': str(e)}, status=500)
    @logueado
    def put(self, request, id):
        try:
            receta = Recetas.objects.filter(id=id).get()
        except Recetas.DoesNotExist:
            return JsonResponse({'estatus':'error', 'mensaje':'Receta no encontrada'}, status=404)
        
        if request.data.get('nombre') == None or request.data['nombre'] == '':
            return JsonResponse({'estatus':'error', 'mensaje':'El campo nombre es obligatorio'}, status=400)
        if request.data.get('categoria_id') == None or request.data['categoria_id'] == '':
            return JsonResponse({'estatus':'error', 'mensaje':'El campo categoria es obligatorio'}, status=400)
        if request.data.get('descripcion') == None or request.data['descripcion'] == '':
            return JsonResponse({'estatus':'error', 'mensaje':'El campo descripcion es obligatorio'}, status=400)
        if request.data.get('tiempo_preparacion') == None or request.data['tiempo_preparacion'] == '':
            return JsonResponse({'estatus':'error', 'mensaje':'El campo tiempo de preparacion es obligatorio'}, status=400) 
        
        receta.nombre = request.data['nombre']
        receta.descripcion = request.data['descripcion']
        receta.tiempo_preparacion = request.data['tiempo_preparacion']
        receta.categoria = Categoria.objects.filter(id=request.data['categoria_id']).first()
        receta.slug = slugify(request.data['nombre'])
        
        receta.save()
        return JsonResponse({'estatus':'ok', 'mensaje':'Receta actualizada correctamente'}, status=200)
    @logueado
    def delete(self, request, id):
        try:
            receta = Recetas.objects.filter(id=id).get()
        except Recetas.DoesNotExist:
            return JsonResponse({'estatus':'error', 'mensaje':'Receta no encontrada'}, status=404)
        if receta.foto:
            os.remove(f"{settings.MEDIA_ROOT}/recetas/{receta.foto}")
        receta.delete()
        return JsonResponse({'estatus':'ok', 'mensaje':'Receta eliminada correctamente'}, status=200)