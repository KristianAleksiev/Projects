from django.contrib.auth import get_user_model
from rest_framework import serializers

UserModel = get_user_model()


class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = (UserModel.USERNAME_FIELD, "password",)

    #  Pass overhaul for plain text problem, encrypted
    def create(self, validated_data):
        user = super().create(validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user

    #  Called on return -> Remove pass from response
    def to_representation(self, instance):
        result = super().to_representation(instance)
        result.pop("password")
        return result

    #  Django password validations
    def validate(self, data):
        return super().validate(data)
