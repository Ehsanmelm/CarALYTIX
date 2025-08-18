from django.db import models

# Create your models here.
class Role(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name = 'role'
        verbose_name_plural = 'roles'
        db_table = 'role'