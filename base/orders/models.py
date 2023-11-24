from django.db import models
import uuid
from product import models as pmd
from users import models as umd

# Create your models here.


class Orders(models.Model):
    order_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    order_payment_id = models.CharField(max_length=100, blank=True)
    order_item = models.ForeignKey(
        pmd.Product_model, on_delete=models.CASCADE, related_name='order_item')
    order_price = models.DecimalField(decimal_places=2, max_digits=7)
    user_id = models.ForeignKey(
        umd.Users, on_delete=models.CASCADE, related_name='order_user_id')
    address = models.ForeignKey(umd.Address, on_delete=models.CASCADE)
    status = models.CharField(
        choices=[('processed', 'Processed'), ('ordered', 'Ordered'), ('shipped', 'Shipped'), ('delivery', 'Delivery'), ('cancel', 'Cancel')], max_length=100, default='processed')
    MOP = models.CharField(
        choices=[('cod', 'COD'), ('card', 'Card')], max_length=100)
    date_of_order = models.DateTimeField(auto_now_add=True)
    date_of_payment = models.DateTimeField(null=True)
