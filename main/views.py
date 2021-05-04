from django.shortcuts import render

# Create your views here.
from rest_framework import filters
from rest_framework.decorators import api_view
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import Category, Tag, Post
from .permissions import IsAdminPermission, IsAuthorPermission
from .serializers import CategorySerializer, TagSerializer, PostSerializer


@api_view()
def categories_list(request):
    categories = Category.objects.all()
    print(categories)
    serializer = CategorySerializer(categories, many=True)
    categories = serializer.data
    print(categories)
    return Response(categories)


class CategoriesListView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class TagsListView(ListAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class PostsListView(ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


# api/v1/posts/tag/
# api/v1/posts?tags=sport,interesting
class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_url_kwarg = 'slug'
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'text', 'tags__title']

    def get_permissions(self):
        if self.action == 'create':
            permissions = [IsAdminPermission]
        elif self.action in ['update', 'partial_update', 'destroy']:
            permissions = [IsAuthorPermission]
        else:
            permissions = []
        return [perm() for perm in permissions]

    def get_queryset(self):
        queryset = super().get_queryset()
        tags = self.request.query_params.get('tags')
        if tags is not None:
            tags = tags.split(',')
            queryset = queryset.filter(tags__slug__in=tags)
        return queryset

#TODO: сделать валидацию данных при создании
#TODO: сделать пагинацию, фильтрацию, поиск
#TODO: сделать документацию
#TODO: сделать восстановление и смену пароля
#TODO: сделать избранное(лайки)
#TODO: сделать комментарии