class ProfileDetailsView(views.DetailView):
    model = Profile
    template_name = "main/profile_details.html"
    context_object_name = "profile"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pets = list(Pet.objects.filter(user_id=self.object.id))
        pet_photos = PetPhoto.objects.filter(tagged_pets__in=self.object).distinct()

        total_likes_count = sum(pp.likes for pp in pet_photos)
        total_pet_photos_count = len(pet_photos)

        context.update({

            "total_likes": total_likes_count,
            "total_pet_photos_count": total_pet_photos_count,
            "is_owner": self.object.user_id == self.request.user.id,
            "pets": pets,
        })
        return context


# ----------------------------
from django.shortcuts import render, redirect
from django.views import generic as views
from petstagram_app.main.models import PetPhoto


class HomeView(views.TemplateView):
    template_name = "main/home_page.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context["hide_additional_nav_items"] = True
        return context

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("dashboard")
        return super().dispatch(request, *args, **kwargs)


class DashboardView(views.ListView):
    model = PetPhoto
    template_name = "main/dashboard.html"
    context_object_name = "pet_photos"


# ----------------------------

from django.contrib.auth import mixins as auth_mixins
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic as views
from petstagram_app.main.models import PetPhoto


class PetPhotoDetailsView(auth_mixins.LoginRequiredMixin, views.DetailView):
    model = PetPhoto
    template_name = "main/photo_details.html"
    context_object_name = "pet_photo"

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset.prefetch_related("tagged_pets")
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_owner"] = self.object.user == self.request.user
        return context


class CreatePetPhotoView(auth_mixins.LoginRequiredMixin, views.CreateView):
    model = PetPhoto
    template_name = "main/photo_create.html"
    fields = ("photo", "description", "tagged_pets")
    success_url = reverse_lazy("dashboard")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


def like_pet_photo(request, pk):
    pet_photo = PetPhoto.objects.get(pk=pk)
    pet_photo.likes += 1
    pet_photo.save()
    return redirect("pet photo details", pk)


class EditPetPhotoView(views.UpdateView):
    model = PetPhoto
    template_name = "main/photo_edit.html"
    success_url = reverse_lazy("dashboard")


# ----------------------------
from django.views import generic as views
from petstagram_app.main.forms import CreatePetForm, EditPetForm, DeletePetForm


class CreatePetView(views.CreateView):
    form_class = CreatePetForm
    template_name = "main/pet_create.html"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs


class EditPetView(views.UpdateView):
    form_class = EditPetForm
    template_name = "main/pet_edit.html"


class DeletePetView(views.DeleteView):
    form_class = DeletePetForm
    template_name = "main/pet_delete.html"


# ----------------------------
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy


# Create your views here.

class UserLoginView(auth_views.LoginView):
    template_name = "accounts/login_page.html"
    success_url = reverse_lazy("dashboard")

    def get_success_url(self):
        if self.success_url:
            return self.success_url
        return super().get_success_url()
