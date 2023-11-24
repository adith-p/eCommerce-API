from django.db import models
import uuid
# Create your models here.


class Product_model(models.Model):
    product_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, name='product_id')
    product_name = models.CharField(
        max_length=255, blank=False, name='product_name')
    pr_desc = models.TextField()
    pr_price = models.DecimalField(decimal_places=2, max_digits=7)
    pr_stock = models.IntegerField(default=10)
    pr_date = models.DateTimeField(auto_now_add=True)
    pr_m_date = models.DateTimeField(auto_now=True)


class Product_image(models.Model):
    pr_i_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, name='product_id')
    pr_img = models.ImageField(upload_to='product/')
    prid = models.ForeignKey(
        Product_model, on_delete=models.CASCADE, related_name='product')
