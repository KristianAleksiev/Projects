from ToDoWorkshop.todos.models import Todo, Category
from rest_framework import serializers


class TodoForListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = ("id", "title", "user")


class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = ("id", "title", "description", "category", "is_done")

    #  Validated data => User
    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)


class CategoryForListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("id", "name",)
