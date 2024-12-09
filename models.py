# app/models.py

from tortoise.models import Model
from tortoise import fields
from enum import Enum

# Define enums for the application
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

class ObjectState(str, Enum):
    PENDING = "Pending"
    IN_PROGRESS = "In Progress"
    COMPLETED = "Completed"
    CANCELLED = "Cancelled"
    ARCHIVED = "Archived"

# Base model with common fields
class Base(Model):
    id = fields.IntField(pk=True)  # SERIAL PRIMARY KEY
    active = fields.BooleanField(default=True)  # Binary active field
    object_state = fields.CharEnumField(ObjectState, default=ObjectState.PENDING)  # Enum for object states
    properties = fields.JSONField(default={})  # JSONB DEFAULT '{}'::JSONB
    created = fields.DatetimeField(auto_now_add=True)  # TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    updated = fields.DatetimeField(auto_now=True)  # TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    class Meta:
        abstract = True

# Queue model
class Queue(Base):
    raw_text = fields.TextField()  # TEXT NOT NULL
    user_id = fields.IntField()  # Foreign key to the User model, but defined as an integer for simplicity

    class Meta:
        table = "queue"

# Transaction model
class Transaction(Base):
    shoe_id = fields.IntField()  # Foreign key to the Shoe model
    listing_id = fields.CharField(max_length=50, null=True)
    listing_status = fields.CharEnumField(ListingStatus, default=ListingStatus.NOT_LISTED)

    class Meta:
        table = "transactions"

# Audit model
class Audit(Base):
    shoe_id = fields.IntField()  # Foreign key to the Shoe model
    action_type = fields.CharField(max_length=255)
    actor = fields.CharField(max_length=255)  # The user or system initiating the action

    class Meta:
        table = "audits"

# User model
class User(Base):
    email = fields.CharField(max_length=255, unique=True, null=False)

    class Meta:
        table = "users"

# Image model
class Image(Base):
    queue_id = fields.ForeignKeyField("models.Queue", related_name="images", on_delete=fields.CASCADE)
    filename = fields.CharField(max_length=255, null=False)
    filepath = fields.CharField(max_length=255, null=False)
    filetype = fields.CharField(max_length=50, null=False)
    filesize = fields.IntField(null=False)

    class Meta:
        table = "images"

# Shoe model (kept as per previous versions, for reference)
class Shoe(Base):
    """Shoe inventory model with complete details and status tracking"""

    # Foreign key (Assuming User model exists)
    user_id = fields.ForeignKeyField(
        "models.User",
        related_name="shoes",
        on_delete=fields.CASCADE,
        description="Reference to the user owning the shoe"
    )

    # Basic shoe information
    brand = fields.CharField(max_length=255, null=False, index=True, description="Brand of the shoe")
    model = fields.CharField(max_length=255, null=False, index=True, description="Model name/number of the shoe")
    gender = fields.CharEnumField(Gender, null=False, index=True, description="Target gender")
    size = fields.DecimalField(max_digits=5, decimal_places=2, null=False, index=True, description="Size of the shoe")
    width = fields.CharField(max_length=50, default="M", description="Width of the shoe (e.g., M, W, N)")
    color = fields.CharField(max_length=255, null=False, index=True, description="Primary color of the shoe")
    shoe_type = fields.CharField(max_length=100, null=False, index=True, description="Type of shoe (e.g., Sneakers)")
    style = fields.CharField(max_length=100, null=False, description="Style of the shoe")

    # Additional details
    material = fields.CharField(max_length=255, null=True, description="Material of the shoe")
    heel_type = fields.CharField(max_length=100, null=True, description="Type of heel (if applicable)")
    occasion = fields.CharField(max_length=100, null=True, description="Occasion for use")
    condition = fields.CharField(max_length=50, default="Brand New, in Box", null=False, description="Condition of the shoe")
    special_features = fields.JSONField(null=True, description="Special features (if any)")

    # Product information
    upc = fields.CharField(max_length=20, unique=True, null=True, description="Unique product code")
    msrp = fields.DecimalField(max_digits=10, decimal_places=2, null=True, description="Manufacturer's suggested retail price")
    average_ebay_selling_price = fields.DecimalField(max_digits=10, decimal_places=2, null=True, description="Average selling price on eBay")
    category = fields.CharField(max_length=255, null=True, index=True, description="Category of the shoe")

    # Listing information
    photos = fields.JSONField(null=True, description="Photos associated with the listing")
    description = fields.TextField(null=True, description="Detailed description of the shoe")
    ebay_listing_id = fields.CharField(max_length=50, unique=True, null=True, description="eBay listing ID")
    ebay_listing_url = fields.CharField(max_length=255, null=True, description="eBay listing URL")
    listing_status = fields.CharEnumField(
        ListingStatus,
        default=ListingStatus.NOT_LISTED,
        null=False,
        description="Current status of the listing"
    )
    listing_start_date = fields.DatetimeField(null=True, description="Start date of the listing")
    listing_end_date = fields.DatetimeField(null=True, description="End date of the listing")

    # Sales information
    sale_price = fields.DecimalField(max_digits=10, decimal_places=2, null=True, description="Final sale price")
    buyer_username = fields.CharField(max_length=255, null=True, description="Username of the buyer")
    payment_status = fields.CharEnumField(
        PaymentStatus,
        default=PaymentStatus.PENDING,
        null=False,
        description="Status of the payment"
    )
    shipping_status = fields.CharEnumField(
        ShippingStatus,
        default=ShippingStatus.NOT_SHIPPED,
        null=False,
        description="Current shipping status"
    )
    shipping_tracking_number = fields.CharField(max_length=100, null=True, description="Tracking number for shipping")

    class Meta:
        table = "shoes"
