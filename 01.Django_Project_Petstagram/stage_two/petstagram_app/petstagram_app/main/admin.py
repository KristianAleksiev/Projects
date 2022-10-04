from django.contrib import admin

from petstagram_app.main.models import Profile, Pet, PetPhoto


class PetInlineAdmin(admin.StackedInline):
    model = Pet


# Register your models here.
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    inlines = (PetInlineAdmin,)  # < In the admin panel, when a user is selected, the pets are seen as well
    list_display = ("first_name", "last_name")


@admin.register(Pet)
class PetAdmin(admin.ModelAdmin):
    list_display = ("name", "type")


@admin.register(PetPhoto)
class PetPhotoAdmin(admin.ModelAdmin):
    pass
