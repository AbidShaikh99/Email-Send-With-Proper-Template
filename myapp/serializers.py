from rest_framework import serializers
from . models import *

class UserSerializer(serializers.Serializer):

    email = serializers.ListField(
        child=serializers.EmailField()
    )
    subject = serializers.CharField()
    body = serializers.CharField()
    sender_name = serializers.CharField()   
        