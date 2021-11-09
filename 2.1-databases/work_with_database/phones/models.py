from django.db import models
from slugify import slugify


class Phone(models.Model):
    # TODO: Добавьте требуемые поля
    name = models.TextField()
    price = models.FloatField()
    image = models.ImageField(upload_to='res/')
    release_date = models.DateField()
    lte_exists = models.BooleanField()
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(f'iphone {self.name}')
        super(Phone, self).save(*args, **kwargs)
