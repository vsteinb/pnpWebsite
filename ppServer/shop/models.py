from itertools import chain
from PIL import Image as PilImage

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.urls import reverse

from . import enums


# Firma
class Firma(models.Model):
    class Meta:
        ordering = ['name']
        verbose_name = "Firma"
        verbose_name_plural = "Firmen"

    name = models.CharField(max_length=50, default='')
    beschreibung = models.TextField(max_length=1000, default='', blank=True)

    def __str__(self):
        return "{}".format(self.name)


############# FirmaShop #####################

class FirmaShop(models.Model):
    class Meta:
        abstract = True
        ordering = ['item', 'firma']
        verbose_name = "Firma"
        verbose_name_plural = "Firmen"

    firma = models.ForeignKey(Firma, on_delete=models.CASCADE)
    preis = models.IntegerField(default=0, null=True)

    verfügbarkeit = models.PositiveIntegerField(default=0)

    def __str__(self):
        return "{} von {} ({}%)".format(self.item, self.firma, self.verfügbarkeit)


class FirmaItem(FirmaShop):
    item = models.ForeignKey('Item', on_delete=models.CASCADE)


class FirmaWaffen_Werkzeuge(FirmaShop):
    item = models.ForeignKey('Waffen_Werkzeuge', on_delete=models.CASCADE)


class FirmaMagazin(FirmaShop):
    item = models.ForeignKey('Magazin', on_delete=models.CASCADE)


class FirmaPfeil_Bolzen(FirmaShop):
    item = models.ForeignKey('Pfeil_Bolzen', on_delete=models.CASCADE)


class FirmaSchusswaffen(FirmaShop):
    item = models.ForeignKey('Schusswaffen', on_delete=models.CASCADE)


class FirmaMagische_Ausrüstung(FirmaShop):
    item = models.ForeignKey('Magische_Ausrüstung', on_delete=models.CASCADE)


class FirmaRituale_Runen(models.Model):
    class Meta:
        verbose_name = "Firma"
        verbose_name_plural = "Firmen"

    firma = models.ForeignKey(Firma, on_delete=models.CASCADE)
    item = models.ForeignKey('Rituale_Runen', on_delete=models.CASCADE)

    stufe_1 = models.IntegerField(default=0, null=True)
    stufe_2 = models.IntegerField(default=0, null=True)
    stufe_3 = models.IntegerField(default=0, null=True)
    stufe_4 = models.IntegerField(default=0, null=True)
    stufe_5 = models.IntegerField(default=0, null=True)


    verfügbarkeit = models.PositiveIntegerField(default=0)

    def __str__(self):
        return "{} von {} ({}%)".format(self.item, self.firma, self.verfügbarkeit)


class FirmaRüstungen(FirmaShop):
    item = models.ForeignKey('Rüstungen', on_delete=models.CASCADE)


class FirmaAusrüstung_Technik(FirmaShop):
    item = models.ForeignKey('Ausrüstung_Technik', on_delete=models.CASCADE)


class FirmaFahrzeug(FirmaShop):
    item = models.ForeignKey('Fahrzeug', on_delete=models.CASCADE)


class FirmaEinbauten(FirmaShop):
    item = models.ForeignKey('Einbauten', on_delete=models.CASCADE)


class FirmaZauber(FirmaShop):
    item = models.ForeignKey('Zauber', on_delete=models.CASCADE)


class FirmaVergessenerZauber(FirmaShop):
    item = models.ForeignKey('VergessenerZauber', on_delete=models.CASCADE)


class FirmaAlchemie(FirmaShop):
    item = models.ForeignKey('Alchemie', on_delete=models.CASCADE)


class FirmaTinker(FirmaShop):
    item = models.ForeignKey('Tinker', on_delete=models.CASCADE)

################ Base Shop ####################

