from django.db import models
from django.urls import reverse


class List(models.Model):
    pass

    def get_absolute_url(self):
        return reverse('list_detail', kwargs={'pk': self.pk})


class Item(models.Model):
    text = models.TextField(default='')
    list = models.ForeignKey(List, default=None, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.text

    class Meta:
        ordering = ('id',)
        unique_together = ('list', 'text')
