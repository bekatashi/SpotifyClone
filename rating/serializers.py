from rest_framework import serializers
from .models import Ratings


class RatingSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.email')

    class Meta:
        model = Ratings
        fields = '__all__'

