import json, re

from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError

from PIL import Image as PilImage
from django.forms.models import model_to_dict

from shop.models import Tinker

def validate_not_zero(value):
    if value == 0:
        raise ValidationError('{} is zero'.format(value))

def is_rgb_color(value):
	if not value or not len(value): raise ValidationError("Color is missing")
	if value[0] != "#": raise ValidationError("Leading '#' is missing")
	if not len(value) in [4, 7]: raise ValidationError("Length is incorrect")

	print(re.search("^#[0-9a-fA-F]+$", value))
	return not not re.search("^#[0-9a-fA-F]+$", value)

def validate_angle_multiple_90(value):
    if value % 90 != 0:
        raise ValidationError(
            '{} is not an angle which is a multiple of 90°'.format(value),
            params={'value': value},
        )



class Region(models.Model):
	class Meta:
		verbose_name = "Region"
		verbose_name_plural = "Regionen"
		ordering = ["name"]

	name = models.CharField(max_length=200, unique=True)
	layer_index_of_char = models.SmallIntegerField(default=0, validators=[MinValueValidator(-100), MaxValueValidator(100)])
	bg_color_rgb = models.CharField(default="#b9fefd", max_length=7, validators=[is_rgb_color])

	def __str__(self):
		return "Region {}".format(self.name)


class Layer(models.Model):
	class Meta:
		verbose_name = "Layer"
		verbose_name_plural = "Layers"

		unique_together = ["region", "index"]
		ordering = ["region", "index"]

	region = models.ForeignKey(Region, on_delete=models.CASCADE)
	index = models.SmallIntegerField(validators=[MinValueValidator(-100), MaxValueValidator(100)])

	name = models.CharField(max_length=200)

	is_collidable = models.BooleanField(default=True)
	is_breakable = models.BooleanField(default=True)

	def __str__(self):
		return "Layer {} ({}) of {}".format(self.index, self.name, self.region.name)

	def toDict(self):
		l = model_to_dict(self)
		l["entities"] = [entity.toDict() for entity in self.entity_set.all()]
		return l



class Material(models.Model):
	class Meta:
		verbose_name = "Material"
		verbose_name_plural = "Materialien"

	name = models.CharField(max_length=200)
	icon = models.ImageField(null=False, blank=False)
	
	rigidity = models.PositiveIntegerField(default=10, null=False, blank=False)
	tier = models.PositiveIntegerField(default=0, null=False, blank=False)

	def __str__(self):
		return "{}".format(self.name)

	# resize icon
	def save(self, *args, **kwargs):
		MAX_SIZE = 1024

		super().save(*args, **kwargs)

		# proceed only if an image exists
		if not self.icon or not self.icon.path: return

		icon = PilImage.open(self.icon.path)

		# is smaller, leave it
		if icon.height <= MAX_SIZE and icon.width <= MAX_SIZE:
			return

		# resize, longest is MAX_SIZE, scale the other accordingly while maintaining ratio
		new_width = MAX_SIZE if icon.width >= icon.height else icon.width * MAX_SIZE // icon.height
		new_height = MAX_SIZE if icon.width <= icon.height else icon.height * MAX_SIZE // icon.width

		icon.thumbnail((new_width, new_height), PilImage.BILINEAR)
		icon.save(self.icon.path, "png")

	def w(self):
		if not self.icon or not self.icon.path: return 0
		return PilImage.open(self.icon.path).width

	def h(self):
		if not self.icon or not self.icon.path: return 0
		return PilImage.open(self.icon.path).height

	def toDict(self):
		m = model_to_dict(self)
		m["icon"] = self.icon.url
		m["h"] = self.h()
		m["w"] = self.w()
		return m

class MaterialDrop(models.Model):
	item = models.ForeignKey(Tinker, on_delete=models.CASCADE, blank=False, null=True)
	amount = models.TextField(default="[1]")
	material = models.ForeignKey(Material, on_delete=models.CASCADE)

class MaterialGroup(models.Model):

	class Meta:
		verbose_name = "Materialgruppe"
		verbose_name_plural = "Materialgruppen"

		ordering = ["name"]

	name = models.CharField(max_length=200)
	materials = models.ManyToManyField(Material)

	def __str__(self):
		return "Materialgruppe {}".format(self.name)


class Entity(models.Model):
	class Meta:
		verbose_name = "Objekt"
		verbose_name_plural = "Objekte"

		ordering = ["layer", "x", "y"]

	material = models.ForeignKey(Material, on_delete=models.CASCADE)
	layer = models.ForeignKey(Layer, on_delete=models.CASCADE)

	x = models.PositiveSmallIntegerField(default=0)
	y = models.PositiveSmallIntegerField(default=0)

	mirrored = models.BooleanField(default=False)
	rotation_angle = models.PositiveSmallIntegerField(default=0, validators=[validate_angle_multiple_90, MaxValueValidator(3)])
	scale = models.FloatField(default=1.0)


	def __str__(self):
		return "Objekt {} in Layer {} von {}".format(self.material.name, self.layer.index, self.layer.region.name)
	
	def w(self):
		return self.material.w() * self.scale

	def h(self):
		return self.material.h() * self.scale

	def toDict(self):
		e = model_to_dict(self)
		e["w"] = self.material.w()
		e["h"] = self.material.h()
		e["material"] = self.material.toDict()
		return e
