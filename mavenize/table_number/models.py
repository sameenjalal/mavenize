from django.db import models

class table_number(models.Model):
    table_number_id = models.AutoField(primary_key=True)
    table_name = models.CharField(max_length=255)
