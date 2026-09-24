from django.db import models
from django.utils.text import slugify


class Phone(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    price = models.FloatField()
    image = models.URLField()
    release_date = models.DateField()
    lte_exists = models.BooleanField()
    slug = models.SlugField(max_length=255, unique=True, blank=True)

    def save(self, *args, **kwargs):
        base_slug = slugify(self.name)
        slug = base_slug

        ModelClass = self.__class__
        if ModelClass.objects.exclude(pk=self.pk).filter(slug=slug).exists():
            slug = f"{base_slug}-{self.pk or ''}".rstrip("-")

        self.slug = slug

        update_fields = kwargs.get("update_fields")
        if update_fields is not None:
            kwargs["update_fields"] = set(update_fields) | {"slug"}

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name