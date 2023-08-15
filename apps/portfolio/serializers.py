from rest_framework import serializers

class MessageSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    sessionId = serializers.UUIDField()
    createdOn = serializers.DateTimeField()
    description = serializers.CharField()
    response = serializers.CharField()
    