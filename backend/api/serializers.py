from rest_framework import serializers

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
        fields = 'name', 'producers'

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
        fields = 'name', 'country', 'cars'


class CarSerializer(serializers.ModelSerializer):
    producer = serializers.SlugRelatedField(
        slug_field='name',
        queryset=Producer.objects.all()
    )
    comments = serializers.SerializerMethodField(read_only=True)
    comment_amount = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Car
        fields = ('name', 'producer', 'inception_year',
                  'completion_year', 'comments', 'comment_amount')

    def get_producers(self, obj):
        return [comment.comment for comment in obj.comments.all()]

    def get_comment_amount(self, obj):
        return obj.comments.all().count()


class CommentSerializer(serializers.ModelSerializer):
    car = serializers.SlugRelatedField(
        slug_field='name',
        queryset=Car.objects.all()
    )


    class Meta:
        model = Comment
        fields = 'email', 'car', 'comment'


