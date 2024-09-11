from django.contrib import admin
from django.utils.html import format_html

from pokemon.models import Pokemon, FileUpload


class FileUploadInline(admin.TabularInline):
    model = FileUpload
    extra = 0
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        return format_html('<img src="{}" width="200" height="200" />'.format(obj.file_url))

    image_preview.short_description = 'Image Preview'


class PokemonAdmin(admin.ModelAdmin):
    list_display = ['name', 'type_list', 'weight', 'height', 'abilities_list', 'show_images']
    search_fields = ['name']
    inlines = [FileUploadInline]

    def show_images(self, obj):
        images = obj.fileupload_set.all()  # Get all related images
        image_list = [format_html('<img src="{}" width="50" height="50" />'.format(image.file_url)) for image in images]
        return format_html(" ".join(image_list))

    show_images.short_description = 'Images'

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('type', 'abilities', 'egg_groups', 'ev_yield', 'fileupload_set').all()

    def type_list(self, obj):
        return u", ".join(o.name for o in obj.type.all())

    def abilities_list(self, obj):
        return u", ".join(o.name for o in obj.abilities.all())


class FileUploadAdmin(admin.ModelAdmin):
    list_display = ('pokemon__name', 'image_thumbnail')
    search_fields = ['pokemon__name']

    def image_thumbnail(self, obj):
        return format_html('<img src="{}" width="100" height="100" />'.format(obj.file_url))

    image_thumbnail.short_description = 'Image Preview'


admin.site.register(Pokemon, PokemonAdmin)
admin.site.register(FileUpload, FileUploadAdmin)
