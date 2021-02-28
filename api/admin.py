from django.contrib import admin
from .models import Dog, Breed


class DogAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "sex",
        "coat_color",
        "behavior",
        "breed",
        "age",
    )


class BreedAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "description",
    )


admin.site.register(Dog, DogAdmin)
admin.site.register(Breed, BreedAdmin)
