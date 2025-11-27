from django.shortcuts import render
from rest_framework.views import APIView
from http import HTTPStatus
from django.http.response import JsonResponse
from categorias.models import Categoria
from seguridad.decorators import logueado
from django.contrib.auth.models import User

from recetas.models import Recetas
from recetas.serializers import RecetasSerializer

from dotenv import load_dotenv
import os
from datetime import datetime
from django.core.files.storage import FileSystemStorage

class Class1(APIView):
    
    @logueado()
    def get(self, request, id):
        try: 
            user = User.objects.get(id=id)
        except User.DoesNotExist:
            return JsonResponse({"estado":"error", "mensaje":"Ocurrio un error"}, status=HTTPStatus.BAD_REQUEST)
        
        data = Recetas.objects.filter(usuario_id=id).order_by("-id").all()
        
        data_serializada = RecetasSerializer(data, many=True)
        
        return JsonResponse({"estado":"ok", "data":data_serializada.data}, status=HTTPStatus.OK)
    
class FotoEditarAPIView(APIView):
    def post(self, request):
        if request.data.get('id') is None or not request.data.get('id'):
            return JsonResponse({"estado":"error", "mensaje":"El campo id es obligatorio"}, status=HTTPStatus.BAD_REQUEST)
        
        try:
            existe = Recetas.objects.filter(pk=request.data["id"]).get()
            antiguaFoto = existe.foto
        except Recetas.DoesNotExist:
            return JsonResponse({"estado":"error", "mensaje":"Algo salio mal!"}, status=HTTPStatus.BAD_REQUEST)
        
        fs = FileSystemStorage()
        try:
            foto = f"{datetime.timestamp(datetime.now())}{os.path.splitext(str(request.FILES['foto']))[1]}"
        except Exception as e:
            return JsonResponse({"estado":"error", "mensaje":"Debe adjuntar una foto en el campo foto."}, status=HTTPStatus.BAD_REQUEST)
        
        
        if request.FILES["foto"].content_type=="image/jpeg" or request.FILES["foto"].content_type == "image/png":
            try:
                fs.save(f"recetas/{foto}", request.FILES['foto'])
                fs.url(request.FILES['foto'])
            except Exception as e:
                return JsonResponse({"estado":"error", "mensaje":"Algo salio mal!"}, status=HTTPStatus.BAD_REQUEST)

            try:
                Recetas.objects.filter(id=request.data["id"]).update(foto=foto)
                os.remove(f"./media/recetas/{antiguaFoto}")
                return JsonResponse({"estado":"Ok", "mensaje":"La foto ha sido actualizada exitosamente."})
            except Exception as e:
                print(e)
                return JsonResponse({"estado":"error", "mensaje":"Algo salio mal!"}, status=HTTPStatus.BAD_REQUEST)
        
        else:
            return JsonResponse({"estado":"error", "mensaje":"Algo salio mal con el formato de la foto!"}, status=HTTPStatus.BAD_REQUEST)
        
class FiltroRecetasPorSlug(APIView):
    def get(self, request, slug):
        try:
            receta = Recetas.objects.filter(slug=slug).get()
            data = RecetasSerializer(receta)
            return JsonResponse({'estatus':'ok', 'data': data.data}, status=200)
        except Recetas.DoesNotExist:
            return JsonResponse({'estatus':'error', 'mensage': 'Receta no encontrada'}, status=404)
        except Exception as e:
            return JsonResponse({'estatus':'error', 'mensage': str(e)}, status=500)

class HomeRecetasAPIView(APIView):
    
    def get(self, request):
        data = Recetas.objects.order_by('?').all()[:3]
        data_json = RecetasSerializer(data, many=True)
        return JsonResponse({'estado':"Ok", 'data':data_json.data}, status=HTTPStatus.OK)
    
class RecetaBuscador(APIView):
    def get(self, request):
        
        #Validar que no viene vacio el argumento de categoria id
        if request.GET.get('categoria_id') is None or not request.GET.get("categoria_id"):
            return JsonResponse({'estado':"error", 'mensaje':"ocurrio un error inesperado"}, status=HTTPStatus.BAD_REQUEST)
        if not Categoria.objects.filter(id=request.GET.get('categoria_id')).exists():
            return JsonResponse({'estado':"error", 'mensaje':'La categoria no existe.'})
        data = Recetas.objects.filter(categoria_id = request.GET.get('categoria_id')).filter(nombre__icontains=request.GET.get('search')).order_by('-id').all()
        data_json = RecetasSerializer(data, many=True)
        return JsonResponse({'estado':'ok','data':data_json.data})
        