class BaseShop(models.Model):
    class Meta:
        abstract = True

    name = models.CharField(max_length=50, default='', unique=True)
    beschreibung = models.TextField(max_length=1500, default='', blank=True)
    icon = models.ImageField(null=True, blank=True)

    ab_stufe = models.IntegerField(default=0, validators=[MinValueValidator(0)], blank=True)
    illegal = models.BooleanField(default=False)
    lizenz_benötigt = models.BooleanField(default=False)

    frei_editierbar = models.BooleanField(default=True)
    stufenabhängig = models.BooleanField(default=False)


    @staticmethod
    def get_table_headings():
        return [
            {"headerName": "Icon", "field": "icon", "type": "image"},
            {"headerName": "Name", "field": "name", "type": "text"},
            {"headerName": "Beschreibung", "field": "beschreibung", "type": "text--long"},
            {"headerName": "Ab Stufe", "field": "ab_stufe", "type": "number"},
            {"headerName": "Günstigster Preis", "field": "billigster", "type": "price"},
            {"headerName": "Weiteres", "field": "weiteres", "type": "text"},
            {"headerName": "Preis * Stufe?", "field": "stufenabhängig", "type": "boolean"}
        ]

    @classmethod
    def get_all_serialized(cls, url_prefix=None):
        fields = [heading["field"] for heading in cls.get_table_headings()] + ["pk"]

        objects = cls.objects.filter(frei_editierbar=False)
        if len(objects) == 0: return []

        firma_model = objects[0].firmen.through

        serialized = []

        for object in objects:
            object_dict = object.__dict__

            serialized_object = {}
            for field in fields:
                serialized_object[field] = object_dict[field] if field in object_dict else None

            # add pk
            serialized_object["pk"] = object.pk

            # add "weiteres"
            weiteres = "illegal" if object.illegal else ""
            if object.lizenz_benötigt and not weiteres: weiteres = "Lizenz"
            if object.lizenz_benötigt and object.illegal: weiteres += ", Lizenz"

            serialized_object["weiteres"] = weiteres


            # add "billigster"
            billigster = firma_model.objects.filter(item=object).order_by("preis").first()
            billigster_preis = billigster.preis if billigster else None
            serialized_object["billigster"] = billigster_preis

            
            # add "icon"
            serialized_object["icon"] = object.getIconUrl()

            # add "url"
            serialized_object["url"] = reverse(url_prefix, args=[object.pk]) if url_prefix else None

            serialized.append(serialized_object)

        return serialized


    def getIconUrl(self):
        return self.icon.url if self.icon else "/static/res/img/icon-dice-account.svg"


    # resize icon
    def save(self, *args, **kwargs):
        MAX_SIZE = 64

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
        icon.save(self.icon.path)


class Item(BaseShop):
    class Meta:
        verbose_name = "Item"
        verbose_name_plural = "Items"

        ordering = ['name']

    kategorie = models.CharField(choices=enums.item_enum, max_length=2, default=enums.item_enum[0][0])
    firmen = models.ManyToManyField('Firma', through='FirmaItem', blank=True, related_name='firmen')

    def __str__(self):
        return "{} (item)".format(self.name)

    @classmethod
    def get_all_serialized(cls, url_prefix="shop:buy_item"):
        return super().get_all_serialized(url_prefix)


class Waffen_Werkzeuge(BaseShop):
    class Meta:
        verbose_name = "Waffe/Werkzeug"
        verbose_name_plural = "Waffen & Werkzeuge"

        ordering = ['name']

    erfolge = models.PositiveIntegerField(default=0)
    bs = models.CharField(max_length=20, default=0)
    zs = models.CharField(max_length=20, default=0)
    dk = models.PositiveIntegerField(default=0, blank=True, null=True)

    kategorie = models.CharField(choices=enums.werkzeuge_enum, max_length=2, default=enums.werkzeuge_enum[0][0])
    firmen = models.ManyToManyField('Firma', through='FirmaWaffen_Werkzeuge', blank=True)

    def __str__(self):
        return "{} (Waffen & Werkzeuge)".format(self.name)
    
    @staticmethod
    def get_table_headings():
        return [
            {"headerName": "Icon", "field": "icon", "type": "image"},
            {"headerName": "Name", "field": "name", "type": "text"},
            {"headerName": "Beschreibung", "field": "beschreibung", "type": "text--long"},
            {"headerName": "Ab Stufe", "field": "ab_stufe", "type": "number"},
            {"headerName": "Erfolge", "field": "erfolge", "type": "number"},
            {"headerName": "BS", "field": "bs", "type": "text"},
            {"headerName": "ZS", "field": "zs", "type": "text"},
            {"headerName": "DK", "field": "dk", "type": "number"},
            {"headerName": "Günstigster Preis", "field": "billigster", "type": "price"},
            {"headerName": "Weiteres", "field": "weiteres", "type": "text"},
            {"headerName": "Preis * Stufe?", "field": "stufenabhängig", "type": "boolean"}
        ]

    @classmethod
    def get_all_serialized(cls, url_prefix="shop:buy_waffen_werkzeuge"):
        return super().get_all_serialized(url_prefix)


