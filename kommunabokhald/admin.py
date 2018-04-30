from django.contrib import admin
from django.contrib.auth.models import User

from .models import Rent, Housemate, Payment, GroceryItem


# Register your models here.
admin.site.register(Rent)
#admin.site.unregister(User)
admin.site.register(Housemate)
admin.site.register(Payment)
admin.site.register(GroceryItem)
