from rest_framework import serializers

from reviews.models import ReviewModel


class ReviewCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = ReviewModel
        fields = ['stars', 'image_1', 'image_2', 'image_3', 'image_4', 'comment']


class ReviewListSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source='user.get_full_name')
    avatar = serializers.ImageField(source='user.profile.avatar')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['created_at'] = instance.created_at.strftime('%d.%m.%Y')
        return representation

    class Meta:
        model = ReviewModel
        fields = ['full_name', 'avatar', 'stars', 'image_1', 'image_2', 'image_3', 'image_4', 'comment', 'created_at']
