import datetime

from django.core.validators import MinLengthValidator
from django.db import models
from petstagram_app.main.validators import only_letters_validator, file_max_size_validator_mb


# Create your models here.

class Profile(models.Model):
    FIRST_NAME_MAX_LENGTH = 30
    FIRST_NAME_MIN_LENGTH = 2

    LAST_NAME_MAX_LENGTH = 30
    LAST_NAME_MIN_LENGTH = 2

    MALE = "Male"
    FEMALE = "Female"
    DO_NOT_SHOW = "Do not show"

    GENDERS = [(x, x) for x in (MALE, FEMALE, DO_NOT_SHOW)]

    first_name = models.CharField(
        max_length=FIRST_NAME_MAX_LENGTH,
        validators=(
            MinLengthValidator(FIRST_NAME_MIN_LENGTH),
            only_letters_validator,
        )
    )

    last_name = models.CharField(
        max_length=LAST_NAME_MAX_LENGTH,
        validators=(
            MinLengthValidator(LAST_NAME_MIN_LENGTH),
            only_letters_validator,
        )
    )

    picture = models.URLField()

    # picture2 = models.CharField(validators=(URLValidator()))

    date_of_birth = models.DateField(
        null=True,
        blank=True,
    )

    description = models.TextField(
        null=True,
        blank=True,
    )

    email = models.EmailField(
        null=True,
        blank=True,
    )

    gender = models.CharField(
        max_length=max(len(x) for x, _ in GENDERS),
        choices=GENDERS,
        null=True,
        blank=True,
        default=DO_NOT_SHOW,
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Pet(models.Model):
    NAME_MAX_LENGTH = 30

    CAT = "Cat"
    DOG = "Dog"
    BUNNY = "Bunny"
    PARROT = "Parrot"
    FISH = "Fish"
    OTHER = "Other"

    TYPES = [(x, x) for x in (CAT, DOG, BUNNY, PARROT, FISH, OTHER)]

    name = models.CharField(
        max_length=NAME_MAX_LENGTH,
    )

    type = models.CharField(
        max_length=max(len(x) for (x, _) in TYPES),
        choices=TYPES,
    )

    date_of_birth = models.DateField(
        null=True,
        blank=True,
    )

    user_profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
    )

    @property
    def age(self):
        return datetime.datetime.now().year - self.date_of_birth.year

    class Meta:
        unique_together = ("user_profile", "name")


class PetPhoto(models.Model):
    photo = models.ImageField(
        validators=(
            file_max_size_validator_mb,
        )
    )

    tagged_pets = models.ManyToManyField(
        Pet,
        # validation needed
    )

    description = models.TextField(
        null=True,
        blank=True,
    )

    publication_date = models.DateTimeField(
        auto_now_add=True,
    )

    likes = models.IntegerField(
        default=0,
    )
