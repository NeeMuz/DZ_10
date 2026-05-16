import graphene
from graphene_django import DjangoObjectType
from .models import Article, Category, Tag


class CategoryType(DjangoObjectType):
    class Meta:
        model = Category
        fields = ("id", "name")


class TagType(DjangoObjectType):
    class Meta:
        model = Tag
        fields = ("id", "name")


class ArticleType(DjangoObjectType):
    class Meta:
        model = Article
        fields = (
            "id",
            "title",
            "content",
            "image",
            "category",
            "tags",
            "created_date",
        )


class CreateArticle(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        content = graphene.String(required=True)
        category_id = graphene.ID(required=False)
        tag_ids = graphene.List(graphene.ID, required=False)

    article = graphene.Field(ArticleType)

    @classmethod
    def mutate(cls, root, info, title, content, category_id=None, tag_ids=None):
        category = None
        if category_id:
            try:
                category = Category.objects.get(id=category_id)
            except Category.DoesNotExist:
                category = None

        article = Article.objects.create(
            title=title,
            content=content,
            category=category,
        )

        if tag_ids:
            tags = Tag.objects.filter(id__in=tag_ids)
            article.tags.set(tags)

        return CreateArticle(article=article)


class Query(graphene.ObjectType):
    all_articles = graphene.List(
        ArticleType,
        category_id=graphene.ID(required=False),
        tag_id=graphene.ID(required=False),
        search=graphene.String(required=False),
        sort_by=graphene.String(required=False),
    )

    def resolve_all_articles(self, info, category_id=None, tag_id=None, search=None, sort_by=None):
        qs = Article.objects.all()

        if category_id:
            qs = qs.filter(category_id=category_id)

        if tag_id:
            qs = qs.filter(tags__id=tag_id)

        if search:
            qs = qs.filter(title__icontains=search) | qs.filter(content__icontains=search)

        if sort_by:
            allowed = ["title", "-title", "created_date", "-created_date"]
            if sort_by in allowed:
                qs = qs.order_by(sort_by)

        return qs


class Mutation(graphene.ObjectType):
    create_article = CreateArticle.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
