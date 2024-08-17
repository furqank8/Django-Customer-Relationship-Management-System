from django.contrib import admin

# Import your models to be registered with the Django admin site
from .models import Customer, Product, Order, Tag

# Register the Customer model with the admin site
admin.site.register(Customer)

# Register the Product model with the admin site
admin.site.register(Product)

# Register the Order model with the admin site
admin.site.register(Order)

# Register the Tag model with the admin site
admin.site.register(Tag)
