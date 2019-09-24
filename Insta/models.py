from django.db import models
from imagekit.models import ProcessedImageField

from django.urls import reverse

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

    def get_absolute_url(self):
        # 只能return 在app内的path
        # 如果给string，会接在调用url后面，比如/insta/post/new/<add>
        return reverse("post_detail", args=[str(self.id)])
 