from rest_framework.views import APIView
from django.http.response import JsonResponse
from rest_framework.response import Response
from .serializers import CategoriaSerializer
from .models import Categoria
from django.utils.text import slugify
from recetas.models import Recetas
# Create your views here.

class CategoriaAPIView(APIView):
    
    
    def get(self, request):
        categorias = Categoria.objects.all()
        datos_jsin = CategoriaSerializer(categorias, many=True)
        return Response(datos_jsin.data)

    def post(self, request):
        try: 
            if request.data.get('nombre') == None or not request.data['nombre']:
                return JsonResponse({'message': 'El campo nombre es obligatorio'}, status=400)
            if Categoria.objects.filter(nombre=request.data['nombre']).exists():
                return JsonResponse({'message': 'Ya existe una categoria con ese nombre'}, status=400)
            data = request.data
            Categoria.objects.create(
                nombre=data['nombre']
            )
            return JsonResponse({'estatus': 'ok', 'mensaje':'Categoria creada exitosamente'}, status=201)
        except Exception as e:
            return JsonResponse({'estatus': 'error','message': 'Ocurrio un error durante la creacion de una Categoria', 'console':str(e)}, status=400)
    
class CategoriaDetailAPIView(APIView):
    
    
    def get(self, request, id):
        try:
            categoria = Categoria.objects.filter(id=id).get()
            datos_jsin = CategoriaSerializer(categoria)
            return JsonResponse({'data':datos_jsin.data}, status=200)
        except Categoria.DoesNotExist:
            return JsonResponse({'message': 'Categoria no encontrada'}, status=404)
        
    def put(self, request, id):
        try:
            categoria = Categoria.objects.filter(id=id).get()
            data = request.data
            if request.data.get('nombre') == None or data['nombre'] == '':
                return JsonResponse({'message': 'El campo nombre es obligatorio'}, status=400)
            categoria.nombre = data['nombre']
            categoria.slug = slugify(data['nombre'])
            categoria.save()
            return JsonResponse({'estatus':'ok','mensaje':'Categoria actualizada exitosamente'}, status=200)
        except Categoria.DoesNotExist:
            return JsonResponse({'status':'error', 'mensaje':'Categoria no encontrada'}, status=404)
        except Exception as e:
            return JsonResponse({'status':'error', 'mensaje':'Se ha producido un error al actualizar la categoria', 'error': str(e)}, status=400)
    
    def delete(self, request, id):
        try:
            categoria = Categoria.objects.filter(id=id).get()
            if Recetas.objects.filter(categoria=categoria).exists():
                return JsonResponse({'estatus': 'error', 'mensaje': 'No se pudo eliminar la Categoria'}, status=400)
            categoria.delete()
            return JsonResponse({'estatus':'ok', 'mensaje':'Categoria eliminada exitosamente'}, status=200)
        except Categoria.DoesNotExist:
            return JsonResponse({'estatus': 'error', 'mensaje': 'Categoria no encontrada'}, status=404)
        except Exception as e:
            return JsonResponse({'estatus':'error', 'mensaje': 'Se ha producido un error al eliminar la categoria', 'error': str(e)}, status=400)
        