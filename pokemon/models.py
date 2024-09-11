from django.contrib.auth.models import User
from django.db import models

from pokemon.choices import GrowthRate

from taggit.managers import TaggableManager
from taggit.models import TaggedItemBase, ItemBase


class TypeTag(TaggedItemBase):
    content_object = models.ForeignKey('Pokemon', on_delete=models.CASCADE, default="")


class AbilitiesTag(TaggedItemBase):
    content_object = models.ForeignKey('Pokemon', on_delete=models.CASCADE, default="")


class EggGroupsTag(TaggedItemBase):
    content_object = models.ForeignKey('Pokemon', on_delete=models.CASCADE, default="")


class EVYieldTag(TaggedItemBase):
    content_object = models.ForeignKey('Pokemon', on_delete=models.CASCADE, default="")


class TimestampModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True


class Pokemon(TimestampModel):
    name = models.CharField(max_length=200, null=False, blank=False, db_index=True)
    type = TaggableManager(through=TypeTag, related_name="type_tag", verbose_name="Type")
    abilities = TaggableManager(through=AbilitiesTag, related_name="abilities_tag", verbose_name="Abilities")
    egg_groups = TaggableManager(through=EggGroupsTag, related_name="egg_groups_tag", verbose_name="Egg Groups")
    ev_yield = TaggableManager(through=EVYieldTag, related_name="ev_yield_tag", verbose_name="EV Yield")
    species = models.CharField(max_length=200, null=True, blank=True)
    height = models.FloatField(null=True)
    weight = models.FloatField(null=True)
    growth_rate = models.CharField(max_length=200, null=True, blank=True, choices=GrowthRate.CHOICES)


class FileUpload(TimestampModel):
    file_label = models.CharField(null=True, default=None, max_length=500)
    file_url = models.CharField(null=True, default=None, max_length=1000)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    pokemon = models.ForeignKey(Pokemon, null=True, on_delete=models.SET_NULL)

