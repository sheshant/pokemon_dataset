from http import HTTPStatus

from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django_filters import rest_framework as filters

from pokemon.filters import PokemonFilter
from pokemon.models import Pokemon, FileUpload
from pokemon.serializers import PokemonSerializer, FileUploadSerializer
from pokemon.upload_utils.upload_to_s3_utils import UploadToS3


class PokemonView(ListCreateAPIView):
    serializer_class = PokemonSerializer
    pagination_class = PageNumberPagination
    permission_classes = IsAuthenticated,
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = PokemonFilter
    queryset = Pokemon.objects.prefetch_related('type', 'abilities', 'egg_groups', 'ev_yield', 'fileupload_set').all()
    
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


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
