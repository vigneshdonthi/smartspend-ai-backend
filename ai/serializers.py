from rest_framework import serializers


class AnalyzeSerializer(serializers.Serializer):

    month = serializers.IntegerField(
        min_value=1,
        max_value=12,
    )

    year = serializers.IntegerField(
        min_value=2000,
    )

    def validate(self, data):

        month = data["month"]
        year = data["year"]

        if year > 2100:
            raise serializers.ValidationError(
                "Enter a valid year."
            )

        return data