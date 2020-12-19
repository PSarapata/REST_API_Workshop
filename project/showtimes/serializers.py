from rest_framework import serializers
from movielist.models import Movie
from showtimes.models import Cinema, Screening


class CinemaSerializer(serializers.ModelSerializer):
    movies = serializers.HyperlinkedIdentityField(view_name='movie-details', many=True)

    class Meta:
        model = Cinema
        fields = ['name', 'city', 'movies']


class ScreeningSerializer(serializers.HyperlinkedModelSerializer):
    cinema = serializers.SlugRelatedField(slug_field='name', queryset=Cinema.objects.all())
    movie = serializers.SlugRelatedField(slug_field='title', queryset=Movie.objects.all())

    class Meta:
        model = Screening
        fields = ['id', 'movie', 'cinema', 'date']