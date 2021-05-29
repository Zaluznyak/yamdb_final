#!/usr/bin/python
# -*- coding: utf-8 -*-
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import Category, Comment, Genre, Review, Title


class GenreSerializer(serializers.ModelSerializer):

    class Meta:

        fields = ('name', 'slug')
        model = Genre


class CategorySerializer(serializers.ModelSerializer):

    class Meta:

        fields = ('name', 'slug')
        model = Category
        validators = [UniqueTogetherValidator(queryset=Category.objects.all(),
                      fields=['name'])]


class TitlesCreateUpdateSerializer(serializers.ModelSerializer):

    id = serializers.PrimaryKeyRelatedField(read_only=True)
    genre = serializers.SlugRelatedField(queryset=Genre.objects.all(),
                                         slug_field='slug', many=True)
    category = serializers.SlugRelatedField(queryset=Category.objects.all(),
                                            slug_field='slug')

    class Meta:

        fields = (
            'id',
            'name',
            'year',
            'genre',
            'category',
            'description',
        )
        model = Title


class TitlesListSerializer(serializers.ModelSerializer):

    id = serializers.PrimaryKeyRelatedField(read_only=True)
    genre = GenreSerializer(many=True)
    category = CategorySerializer()
    rating = serializers.IntegerField()

    class Meta:

        fields = (
            'id',
            'name',
            'year',
            'genre',
            'category',
            'description',
            'rating',
        )
        model = Title


class ReviewSerializer(serializers.ModelSerializer):

    author = serializers.SlugRelatedField(slug_field='username',
                                          read_only=True)

    def validate(self, data):
        title_id = self.context['view'].kwargs.get('title_id')
        author = self.context['request'].user
        if (self.context['request'].method == 'POST'
            and Review.objects.filter(title=title_id,
                                      author=author).exists()):
            raise serializers.ValidationError('You can review title only once'
                                              'Consider partial update of your'
                                              'review.')

        score = data.get('score')
        if not 1 <= score <= 10:
            raise serializers.ValidationError('Score value should'
                                              'be in between 1 and 10!')
        return data

    class Meta:

        model = Review
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):

    author = serializers.SlugRelatedField(slug_field='username',
                                          read_only=True)

    class Meta:

        model = Comment
        fields = '__all__'
