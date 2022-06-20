from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.


class TweetData(models.Model):
    id = models.IntegerField(unique=True, primary_key= True)
    text = models.TextField(max_length=255, unique=False, null=False, blank=False,)
    username = models.CharField(max_length=255, unique=False, null=False, blank=False)
    likes = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(100)])
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_at"]
        verbose_name_plural = "Tweetdata"
    
    def __str__(self):
        return "{} {} {}".format(self.username, self.id, self.text)