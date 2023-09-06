#created serializer.py to work with Django models.

from rest_framework import serializers
from core.models import User

class UserSerializator(serializers.HyperlinkedModelSerializer):
    class Meta:
        model= User
        fields= '__all__'

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
    
class SignInSerializer(serializers.HyperlinkedModelSerializer):
    model=User
    field= ['username','email','password']

