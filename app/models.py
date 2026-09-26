from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    ROLE_CHOICES=(
        ('ADMIN','admin'),
        ('CUSTOMER','customer'),
        ('DELIVERY','delivery')
    )

    user=models.OneToOneField(User,on_delete=models.CASCADE)
    role=models.CharField(max_length=100,choices=ROLE_CHOICES)


class Resturant(models.Model):
    name=models.CharField(max_length=100)
    location=models.CharField(max_length=100)

    def __str__(self):
        return self.name

class FoodItem(models.Model):
    resturant = models.ForeignKey(Resturant, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    image_url = models.URLField(blank=True, null=True)
    is_veg = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    @property
    def average_rating(self):
        reviews = self.reviews.all()
        if reviews:
            return round(sum(r.rating for r in reviews) / len(reviews), 1)
        return None

    @property
    def review_count(self):
        return self.reviews.count()


class Order(models.Model):
    STATUS = (
        ('PLACED', 'placed'),
        ('PACKING', 'packing'),
        ('OUT', 'out for delivery'),
        ('DELIVERED', 'delivered'),
        ('CANCELLED', 'cancelled'),

    )
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='customer')
    delivery = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='delivery')
    status = models.CharField(max_length=100, choices=STATUS, default='PLACED')
    created_at = models.DateTimeField(auto_now_add=True)
    razorpay_order_id = models.CharField(max_length=100, blank=True, null=True)
    razorpay_payment_id = models.CharField(max_length=100, blank=True, null=True)
    is_paid = models.BooleanField(default=False)
    is_refunded = models.BooleanField(default=False)
    cancel_reason = models.CharField(max_length=255, blank=True, null=True)
    delivery_address = models.ForeignKey('Address', on_delete=models.SET_NULL, null=True, blank=True)
    

    PAYMENT_METHOD = (
        ('ONLINE', 'Online Payment'),
        ('COD', 'Cash on Delivery'),
    )
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD, default='ONLINE')

    def __str__(self):
        return f"Order #{self.id} - {self.customer.username}"

    @property
    def total(self):
        return sum(oi.subtotal for oi in self.order_items.all())

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    food = models.ForeignKey(FoodItem, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=1)
    price = models.IntegerField()  # snapshot price at time of order

    @property
    def subtotal(self):
        return self.price * self.quantity

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    food = models.ForeignKey(FoodItem, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    @property
    def subtotal(self):
        return self.food.price * self.quantity

class Review(models.Model):
    RATING_CHOICES = (
        (1, '1 - Poor'),
        (2, '2 - Fair'),
        (3, '3 - Good'),
        (4, '4 - Very Good'),
        (5, '5 - Excellent'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    food = models.ForeignKey(FoodItem, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField(choices=RATING_CHOICES)
    comment = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.food.name} - {self.rating}★"

class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses')
    label = models.CharField(max_length=50, default='Home')
    full_address = models.CharField(max_length=255)
    is_default = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.label} - {self.full_address[:30]}"



    
