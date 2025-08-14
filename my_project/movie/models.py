from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import MinValueValidator, MaxValueValidator

STATUS_CHOICES = (
    ('pro', 'pro'),
    ('simple', 'simple')
)

class Profile(AbstractUser):
    phone_number = PhoneNumberField(null=True, blank=True)
    age = models.PositiveSmallIntegerField(validators=[MinValueValidator(12), MaxValueValidator(75)],
                                           null=True, blank=True)
    avatar = models.ImageField(upload_to='user_avatar/', null=True, blank=True)
    status = models.CharField(choices=STATUS_CHOICES, default='simple')
    data_registered = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.first_name} - {self.last_name}'


class Country(models.Model):
    country_name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.country_name


class Director(models.Model):
    director_name = models.CharField(max_length=64)
    director_bio = models.TextField()
    director_age = models.PositiveSmallIntegerField(validators=[MinValueValidator(16), MaxValueValidator(95)])
    director_image = models.ImageField(upload_to='director_image/', null=True, blank=True)

    def __str__(self):
        return self.director_name


class Actor(models.Model):
    actor_name = models.CharField(max_length=64)
    actor_bio = models.TextField()
    actor_age = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    actor_image = models.ImageField(upload_to='actor_image/', null=True, blank=True)

    def __str__(self):
        return self.actor_name


class Genre(models.Model):
    genre_name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.genre_name


class Movie(models.Model):
    movie_name = models.CharField(max_length=64)
    year = models.DateField()
    country = models.ManyToManyField(Country, related_name='countries')
    director = models.ManyToManyField(Director)
    actor = models.ManyToManyField(Actor)
    genre = models.ManyToManyField(Genre)
    TYPES_CHOICES = (
    ('144p', '144p'),
    ('270p', '270p'),
    ('360p', '360p'),
    ('480p', '480p'),
    ('720p', '720p'),
    ('1080p', '1080p'),
    )
    types = models.CharField(choices=TYPES_CHOICES, default='360p')
    movie_time = models.PositiveSmallIntegerField()
    descriptions = models.TextField()
    movie_trailer = models.URLField()
    movie_image = models.ImageField(upload_to='movie_image/')
    status_movie = models.CharField(choices=STATUS_CHOICES, default='simple')

    def __str__(self):
        return f'{self.movie_name}'

    def get_avg_rating(self):
        score = self.ratings.all()
        if score.exists():
            return round(sum([i.stars for i in score]) / score.count(), 2)
        return 0

    def get_count_people(self):
        return self.ratings.count()


class MovieLanguage(models.Model):
    language = models.CharField(max_length=32)
    video = models.FileField(upload_to='movie_videos/', null=True, blank=True)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='languages')

    def __str__(self):
        return f'{self.language}-{self.movie}'


class Moments(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='moments')
    movie_moment = models.ImageField(upload_to='movie_moment/', null=True, blank=True)

    def __str__(self):
        return f'{self.movie}'


class Rating(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='ratings')
    stars = models.PositiveSmallIntegerField(choices=[(i, str(i)) for i in range(1, 11)])
    text = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user}-{self.movie}'


class Favorite(models.Model):
    user = models.OneToOneField(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return self.user


class  FavoriteMovie(models.Model):
    favorite = models.ForeignKey(Favorite, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.favorite}-{self.movie}'


class History(models.Model):
    user = models.OneToOneField(Profile, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    viewed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user