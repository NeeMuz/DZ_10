from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name = "Категорія"
        verbose_name_plural = "Категорії"

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"

    def __str__(self):
        return self.name


class Article(models.Model):
    title = models.CharField("Заголовок", max_length=255)
    content = models.TextField("Текст")
    image = models.ImageField(
        "Зображення",
        upload_to="articles/%Y/%m/",
        blank=True,
        null=True,
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="articles",
        verbose_name="Категорія",
    )
    tags = models.ManyToManyField(
        Tag,
        blank=True,
        related_name="articles",
        verbose_name="Теги",
    )
    created_date = models.DateTimeField("Дата створення", auto_now_add=True)

    class Meta:
        verbose_name = "Стаття"
        verbose_name_plural = "Статті"
        ordering = ["-created_date"]

    def __str__(self):
        return self.title
