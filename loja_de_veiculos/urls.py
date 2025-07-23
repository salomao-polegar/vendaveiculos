from django.urls import path, include
from django.shortcuts import redirect
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="Minha API",
      default_version='v1',
      description="Documentação Swagger da API",
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)
urlpatterns = [
    path('', lambda request: redirect('swagger/', permanent=False)),  # redireciona para /swagger/

    path('veiculos/', include('veiculos.urls')),
    path('pessoas/', include('pessoas.urls')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]