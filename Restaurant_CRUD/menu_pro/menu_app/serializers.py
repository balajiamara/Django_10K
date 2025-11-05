from rest_framework import serializers
from .models import Menu

class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model=Menu
        fields='__all__'        #['DishId','DishName','Ingredients','Price','Image']

    def validate_Image(self,value):
        max_size=2*1024*1024  # 2 MB
        if value.size>max_size:
            raise serializers.ValidationError("Image size should not exceed 2 MB")
        
        allowed_types=['image/jpeg','image/png']
        if value.content_type not in allowed_types:
            raise serializers.ValidationError("Only JPEG and PNG images are allowed")
        return value
    