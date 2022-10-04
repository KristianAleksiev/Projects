from ToDoWorkshop.todos.models import Todo, Category
from ToDoWorkshop.todos.serializers import TodoForListSerializer, TodoSerializer, CategoryForListSerializer
from rest_framework import permissions
from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveUpdateAPIView


# Create your views here.


class TodosListAndCreateView(ListCreateAPIView):
    queryset = Todo.objects.all()
    list_serializer_class = TodoForListSerializer
    create_serializer_class = TodoSerializer
    permission_classes = (permissions.IsAuthenticated,)  # Anon user

    #  Filtering todos by user:
    def get_queryset(self):
        queryset = super().get_queryset()
        # Anon user, lack of React
        queryset = queryset.filter(user=self.request.user)
        # Filtering the todos by category, optimized, database level
        category_id = self.request.query_params.get("category", None)

        if category_id:
            queryset = queryset.filter(category_id=category_id)
        return queryset

    #  Serializer type
    def get_serializer_class(self):
        if self.request.method.lower() == "POST":
            return self.create_serializer_class
        return self.list_serializer_class

    def post(self, request, *args, **kwargs):
        response = super().post(request)

        return response


class CategoriesListView(ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Category.objects.all()
    serializer_class = CategoryForListSerializer

    #  Filter the user's categories that have a todo
    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     queryset = queryset.filter(todo__user=self.request.user)
    #     return queryset


class TodoDetailsUpdateView(RetrieveUpdateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer
