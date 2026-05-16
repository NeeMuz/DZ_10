from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Article, Category, Tag, Comment
from .serializers import ArticleSerializer, CategorySerializer, TagSerializer, CommentSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from .permissions import IsAuthorOrAdminOrReadOnly, IsEditorsGroupOrReadOnly


class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all().order_by('-created_date')
    serializer_class = ArticleSerializer

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

    filterset_fields = ['author'] # Точний фільтр за категорією та автором
    search_fields = ['title', 'content'] # Пошук за заголовком та вмістом
    ordering_fields = ['created_date', 'title'] # Сортування за датою створення та заголовком
    ordering = ['-created_date'] # За замовчуванням сортувати за датою створення у спадному порядку

    permission_classes = [
        IsAuthenticatedOrReadOnly,
        IsEditorsGroupOrReadOnly,
        IsAuthorOrAdminOrReadOnly
    ]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)



class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    permission_classes = [IsAuthenticated]


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

    permission_classes = [AllowAny]

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [AllowAny]
