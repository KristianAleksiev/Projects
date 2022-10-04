from ToDoWorkshop.todos.models import Todo, Category
from django.contrib import admin


# Register your models here.
@admin.register(Todo)
class TodoAdmin(admin.ModelAdmin):
    list_display = ("title", "username", "is_done")

    @staticmethod
    def username(obj):
        return obj.user.username


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