class Magazin(BaseShop):
    class Meta:
        verbose_name = "Magazin"
        verbose_name_plural = "Magazine"

        ordering = ['name']

    schuss = models.PositiveIntegerField(default=0)
    firmen = models.ManyToManyField('Firma', through='FirmaMagazin', blank=True)

    def __str__(self):
        return "{}, {} Schuss (Magazine)".format(self.name, self.schuss)

    @staticmethod
    def get_table_headings():
        return [
            {"headerName": "Icon", "field": "icon", "type": "image"},
            {"headerName": "Name", "field": "name", "type": "text"},
            {"headerName": "Beschreibung", "field": "beschreibung", "type": "text--long"},
            {"headerName": "Ab Stufe", "field": "ab_stufe", "type": "number"},
            {"headerName": "Schuss", "field": "schuss", "type": "number"},
            {"headerName": "Günstigster Preis", "field": "billigster", "type": "price"},
            {"headerName": "Weiteres", "field": "weiteres", "type": "text"},
            {"headerName": "Preis * Stufe?", "field": "stufenabhängig", "type": "boolean"}
        ]

    @classmethod
    def get_all_serialized(cls, url_prefix="shop:buy_magazine"):
        return super().get_all_serialized(url_prefix)


class Pfeil_Bolzen(BaseShop):
    class Meta:
        verbose_name = "Pfeil/Bolzen"
        verbose_name_plural = "Pfeile & Bolzen"

        ordering = ['name']

    bs = models.CharField(max_length=20, default='')
    zs = models.CharField(max_length=20, default='')
    firmen = models.ManyToManyField('Firma', through='FirmaPfeil_Bolzen', blank=True)

    def __str__(self):
        return "{} (Pfeile & Bolzen)".format(self.name)
    
    @staticmethod
    def get_table_headings():
        return [
            {"headerName": "Icon", "field": "icon", "type": "image"},
            {"headerName": "Name", "field": "name", "type": "text"},
            {"headerName": "Beschreibung", "field": "beschreibung", "type": "text--long"},
            {"headerName": "Ab Stufe", "field": "ab_stufe", "type": "number"},
            {"headerName": "BS", "field": "bs", "type": "text"},
            {"headerName": "ZS", "field": "zs", "type": "text"},
            {"headerName": "Günstigster Preis", "field": "billigster", "type": "price"},
            {"headerName": "Weiteres", "field": "weiteres", "type": "text"},
            {"headerName": "Preis * Stufe?", "field": "stufenabhängig", "type": "boolean"}
        ]

    @classmethod
    def get_all_serialized(cls, url_prefix="shop:buy_pfeil_bolzen"):
        return super().get_all_serialized(url_prefix)


