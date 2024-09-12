
from django.urls import path

from pokemon.views import PokemonView, PokemonSingleView, FileUploadView, FileUploadSingleView, HealthCheckView

urlpatterns = [
    path('health/', HealthCheckView.as_view(), name='health-check'),
    path("file_upload/", FileUploadView.as_view(), name="file_upload"),
    path('file_upload/<int:id>/', FileUploadSingleView.as_view(), name="file_upload_single"),
    path("pokemon/", PokemonView.as_view(), name="pokemon"),
    path('pokemon/<int:id>/', PokemonSingleView.as_view(), name="pokemon_single"),
]
