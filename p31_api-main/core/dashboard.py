from django.utils.translation import gettext_lazy as _

def get_dashboard_stats(request):
    from news.models import Article, Category, Tag
    from django.contrib.auth.models import User
    
    return [
        {
            "label": "Всього статей",
            "number": Article.objects.count(),
            "header_icon": "article",
            "color": "primary", # Фіолетовий
        },
        {
            "label": "Категорії",
            "number": Category.objects.count(),
            "header_icon": "category",
            "color": "info", # Блакитний
        },
        {
            "label": "Користувачі",
            "number": User.objects.count(),
            "header_icon": "person",
            "color": "success", # Зелений
        },
        {
            "label": "Теги",
            "number": Tag.objects.count(),
            "header_icon": "sell",
            "color": "warning", # Помаранчевий
        },
    ]

def get_activity_chart(request):
    from news.models import Article
    from django.db.models import Count
    from django.db.models.functions import TruncMonth
    import datetime

    # Дані за останні 6 місяців
    data = (
        Article.objects.annotate(month=TruncMonth('created_date'))
        .values('month')
        .annotate(count=Count('id'))
        .order_by('month')
    )
    
    months = ["Січ", "Лют", "Бер", "Кві", "Тра", "Чер", "Лип", "Сер", "Вер", "Жов", "Лис", "Гру"]
    labels = [months[d['month'].month - 1] for d in data] if data else ["Немає даних"]
    values = [d['count'] for d in data] if data else [0]

    return {
        "labels": labels,
        "datasets": [
            {
                "label": "Нові статті",
                "data": values,
                "backgroundColor": "#9333ea",
            }
        ],
    }

def get_categories_chart(request):
    from news.models import Article
    from django.db.models import Count
    
    data = (
        Article.objects.values('category')
        .annotate(count=Count('id'))
        .order_by('-count')[:5]
    )
    
    labels = [d['category'] if d['category'] else "Інше" for d in data]
    values = [d['count'] for d in data]

    return {
        "labels": labels,
        "datasets": [
            {
                "label": "Статей у категорії",
                "data": values,
                "borderColor": "#9333ea",
                "backgroundColor": "rgba(147, 51, 234, 0.1)",
                "fill": True,
                "tension": 0.4, # Робимо лінію плавною
            }
        ],
    }