class Schusswaffen(BaseShop):
    class Meta:
        verbose_name = "Schusswaffe"
        verbose_name_plural = "Schusswaffen"

        ordering = ['name']

    erfolge = models.PositiveIntegerField(default=0)
    bs = models.CharField(max_length=20, default='')
    zs = models.CharField(max_length=20, default='')

    magazine = models.ManyToManyField(Magazin, blank=True)
    pfeile_bolzen = models.ManyToManyField(Pfeil_Bolzen, blank=True)

    dk = models.PositiveIntegerField(default=0, blank=True)
    präzision = models.PositiveIntegerField(default=0, blank=True)

    kategorie = models.CharField(choices=enums.schusswaffen_enum, max_length=2, default=enums.schusswaffen_enum[0][0])
    firmen = models.ManyToManyField('Firma', through='FirmaSchusswaffen', blank=True)

    def __str__(self):
        return "{} (Schusswaffen)".format(self.name)

    @staticmethod
    def get_table_headings():
        return [
            {"headerName": "Icon", "field": "icon", "type": "image"},
            {"headerName": "Name", "field": "name", "type": "text"},
            {"headerName": "Beschreibung", "field": "beschreibung", "type": "text--long"},
            {"headerName": "Ab Stufe", "field": "ab_stufe", "type": "number"},
            {"headerName": "Erfolge", "field": "erfolge", "type": "number"},
            {"headerName": "BS", "field": "bs", "type": "text"},
            {"headerName": "ZS", "field": "zs", "type": "text"},
            {"headerName": "DK", "field": "dk", "type": "number"},
            {"headerName": "Präzision", "field": "präzision", "type": "number"},
            {"headerName": "Munition", "field": "munition", "type": "text"},
            {"headerName": "Günstigster Preis", "field": "billigster", "type": "price"},
            {"headerName": "Weiteres", "field": "weiteres", "type": "text"},
            {"headerName": "Preis * Stufe?", "field": "stufenabhängig", "type": "boolean"}
        ]
    
    @classmethod
    def get_all_serialized(cls, url_prefix=None):
        fields = [heading["field"] for heading in cls.get_table_headings()] + ["pk"]

        objects = cls.objects.filter(frei_editierbar=False)
        if len(objects) == 0: return []

        firma_model = objects[0].firmen.through

        serialized = []

        for object in objects:
            object_dict = object.__dict__

            serialized_object = {}
            for field in fields:
                serialized_object[field] = object_dict[field] if field in object_dict else None

            # add pk
            serialized_object["pk"] = object.pk

            # add "weiteres"
            weiteres = "illegal" if object.illegal else ""
            if object.lizenz_benötigt and not weiteres: weiteres = "Lizenz"
            if object.lizenz_benötigt and object.illegal: weiteres += ", Lizenz"

            serialized_object["weiteres"] = weiteres

            # add "munition"
            serialized_object["munition"] = ", ".join([m.name for m in chain(object.magazine.all(), object.pfeile_bolzen.all())])


            # add "billigster"
            billigster = firma_model.objects.filter(item=object).order_by("preis").first()
            billigster_preis = billigster.preis if billigster else None
            serialized_object["billigster"] = billigster_preis

            
            # add "icon"
            serialized_object["icon"] = object.getIconUrl()

            # add "url"
            serialized_object["url"] = reverse(url_prefix, args=[object.pk]) if url_prefix else None

            serialized.append(serialized_object)

        return serialized


class Magische_Ausrüstung(BaseShop):
    class Meta:
        verbose_name = "magische Ausrüstung"
        verbose_name_plural = "magische Ausrüstung"

        ordering = ['name']

    kategorie = models.CharField(choices=enums.magische_Ausrüstung_enum, max_length=2, default=enums.magische_Ausrüstung_enum[0][0])
    firmen = models.ManyToManyField('Firma', through='FirmaMagische_Ausrüstung', blank=True)

    def __str__(self):
        return "{} (Magische Ausrüstung)".format(self.name)

    @classmethod
    def get_all_serialized(cls, url_prefix="shop:buy_mag_ausrüstung"):
        return super().get_all_serialized(url_prefix)


