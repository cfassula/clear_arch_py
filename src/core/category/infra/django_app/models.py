from django.db import models

# Create your models here.
class CategoryModel(models.Model):
    id = models.UUIDField(primary_key=True, editable=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=False, null=True)
    is_active = models.BooleanField()
    created_at = models.DateTimeField()

    class Meta: # pylint: disable=too-few-public-methods
        db_table = 'categories'
