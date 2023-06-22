from django.db import models


class Post(models.Model):
    url = models.URLField(unique=True)
    email = models.EmailField(default='example@example.com', max_length=254)
    password = models.CharField(default='default_password', max_length=250)


class Comment(models.Model):
    postUrl = models.CharField(max_length=250)
    text = models.TextField()
    author = models.CharField(max_length=100)
    def __str__(self):
        return self.postUrl


class miningData(models.Model):
    id = models.AutoField(primary_key=True)
    vader_neg = models.FloatField()
    vader_neu = models.FloatField()
    vader_pos = models.FloatField()
    vader_compound = models.FloatField()
    roberta_neg = models.FloatField()
    roberta_neu = models.FloatField()
    roberta_pos = models.FloatField()
    text = models.TextField()
    author = models.CharField(max_length=50)
    postUrl = models.URLField()

    def __str__(self):
        return self.postUrl
