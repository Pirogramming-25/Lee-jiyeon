from django.db import models

class Review(models.Model):
    GENRE_CHOICES = [
        ('SF', 'SF'),
        ('Comedy', 'Comedy'),
        ('Action', 'Action'),
        ('Drama', 'Drama'),
        ('Horror', 'Horror'),
    ]

    title = models.CharField('제목', max_length=100)
    release_year = models.IntegerField('개봉년도')
    genre = models.CharField('장르', max_length=20, choices=GENRE_CHOICES)
    rating = models.FloatField('별점')
    running_time = models.IntegerField('러닝타임')
    content = models.TextField('리뷰')
    director = models.CharField('감독', max_length=50)
    actors = models.CharField('주연', max_length=200)

    def __str__(self):
        return self.title
    
    def running_time_display(self):
        hours = self.running_time // 60
        minutes = self.running_time % 60
        return f"{hours}시간 {minutes}분"