from django.shortcuts import render, redirect

from petstagram_app.main.forms import CreateProfileForm, EditProfileForm, DeleteProfileForm
from petstagram_app.main.helpers import get_profile
from petstagram_app.main.models import PetPhoto, Profile, Pet


def profile_action(request, form_class, redirect_url, instance, template_name):
    if request.method == "POST":
        form = form_class(request.POST, instance=instance)
        if form.is_valid:
            form.save()
            return redirect(redirect_url)
    else:
        form = form_class(instance=instance)

    context = {
        "form": form,
    }
    return render(request, template_name, context)


def show_profile(request):
    profile = get_profile()
    pets = list(Pet.objects.filter(user_profile=profile))
    pet_photos = PetPhoto.objects.filter(tagged_pets__user_profile=profile).distinct()

    total_likes_count = sum(pp.likes for pp in pet_photos)
    total_pet_photos_count = len(pet_photos)

    context = {
        "profile": get_profile(),
        "total_likes": total_likes_count,
        "total_pet_photos_count": total_pet_photos_count,
        "pets": pets,

    }
    return render(request, "profile_details.html", context)


def create_profile(request):
    # if request.method == "POST":
    #     # Create a form with POST
    #     form = CreateProfileForm(request.POST)
    #
    #     if form.is_valid():
    #         form.save()
    #         return redirect("index")
    #
    # else:
    #     # Create empty form
    #     form = CreateProfileForm()
    #
    # context = {
    #     "form": form,
    # }
    # return render(request, "profile_create.html", context)
    return profile_action(request, CreateProfileForm, "index", Profile(), "profile_create.html")


def edit_profile(request):
    # profile = get_profile()
    #
    # if request.method == "POST":
    #     form = EditProfileForm(request.POST, instance=profile)
    #
    #     if form.is_valid():
    #         form.save()
    #         return redirect("profile details")
    # else:
    #     form = EditProfileForm(instance=profile)
    #
    # context = {
    #     "form": form,
    # }
    # return render(request, "profile_edit.html", context)
    return profile_action(request, EditProfileForm, "profile details", get_profile(), "profile_edit.html")


def delete_profile(request):
    return render(request, DeleteProfileForm, "index", get_profile(), "profile_delete.html")