class Rituale_Runen(BaseShop):
    class Meta:
        verbose_name = "Ritual/Rune"
        verbose_name_plural = "Rituale & Runen"

        ordering = ['name']

    kategorie = models.CharField(choices=enums.rituale_enum, max_length=2, default=enums.rituale_enum[0][0])
    firmen = models.ManyToManyField('Firma', through='FirmaRituale_Runen', blank=True)

    def __str__(self):
        return "{} (Rituale & Runen)".format(self.name)

    @staticmethod
    def get_table_headings():
        return [
            {"headerName": "Icon", "field": "icon", "type": "image"},
            {"headerName": "Name", "field": "name", "type": "text"},
            {"headerName": "Beschreibung", "field": "beschreibung", "type": "text--long"},
            {"headerName": "Ab Stufe", "field": "ab_stufe", "type": "number"},
            {"headerName": "Stufe 1", "field": "stufe1", "type": "price"},
            {"headerName": "Stufe 2", "field": "stufe2", "type": "price"},
            {"headerName": "Stufe 3", "field": "stufe3", "type": "price"},
            {"headerName": "Stufe 4", "field": "stufe4", "type": "price"},
            {"headerName": "Stufe 5", "field": "stufe5", "type": "price"},
            {"headerName": "Weiteres", "field": "weiteres", "type": "text"}
        ]
    
    @classmethod
    def get_all_serialized(cls, url_prefix=None):
        fields = [heading["field"] for heading in cls.get_table_headings()] + ["pk"]

        objects = cls.objects.filter(frei_editierbar=False)
        if len(objects) == 0: return []

        firma_model = objects[0].firmen.through

        serialized = []

        for object in objects:
            object_dict = object.__dict__

            serialized_object = {}
            for field in fields:
                serialized_object[field] = object_dict[field] if field in object_dict else None

            # add pk
            serialized_object["pk"] = object.pk

            # add "weiteres"
            weiteres = "illegal" if object.illegal else ""
            if object.lizenz_benötigt and not weiteres: weiteres = "Lizenz"
            if object.lizenz_benötigt and object.illegal: weiteres += ", Lizenz"

            serialized_object["weiteres"] = weiteres


            # add "billigster"
            if firma_model.objects.filter(item=object).count():
                serialized_object["stufe1"] = firma_model.objects.filter(item=object).order_by("stufe_1").first().stufe_1
                serialized_object["stufe2"] = firma_model.objects.filter(item=object).order_by("stufe_2").first().stufe_2
                serialized_object["stufe3"] = firma_model.objects.filter(item=object).order_by("stufe_3").first().stufe_3
                serialized_object["stufe4"] = firma_model.objects.filter(item=object).order_by("stufe_4").first().stufe_4
                serialized_object["stufe5"] = firma_model.objects.filter(item=object).order_by("stufe_5").first().stufe_5

            # add "icon"
            serialized_object["icon"] = object.getIconUrl()

            # add "url"
            serialized_object["url"] = reverse(url_prefix, args=[object.pk]) if url_prefix else None

            serialized.append(serialized_object)

        return serialized


class Rüstungen(BaseShop):
    class Meta:
        verbose_name = "Rüstung"
        verbose_name_plural = "Rüstung"

        ordering = ['name']

    schutz = models.PositiveIntegerField(default=0)
    stärke = models.PositiveIntegerField(default=0)
    haltbarkeit = models.PositiveIntegerField(default=0)

    firmen = models.ManyToManyField('Firma', through='FirmaRüstungen', blank=True)

    def __str__(self):
        return "{} (Rüstungen)".format(self.name)
    
    @staticmethod
    def get_table_headings():
        return [
            {"headerName": "Icon", "field": "icon", "type": "image"},
            {"headerName": "Name", "field": "name", "type": "text"},
            {"headerName": "Beschreibung", "field": "beschreibung", "type": "text--long"},
            {"headerName": "Ab Stufe", "field": "ab_stufe", "type": "number"},
            {"headerName": "Schutz", "field": "schutz", "type": "number"},
            {"headerName": "Stärke", "field": "stärke", "type": "number"},
            {"headerName": "Haltbarkeit", "field": "haltbarkeit", "type": "number"},
            {"headerName": "Günstigster Preis", "field": "billigster", "type": "price"},
            {"headerName": "Weiteres", "field": "weiteres", "type": "text"},
            {"headerName": "Preis * Stufe?", "field": "stufenabhängig", "type": "boolean"}
        ]

    @classmethod
    def get_all_serialized(cls, url_prefix="shop:buy_rüstungen"):
        return super().get_all_serialized(url_prefix)


class Ausrüstung_Technik(BaseShop):
    class Meta:
        verbose_name = "Ausrüstung/Technik"
        verbose_name_plural = "Ausrüstung & Technik"

        ordering = ['name']

    manifestverlust_str = models.CharField(max_length=20, null=True, blank=True)
    manifestverlust = models.DecimalField('manifestverlust', max_digits=4, decimal_places=2,
                                          default=0.0, blank=True, null=True,
                                          validators=[MinValueValidator(0), MaxValueValidator(10)])
    kategorie = models.CharField(choices=enums.ausrüstung_enum, max_length=2, default=enums.ausrüstung_enum[0][0])
    firmen = models.ManyToManyField('Firma', through='FirmaAusrüstung_Technik', blank=True)

    def __str__(self):
        return "{} (Ausrüstung & Technik)".format(self.name)

    @classmethod
    def get_all_serialized(cls, url_prefix="shop:buy_ausrüstung_technik"):
        return super().get_all_serialized(url_prefix)


