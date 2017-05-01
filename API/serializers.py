from rest_framework import serializers

class CommandSerializer(serializers.Serializer):
	cmd = serializers.CharField(max_length=25550)
