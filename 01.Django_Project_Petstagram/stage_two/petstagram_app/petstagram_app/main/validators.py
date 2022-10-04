from django.core.exceptions import ValidationError


def only_letters_validator(value):
    for ch in value:
        if not ch.isalpha():
            # Invalid case
            raise ValidationError("Value must contain only letters.")


def file_max_size_validator_mb(max_size):
    def validate(value):
        file_size = value.file.size
        if file_size > max_size * 1024 * 1024:
            raise ValidationError("Max file size is %sMB" % str(max_size))

    return validate