class Fahrzeug(BaseShop):
    class Meta:
        verbose_name = "Fahrzeug"
        verbose_name_plural = "Fahrzeuge"

        ordering = ['name']

    schnelligkeit = models.PositiveIntegerField(blank=True, null=True)
    rüstung = models.PositiveIntegerField(blank=True, null=True)
    erfolge = models.PositiveIntegerField(default=0, blank=True, null=True)

    kategorie = models.CharField(choices=enums.fahrzeuge_enum, max_length=2, default=enums.fahrzeuge_enum[0][0])
    firmen = models.ManyToManyField('Firma', through='FirmaFahrzeug', blank=True)

    def __str__(self):
        return "{} (Fahrzeuge)".format(self.name)
    
    @staticmethod
    def get_table_headings():
        return [
            {"headerName": "Icon", "field": "icon", "type": "image"},
            {"headerName": "Name", "field": "name", "type": "text"},
            {"headerName": "Beschreibung", "field": "beschreibung", "type": "text--long"},
            {"headerName": "Ab Stufe", "field": "ab_stufe", "type": "number"},
            {"headerName": "Schnelligkeit", "field": "schnelligkeit", "type": "number"},
            {"headerName": "Rüstung", "field": "rüstung", "type": "number"},
            {"headerName": "Erfolge", "field": "erfolge", "type": "number"},
            {"headerName": "Günstigster Preis", "field": "billigster", "type": "price"},
            {"headerName": "Weiteres", "field": "weiteres", "type": "text"},
            {"headerName": "Preis * Stufe?", "field": "stufenabhängig", "type": "boolean"}
        ]
    
    @classmethod
    def get_all_serialized(cls, url_prefix="shop:buy_fahrzeug"):
        return super().get_all_serialized(url_prefix)


class Einbauten(BaseShop):
    class Meta:
        verbose_name = "Einbauten"
        verbose_name_plural = "Einbauten"

        ordering = ['name']

    manifestverlust = models.CharField(max_length=20, null=True, blank=True)
    kategorie = models.CharField(choices=enums.einbauten_enum, max_length=2, default=enums.einbauten_enum[0][0])
    firmen = models.ManyToManyField('Firma', through='FirmaEinbauten', blank=True)

    def __str__(self):
        return "{} (Einbauten)".format(self.name)

    @staticmethod
    def get_table_headings():
        return [
            {"headerName": "Icon", "field": "icon", "type": "image"},
            {"headerName": "Name", "field": "name", "type": "text"},
            {"headerName": "Beschreibung", "field": "beschreibung", "type": "text--long"},
            {"headerName": "Ab Stufe", "field": "ab_stufe", "type": "number"},
            {"headerName": "Manifestverlust", "field": "manifestverlust", "type": "text"},
            {"headerName": "Günstigster Preis", "field": "billigster", "type": "price"},
            {"headerName": "Weiteres", "field": "weiteres", "type": "text"},
            {"headerName": "Preis * Stufe?", "field": "stufenabhängig", "type": "boolean"}
        ]
    
    @classmethod
    def get_all_serialized(cls, url_prefix="shop:buy_einbauten"):
        return super().get_all_serialized(url_prefix)


class Zauber(BaseShop):
    class Meta:
        verbose_name = "Zauber"
        verbose_name_plural = "Zauber"

        ordering = ['name']

    schaden = models.CharField(max_length=100, default='', null=True, blank=True)
    astralschaden = models.CharField(max_length=100, default='', null=True, blank=True)
    manaverbrauch = models.CharField(max_length=100, default='', null=True, blank=True)

    kategorie = models.CharField(choices=enums.zauber_enum, max_length=2, null=True, blank=True)
    flächenzauber = models.BooleanField(default=False)

    firmen = models.ManyToManyField('Firma', through='FirmaZauber', blank=True)

    def __str__(self):
        return "{} (Zauber)".format(self.name)

    @staticmethod
    def get_table_headings():
        return [
            {"headerName": "Icon", "field": "icon", "type": "image"},
            {"headerName": "Name", "field": "name", "type": "text"},
            {"headerName": "Beschreibung", "field": "beschreibung", "type": "text--long"},
            {"headerName": "Ab Stufe", "field": "ab_stufe", "type": "number"},
            {"headerName": "Schaden", "field": "schaden", "type": "text"},
            {"headerName": "Astralschaden", "field": "astralschaden", "type": "text"},
            {"headerName": "Manaverbrauch", "field": "manaverbrauch", "type": "text"},
            {"headerName": "Flächenwirkung", "field": "flächenzauber", "type": "boolean"},
            {"headerName": "Kategorie", "field": "kategorie", "type": "text"},
            {"headerName": "Günstigster Preis", "field": "billigster", "type": "price"},
            {"headerName": "Weiteres", "field": "weiteres", "type": "text"},
            {"headerName": "Preis * Stufe?", "field": "stufenabhängig", "type": "boolean"}
        ]
    
    @classmethod
    def get_all_serialized(cls, url_prefix="shop:buy_zauber"):
        return super().get_all_serialized(url_prefix)


