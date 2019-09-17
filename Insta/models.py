from django.db import models
from imagekit.models import ProcessedImageField

"""
Create your models here.
"""

class Post(models.Model):
    # blank = True 不加title可以发出去, null = True 没有title可以发出去
    title = models.TextField(blank=True, null=True)
    image = ProcessedImageField(
        upload_to="static/images/posts",
        format="JPEG",
        options={"quality": 100},
        blank=True,
        null=True
    )

