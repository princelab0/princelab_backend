from core.models import AI_APP
from rest_framework import serializers

#creating the serializers
class UserSerializers(serializers.HyperlinkedModelSerializer):
    class Meta:
        model= AI_APP
        fields = ['name','Type','image','describe']