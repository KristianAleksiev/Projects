from ToDoWorkshop.todos.views import TodosListAndCreateView, CategoriesListView, TodoDetailsUpdateView
from django.urls import path

urlpatterns = [
    path("", TodosListAndCreateView.as_view(), name="todo list create"),
    path("categories/", CategoriesListView.as_view(), name="categories list"),
    path("<int:pk>/", TodoDetailsUpdateView.as_view(), name="todo details and update"),
]