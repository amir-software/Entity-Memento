from django.db import models

# Define models and entities


class Product(models.Model): ## Sample Entity
    code = models.CharField()

    title = models.CharField()

    price = models.FloatField()

    creation_date = models.DateTimeField(auto_now_add=True)



class Memento(models.Model):
    modifier_user = models.CharField(max_length=50)

    modifier_ip = models.CharField(max_length=20)

    modification_type = models.CharField(max_length=20)

    object_id = models.TextField()

    object_data = models.TextField()

    modification_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class ProductMemento(Memento):
    class Meta:
        db_table = 'memento_product'