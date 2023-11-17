from datetime import datetime
from django.contrib.auth.models import AnonymousUser
from rest_framework import serializers
from djoser.serializers import UserCreateSerializer

from cars.models import (
    Country,
    Producer,
    Car,
    Comment,
    )


class CountrySerializer(serializers.ModelSerializer):
    producers = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Country
        fields = 'id', 'name', 'producers'

    def get_producers(self, obj):
        return [producer.name for producer in obj.producers.all()]


class NestedCarSerializer(serializers.ModelSerializer):
    comment_amount = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Car
        fields = 'name', 'comment_amount'

    def get_comment_amount(self, obj):
        return obj.comments.all().count()


class ProducerSerializer(serializers.ModelSerializer):
    cars = NestedCarSerializer(many=True, read_only=True)
    country = serializers.SlugRelatedField(
        slug_field='name',
        queryset=Country.objects.all()
    )

    class Meta:
        model = Producer
        fields = 'id', 'name', 'country', 'cars'


class CarSerializer(serializers.ModelSerializer):
    producer = serializers.SlugRelatedField(
        slug_field='name',
        queryset=Producer.objects.all()
    )
    comments = serializers.SerializerMethodField(read_only=True)
    comment_amount = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Car
        fields = ('id', 'name', 'producer', 'inception_year',
                  'completion_year', 'comments', 'comment_amount')

    def get_comments(self, obj):
        return [comment.comment for comment in obj.comments.all()]

    def get_comment_amount(self, obj):
        return obj.comments.all().count()

    def validate_inception_year(self, value):
        current_year = datetime.now().year
        if current_year < value:
            raise serializers.ValidationError(
                'Год выпуска автомобиля не может быть больше текущего года!')
        return value

    def validate(self, data):
        if data.get('completion_year') is not None and data.get('completion_year') < data.get('inception_year'):
            raise serializers.ValidationError(
                'Год выпуска автомобиля не может быть '
                'больше года окончания выпуска!')
        return super().validate(data)


class CommentSerializer(serializers.ModelSerializer):
    car = serializers.SlugRelatedField(
        slug_field='name',
        queryset=Car.objects.all()
    )
    email = serializers.EmailField(required=False, default=serializers.CurrentUserDefault())

    def validate_email(self, value):
        if not self.context['request'].user.is_anonymous:
            value = self.context['request'].user.email
        elif isinstance(value, AnonymousUser):
            raise serializers.ValidationError('Для анонимных пользователей'
                                              ' указание электронной почты'
                                              ' обязательно!')
        return value

    class Meta:
        model = Comment
        fields = 'id', 'email', 'car', 'comment'


class CustomUserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        fields = ('username', 'email', 'password')
