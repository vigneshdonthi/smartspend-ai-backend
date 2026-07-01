from rest_framework import serializers


class AnalyzeSerializer(serializers.Serializer):

    month = serializers.IntegerField(
        min_value=1,
        max_value=12,
    )

    year = serializers.IntegerField(
        min_value=2000,
        max_value=2100,
    )


class ChatSerializer(serializers.Serializer):

    month = serializers.IntegerField(
        min_value=1,
        max_value=12,
    )

    year = serializers.IntegerField(
        min_value=2000,
        max_value=2100,
    )

    question = serializers.CharField(
        max_length=500,
    )