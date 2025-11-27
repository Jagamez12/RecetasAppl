from rest_framework import serializers
from .models import Recetas
from RecetasApp.settings import BASE_DIR


class RecetasSerializer(serializers.ModelSerializer):
    
    categoria = serializers.ReadOnlyField(source='categoria.nombre')
    fecha_creacion = serializers.DateTimeField(format='%Y-%m-%d')
    foto = serializers.SerializerMethodField()
    usuario = serializers.ReadOnlyField(source='usuario.first_name')
    
    class Meta:
        model = Recetas
        fields = ['id', 'nombre', 'slug', 'tiempo_preparacion', 'foto', 'descripcion', 'fecha_creacion', 
                  'categoria', 'usuario_id', 'usuario']
        read_only_fields = ['fecha_creacion']
        
    def get_foto(self, obj):
        if obj.foto:
            return f"{BASE_DIR}/media/{obj.foto}"
        return None