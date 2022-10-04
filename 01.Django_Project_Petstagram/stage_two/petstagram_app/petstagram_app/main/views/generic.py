from django.shortcuts import render

from petstagram_app.main.helpers import get_profile
from petstagram_app.main.models import PetPhoto


def show_home(request):
    context = {
        "hide_additional_nav_items": True,
    }
    return render(request, "home_page.html", context)


def show_dashboard(request):
    profile = get_profile()
    # if not profile:
    #     return redirect("401")
    pet_photos = set(PetPhoto.objects.prefetch_related("tagged_pets").filter(tagged_pets__user_profile=profile))

    context = {
        "pet_photos": pet_photos,
    }
    return render(request, "dashboard.html", context)
