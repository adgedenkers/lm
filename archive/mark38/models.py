# app/models.py
from tortoise import fields
from tortoise.models import Model
from enum import Enum

# Define the base table model (with common fields)
class Base(Model):
    id = fields.IntField(pk=True)

    properties = fields.JSONField(null=True)
    active = fields.IntField(default=1)
    created = fields.DatetimeField(auto_now_add=True)
    updated = fields.DatetimeField(auto_now=True)

    class Meta:
        abstract = True

class queue(Base):
    raw_text = fields.CharField(max_length=255)
    photos = fields.JSONField(null=True)
    queue_status = fields.IntField(default=1)

    class Meta:
        table = "queue"

# Define the enums if they are not already defined
class Gender(str, Enum):
    MALE = "Male"
    FEMALE = "Female"
    UNISEX = "Unisex"

class ListingStatus(str, Enum):
    NOT_LISTED = "Not Listed"
    LISTED = "Listed"
    SOLD = "Sold"

class PaymentStatus(str, Enum):
    PENDING = "Pending"
    COMPLETED = "Completed"
    FAILED = "Failed"

class ShippingStatus(str, Enum):
    NOT_SHIPPED = "Not Shipped"
    SHIPPED = "Shipped"
    DELIVERED = "Delivered"

class Shoe(Base):
    """Shoe inventory model with complete details and status tracking"""
    
    user_id = fields.IntField(index=True, null=False, default=1)
    
    # Basic shoe information
    brand = fields.CharField(max_length=255, index=True)
    model = fields.CharField(max_length=255, index=True)
    gender = fields.CharEnumField(Gender, index=True)
    size = fields.DecimalField(max_digits=5, decimal_places=2, index=True)
    width = fields.CharField(max_length=50, default='M')
    color = fields.CharField(max_length=255, index=True)
    shoe_type = fields.CharField(max_length=100, index=True)
    style = fields.CharField(max_length=100)
    
    # Additional details
    material = fields.CharField(max_length=255, null=True)
    heel_type = fields.CharField(max_length=100, null=True)
    occasion = fields.CharField(max_length=100, null=True)
    condition = fields.CharField(max_length=50, default='Brand New, in Box')
    special_features = fields.JSONField(null=True)  # Tortoise uses JSONField for lists
    
    # Product information
    upc = fields.CharField(max_length=20, unique=True, null=True)
    msrp = fields.DecimalField(max_digits=10, decimal_places=2, null=True)
    average_ebay_selling_price = fields.DecimalField(max_digits=10, decimal_places=2, null=True)
    category = fields.CharField(max_length=255, index=True, null=True)
    
    # Listing information
    photos = fields.JSONField(null=True)  # JSONField to store array-like data
    description = fields.TextField(null=True)
    ebay_listing_id = fields.CharField(max_length=50, unique=True, null=True)
    ebay_listing_url = fields.CharField(max_length=255, null=True)
    listing_status = fields.CharEnumField(ListingStatus, default=ListingStatus.NOT_LISTED)
    listing_start_date = fields.DatetimeField(null=True)
    listing_end_date = fields.DatetimeField(null=True)
    
    # Sales information
    sale_price = fields.DecimalField(max_digits=10, decimal_places=2, null=True)
    buyer_username = fields.CharField(max_length=255, null=True)
    payment_status = fields.CharEnumField(PaymentStatus, default=PaymentStatus.PENDING)
    shipping_status = fields.CharEnumField(ShippingStatus, default=ShippingStatus.NOT_SHIPPED)
    shipping_tracking_number = fields.CharField(max_length=100, null=True)

    def __str__(self):
        return self.brand, self.model
    
    class Meta:
        table = "shoes"
    
