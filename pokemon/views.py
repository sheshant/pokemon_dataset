from http import HTTPStatus

from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django_filters import rest_framework as filters
from rest_framework.views import APIView

from pokemon.filters import PokemonFilter
from pokemon.models import Pokemon, FileUpload
from pokemon.serializers import PokemonSerializer, FileUploadSerializer
from pokemon.upload_utils.upload_to_s3_utils import UploadToS3
from pokemon.utils import PokemonUtils


class HealthCheckView(APIView):
    permission_classes = AllowAny,

    def get(self, request, *args, **kwargs):
        data = {
            'status': 'ok',
            'database': 'connected',
            'cache': 'connected',
            # Add other checks as needed
        }
        return Response(data, status=status.HTTP_200_OK)


class PokemonView(ListCreateAPIView):
    serializer_class = PokemonSerializer
    pagination_class = PageNumberPagination
    permission_classes = IsAuthenticated,
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = PokemonFilter
    queryset = Pokemon.objects.prefetch_related('type', 'abilities', 'egg_groups', 'ev_yield', 'fileupload_set').all()
    
    def post(self, request, *args, **kwargs):
        status, pokemon, message = PokemonUtils.create_update_pokemon(
            name=request.data.get('name'),
            species=request.data.get('species'),
            height=request.data.get('height'),
            weight=request.data.get('weight'),
            growth_rate=request.data.get('growth_rate'),
            type=request.data.get('type', '').split(',') or None,
            abilities=request.data.get('abilities', '').split(',') or None,
            egg_groups=request.data.get('egg_groups', '').split(',') or None,
            ev_yield=request.data.get('ev_yield', '').split(',') or None,
        )
        if status:
            for label, file in request.FILES.items():
                status, file_upload, upload_message = UploadToS3.upload_file(
                    label=label,
                    user_id=request.user and request.user.pk,
                    file_object=file.file,
                    name=file.name,
                    pokemon=pokemon
                )
            return Response(status=HTTPStatus.CREATED, data={"statuas": "success", "message": message,
                                                             "data": self.serializer_class(pokemon).data})

        return Response(status=HTTPStatus.BAD_REQUEST, data={"statuas": "error", "message": message,
                                                             "data": {}})


class PokemonSingleView(RetrieveUpdateDestroyAPIView):
    serializer_class = PokemonSerializer
    pagination_class = PageNumberPagination
    permission_classes = IsAuthenticated,
    queryset = Pokemon.objects.prefetch_related('type', 'abilities', 'egg_groups', 'ev_yield', 'fileupload_set').all()
    lookup_field = "id"


class FileUploadView(ListCreateAPIView):
    serializer_class = FileUploadSerializer
    pagination_class = PageNumberPagination
    permission_classes = IsAuthenticated,
    queryset = FileUpload.objects.all()

    def post(self, request, *args, **kwargs):

        for label, file in request.FILES.items():
            try:
                status, file_upload, message = UploadToS3.upload_file(
                    label=label,
                    user_id=request.user and request.user.pk,
                    file_object=file.file,
                    name=file.name
                )
                if status and file_upload:
                    return Response({"status": "success", "data": FileUploadSerializer(file_upload).data})
                return Response({"status": "error", "message": message}, status=HTTPStatus.BAD_REQUEST)
            except Exception as e:
                raise e
        return Response()


class FileUploadSingleView(RetrieveUpdateDestroyAPIView):
    serializer_class = FileUploadSerializer
    pagination_class = PageNumberPagination
    permission_classes = IsAuthenticated,
    queryset = FileUpload.objects.all()
    lookup_field = "id"
