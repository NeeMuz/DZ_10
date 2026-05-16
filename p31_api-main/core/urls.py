from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from graphene_django.views import GraphQLView

PREFIX = 'api/v1'

urlpatterns = [
    path('admin/', admin.site.urls),
    path(f'{PREFIX}/news/', include('news.urls')),
    path(f'{PREFIX}/auth/', include('authentication.urls')),

    path("graphql/", GraphQLView.as_view(graphiql=True)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
