from django.db import models

# Model representing a Customer
class Customer(models.Model):
    """
    Represents a customer with their personal details and profile picture.
    """
    name = models.CharField(max_length=200, null=True)  # Customer's name
    phone = models.CharField(max_length=200, null=True)  # Customer's phone number
    email = models.CharField(max_length=200, null=True)  # Customer's email address
    profile_pic = models.ImageField(null=True, blank=True)  # Profile picture of the customer
    date_created = models.DateField(auto_now_add=True, null=True)  # Date when the customer was created

    def __str__(self):
        return self.name  # String representation of the Customer object

# Model representing a Tag
class Tag(models.Model):
    """
    Represents a tag that can be associated with products.
    """
    name = models.CharField(max_length=200, null=True)  # Name of the tag

    def __str__(self):
        return self.name  # String representation of the Tag object

# Model representing a Product
class Product(models.Model):
    """
    Represents a product with its details and associated tags.
    """
    CATEGORY = (
        ('Indoor', 'Indoor'),  # Product category for indoor use
        ('Out Door', 'Out Door')  # Product category for outdoor use
    )
    name = models.CharField(max_length=200, null=True)  # Name of the product
    price = models.FloatField(null=True)  # Price of the product
    category = models.CharField(max_length=200, null=True, choices=CATEGORY)  # Product category
    description = models.CharField(max_length=200, null=True, blank=True)  # Description of the product
    date_created = models.DateField(auto_now_add=True, null=True)  # Date when the product was created
    tag = models.ManyToManyField(Tag)  # Tags associated with the product

    def __str__(self):
        return self.name  # String representation of the Product object

# Model representing an Order
class Order(models.Model):
    """
    Represents an order placed by a customer for a product, with status and notes.
    """
    STATUS = (
        ('Pending', 'Pending'),  # Order status for pending
        ('Out for delivery', 'Out for delivery'),  # Order status for out for delivery
        ('Delivered', 'Delivered')  # Order status for delivered
    )
    customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL)  # Customer who placed the order
    product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)  # Product being ordered
    status = models.CharField(max_length=200, null=True, choices=STATUS)  # Status of the order
    note = models.CharField(max_length=200, null=True)  # Additional notes about the order
    date_created = models.DateField(auto_now_add=True, null=True)  # Date when the order was created
