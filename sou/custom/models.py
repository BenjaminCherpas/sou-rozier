#-*- coding: utf-8 -*-

from django.db import models

from coop_cms.models import MediaFilter
from coop_cms.settings import get_article_class


class ArticleMedia(models.Model):

    article = models.OneToOneField(get_article_class())
    media_filter = models.ForeignKey(MediaFilter)

    def __str__(self):
        return self.article