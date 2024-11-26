from django.contrib import admin
from django.db import transaction
from django.urls import path, re_path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_yasg import openapi
from django.views.static import serve
from drf_yasg.views import get_schema_view
from rest_framework import permissions

admin.site.site_header = 'Tavilot Al-Quran Admin'
admin.site.site_title = 'Tavilot Al-Quran Admin'
admin.site.index_title = 'Welcome to dashboard'

schema_view = get_schema_view(
    openapi.Info(
        title="Tavilot Al-Quran APIv1",
        default_version="v1",
        description="API for project Tavilot Al-Quran",
        terms_of_service="",
        contact=openapi.Contact(email="odiljonabduvaitov@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('transaction/', include('pyment.urls')),
    path('api/v1/', include('tavilot.urls')),
    path('api/v1/auth/', include('authentication.urls')),
    path('tinymce/', include('tinymce.urls')),

    re_path(r'static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
    re_path(r'media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]

if settings.SHOW_SWAGGER:
    urlpatterns +=[
    re_path(
        r"^swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    re_path(
        r"^swagger/$",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    re_path(
        r"^redoc/$", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"
    )
    ]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