class VergessenerZauber(BaseShop):
    class Meta:
        verbose_name = "Vergessener Zauber"
        verbose_name_plural = "Vergessene Zauber"

        ordering = ['name']

    schaden = models.CharField(max_length=100, default='', null=True, blank=True)
    astralschaden = models.CharField(max_length=100, default='', null=True, blank=True)
    manaverbrauch = models.CharField(max_length=100, default='', null=True, blank=True)

    flächenzauber = models.BooleanField(default=False)

    firmen = models.ManyToManyField('Firma', through='FirmaVergessenerZauber', blank=True)

    def __str__(self):
        return "{} (vergessener Zauber)".format(self.name)

    @staticmethod
    def get_table_headings():
        return [
            {"headerName": "Icon", "field": "icon", "type": "image"},
            {"headerName": "Name", "field": "name", "type": "text"},
            {"headerName": "Beschreibung", "field": "beschreibung", "type": "text--long"},
            {"headerName": "Ab Stufe", "field": "ab_stufe", "type": "number"},
            {"headerName": "Schaden", "field": "schaden", "type": "text"},
            {"headerName": "Astralschaden", "field": "astralschaden", "type": "text"},
            {"headerName": "Manaverbrauch", "field": "manaverbrauch", "type": "text"},
            {"headerName": "Flächenwirkung", "field": "flächenzauber", "type": "boolean"},
            {"headerName": "Günstigster Preis", "field": "billigster", "type": "price"},
            {"headerName": "Weiteres", "field": "weiteres", "type": "text"},
            {"headerName": "Preis * Stufe?", "field": "stufenabhängig", "type": "boolean"}
        ]
    
    @classmethod
    def get_all_serialized(cls, url_prefix="shop:buy_vergessener_zauber"):
        return super().get_all_serialized(url_prefix)


class Alchemie(BaseShop):
    class Meta:
        verbose_name = "Alchemie"
        verbose_name_plural = "Alchemie"

        ordering = ['name']

    kategorie = models.CharField(choices=enums.alchemie_enum, max_length=2, default=enums.alchemie_enum[0][0])
    firmen = models.ManyToManyField('Firma', through='FirmaAlchemie', blank=True)

    def __str__(self):
        return "{} (Alchemie)".format(self.name)
    
    @classmethod
    def get_all_serialized(cls, url_prefix="shop:buy_alchemie"):
        return super().get_all_serialized(url_prefix)


class Tinker(BaseShop):
    class Meta:
        verbose_name = "Für Selbstständige"
        verbose_name_plural = "Für Selbstständige"

        ordering = ['name']

    werte = models.TextField(max_length=1500, default='', blank=True)
    kategorie = models.CharField(choices=enums.tinker_enum, max_length=2, default=enums.tinker_enum[0][0])
    firmen = models.ManyToManyField('Firma', through='FirmaTinker', blank=True)

    def __str__(self):
        return "{} (für Selbstständige)".format(self.name)

    def toDict(self):
        return {"id": self.id, "name": self.name, "icon_url": self.getIconUrl()}

    @staticmethod
    def get_table_headings():
        return [
            {"headerName": "Icon", "field": "icon", "type": "image"},
            {"headerName": "Name", "field": "name", "type": "text"},
            {"headerName": "Beschreibung", "field": "beschreibung", "type": "text--long"},
            {"headerName": "Ab Stufe", "field": "ab_stufe", "type": "number"},
            {"headerName": "Werte", "field": "werte", "type": "text"},
            {"headerName": "Weiteres", "field": "weiteres", "type": "text"},
            {"headerName": "Preis * Stufe?", "field": "stufenabhängig", "type": "boolean"}
        ]
