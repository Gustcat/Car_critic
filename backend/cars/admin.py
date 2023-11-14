from django.contrib import admin

from .models import (
    Country,
    Producer,
    Car,
    Comment,
    )


admin.site.register(Country)
admin.site.register(Producer)
admin.site.register(Car)
admin.site.register(Comment)
