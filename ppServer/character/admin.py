import itertools

from django.contrib import admin
from django.http.request import HttpRequest
from django.utils.html import format_html

from .models import *


class SpielerReadonlyInLine(admin.TabularInline):
    def has_delete_permission(self, request: HttpRequest, obj) -> bool:
        if request.user.groups.filter(name__iexact="spieler"): return False
        return super().has_delete_permission(request, obj)

    def has_change_permission(self, request: HttpRequest, obj) -> bool:
        if request.user.groups.filter(name__iexact="spieler"): return False
        return super().has_change_permission(request, obj)
    
    def has_add_permission(self, request: HttpRequest, obj) -> bool:
        if request.user.groups.filter(name__iexact="spieler"): return False
        return super().has_add_permission(request, obj)


class WesenkraftZusatzWesenspInLine(admin.TabularInline):
    model = Wesenkraft.skilled_gfs.through
    extra = 1


class GfsImageInLine(admin.TabularInline):
    model = GfsImage
    fields = ["order", "img", "text"]
    extra = 1

class GfsAttributInLine(admin.TabularInline):
    model = GfsAttribut
    fields = ["attribut", "aktuellerWert", "maxWert"]
    readonly_fields = ["attribut"]
    extra = 0

    def has_add_permission(self, request, obj=None):
        return False


class GfsFertigkeitInLine(admin.TabularInline):
    model = GfsFertigkeit
    fields = ["fertigkeit", "fp"]
    readonly_fields = ["fertigkeit"]
    extra = 0

    def has_add_permission(self, request, obj=None):
        return False


class GfsVorteilInLine(admin.TabularInline):
    model = GfsVorteil
    extra = 1


class GfsNachteilInLine(admin.TabularInline):
    model = GfsNachteil
    extra = 1


class GfsWesenkraftInLine(admin.TabularInline):
    model = GfsWesenkraft
    extra = 1


class GfsZauberInLine(admin.TabularInline):
    model = GfsZauber
    extra = 1


class GfsStufenplanInLine(admin.TabularInline):
    model = GfsStufenplan
    fields = ["basis", "vorteile", "zauber", "wesenkräfte", "ability"]
    extra = 0


class SpezialAusgleichInLine(admin.TabularInline):
    model = Spezialfertigkeit.ausgleich.through
    extra = 1


class WissenFertInLine(admin.TabularInline):
    model = Wissensfertigkeit.fertigkeit.through
    extra = 1


class RelSpeziesInline(admin.TabularInline):
    model = RelSpezies
    extra = 1


class RelPersönlichkeitInline(SpielerReadonlyInLine):
    model = RelPersönlichkeit
    extra = 1


class RelAttributInline(SpielerReadonlyInLine):
    fields = ['attribut', 'aktuellerWert', 'aktuellerWert_temp', 'aktuellerWert_bonus', 'maxWert', 'maxWert_temp', 'fg', "fg_temp"]
    readonly_fields = ['attribut']
    model = RelAttribut
    extra = 0

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class RelFertigkeitInLine(SpielerReadonlyInLine):
    fields = ['fertigkeit', 'fp', "fp_temp", 'fp_bonus']
    readonly_fields = ['fertigkeit']
    model = RelFertigkeit
    extra = 0

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class RelWesenkraftInLine(SpielerReadonlyInLine):
    model = RelWesenkraft
    extra = 1


class RelSpezialfertigkeitInLine(SpielerReadonlyInLine):
    model = RelSpezialfertigkeit
    extra = 1


class RelWissensfertigkeitInLine(SpielerReadonlyInLine):
    model = RelWissensfertigkeit
    extra = 1


class AffektivitätInLine(admin.TabularInline):
    model = Affektivität
    extra = 1
    exclude = ['grad', 'umgang']


class GfsAbilityInLine(admin.TabularInline):
    model = RelGfsAbility
    fields = ["ability", "notizen"]
    extra = 1


class RelVorteilInLine(SpielerReadonlyInLine):
    model = RelVorteil
    fields = ["teil", "attribut", "fertigkeit", "engelsroboter", "notizen", "ip", "is_sellable", "will_create"]
    readonly_fields = ["is_sellable", "will_create"]
    exclude = ["anzahl"]
    extra = 1


class RelNachteilInLine(SpielerReadonlyInLine):
    model = RelNachteil
    fields = ["teil", "attribut", "fertigkeit", "notizen", "ip", "is_sellable", "will_create"]
    readonly_fields = ["is_sellable", "will_create"]
    extra = 1

class RelTalentInLine(SpielerReadonlyInLine):
    model = RelTalent
    fields = ["talent"]
    extra = 1

########## generic (st)shop ##############

class RelShopInLine(SpielerReadonlyInLine):
    extra = 1
    fields = ["anz", "item", "notizen"]


################## Shop ############################

class RelItemlInLine(RelShopInLine):
    model = RelItem


class RelWaffen_WerkzeugelInLine(RelShopInLine):
    model = RelWaffen_Werkzeuge


class RelMagazinInLine(RelShopInLine):
    model = RelMagazin


class RelPfeil_BolzenInLine(RelShopInLine):
    model = RelPfeil_Bolzen


class RelSchusswaffenInLine(RelShopInLine):
    model = RelSchusswaffen


class RelMagische_AusrüstungInLine(RelShopInLine):
    model = RelMagische_Ausrüstung


class RelRituale_RunenInLine(RelShopInLine):
    model = RelRituale_Runen
    fields = ["anz", "stufe", "item", "notizen"]


class RelRüstungInLine(RelShopInLine):
    model = RelRüstung


class RelAusrüstung_TechnikInLine(RelShopInLine):
    model = RelAusrüstung_Technik
    fields = ["anz", "item", "notizen", "selbst_eingebaut"]


class RelFahrzeugInLine(RelShopInLine):
    model = RelFahrzeug


class RelEinbautenInLine(RelShopInLine):
    model = RelEinbauten


class RelZauberInLine(RelShopInLine):
    fields = fields = ["anz", "item", "tier", "notizen"]
    model = RelZauber


class RelVergessenerZauberInLine(RelShopInLine):
    model = RelVergessenerZauber


class RelAlchemieInLine(RelShopInLine):
    model = RelAlchemie


class RelTinkerInLine(RelShopInLine):
    model = RelTinker


class RelBegleiterInLine(RelShopInLine):
    model = RelBegleiter


class RelEngelsroboterInLine(RelShopInLine):
    model = RelEngelsroboter



class CharakterAdmin(admin.ModelAdmin):

    class Meta:
        model = Charakter

    fieldsets = [
        ("Settings (Finger weg)", {'fields': ['eigentümer', "in_erstellung", "ep_system", "larp", "gfs"]}),
        ('Roleplay', {'fields': ['image', 'name', "gewicht", "größe", 'alter', 'geschlecht', 'sexualität', 'beruf', "präf_arm",
                              'religion', "hautfarbe", "haarfarbe", "augenfarbe"]}),
        
        ("Manifest", {"fields": ["manifest", "sonstiger_manifestverlust", "notizen_sonstiger_manifestverlust"]}),
        ('HP', {'fields': ['rang', 'HPplus', 'HPplus_fix', 'HPplus_geistig']}),
        ('Kampf', {'fields': ['wesenschaden_waff_kampf', 'wesenschaden_andere_gestalt', 'crit_attack', 'crit_defense',
                              'initiative_bonus', 'reaktion_bonus', 'natürlicher_schadenswiderstand_bonus', 'astralwiderstand_bonus']}),

        ('Kampagne', {'fields': ["ep", 'ep_stufe', 'ep_stufe_in_progress', "skilltree_stufe", "processing_notes"]}),
        ('Währungen', {'fields': ['ap', 'fp', 'fg', 'sp', 'ip', 'tp', 'spF_wF', 'wp', 'zauberplätze', "geld", 'konzentration', "prestige", "verzehr"]}),
        ('Geschreibsel', {'fields': ['notizen', 'persönlicheZiele', 'sonstige_items']}),
    ]

    inlines = [
               RelPersönlichkeitInline,
               RelSpeziesInline, RelWesenkraftInLine,
               RelAttributInline,
               RelFertigkeitInLine,
               RelSpezialfertigkeitInLine,
               RelWissensfertigkeitInLine, RelVorteilInLine,
               RelNachteilInLine, RelTalentInLine,
               AffektivitätInLine,
               GfsAbilityInLine,

               RelItemlInLine,
               RelWaffen_WerkzeugelInLine,
               RelMagazinInLine,
               RelPfeil_BolzenInLine,
               RelSchusswaffenInLine,
               RelMagische_AusrüstungInLine,
               RelRituale_RunenInLine,
               RelRüstungInLine,
               RelAusrüstung_TechnikInLine,
               RelFahrzeugInLine,
               RelEinbautenInLine,
               RelZauberInLine,
               RelVergessenerZauberInLine,
               RelAlchemieInLine,
               RelTinkerInLine,
               RelBegleiterInLine,
               RelEngelsroboterInLine
    ]

    list_display = ['image_', 'name', 'eigentümer', "gfs", "wesen_", "ep_system", "larp", "in_erstellung"]

    list_filter = ['in_erstellung', 'larp', 'ep_system', 'eigentümer']
    search_fields = ['name', 'eigentümer__name']
    list_display_links = ["name"]

    save_on_top = True

    def image_(self, obj):
        return format_html(f"<img src='{obj.image.url}' style='max-width: 32px; max-height:32px;'>") if obj.image else "-"

    def wesen_(self, obj):
        return ', '.join([w.titel for w in obj.spezies.all()])

    def get_readonly_fields(self, request, obj=None):
        if request.user.groups.filter(name__iexact="spieler"):
            all_fields = set(itertools.chain.from_iterable([fs[1]["fields"] for fs in self.fieldsets]))
            allowed_fields = set([
                "name", "gewicht", "größe", "alter", "geschlecht", "sexualität", "beruf",
                "präf_arm", "religion", "hautfarbe", "haarfarbe", "augenfarbe",
                'persönlicheZiele', 'notizen', 'sonstige_items'
            ])
            return all_fields - allowed_fields

        return super().get_readonly_fields(request, obj)

    def get_queryset(self, request):
        if request.user.groups.filter(name__iexact="spieler"):
            return Charakter.objects.filter(eigentümer__name__exact=request.user.username)
        else:
            return super().get_queryset(request)


class AttributAdmin(admin.ModelAdmin):
    list_display = ('titel', 'beschreibung')
    search_fields = ['titel', 'beschreibung']


class FertigkeitAdmin(admin.ModelAdmin):

    fieldsets = [
        (None, {'fields': ['titel', 'limit', 'attr1', 'attr2']}),
        ('Beschreibung', {'fields': ['beschreibung']})
    ]

    list_display = ('titel', 'attr1', 'attr2', 'limit', 'beschreibung')
    search_fields = ['titel', 'attr1__titel', 'attr2__titel', 'limit']
    list_filter = ['attr1', 'attr2', 'limit']


class WesenkraftAdmin(admin.ModelAdmin):

    fields = ['titel', 'probe', 'wirkung', 'manaverbrauch', "skilled_gfs"]
    inlines = [WesenkraftZusatzWesenspInLine]

    list_display = ['titel', 'probe', 'manaverbrauch', 'wirkung', 'skilled_gfs_']
    search_fields = ['titel', 'skilled_gfs']
    list_filter = ['skilled_gfs']

    def skilled_gfs_(self, obj):
        return ", ".join([gfs.titel for gfs in obj.skilled_gfs.all()])


class SpezialfertigkeitAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['titel', 'attr1', 'attr2']}),
        ('Beschreibung', {'fields': ['beschreibung']})
    ]

    inlines = [SpezialAusgleichInLine]

    list_display = ('titel', 'attr1', 'attr2', 'ausgleich_', 'beschreibung')
    list_filter = ['attr1', 'attr2', 'ausgleich']
    search_fields = ['titel', 'attr1__titel', 'attr2__titel']

    def ausgleich_(self, obj):
        return ', '.join([a.titel for a in obj.ausgleich.all()])


class WissensfertigkeitAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['titel', 'attr1', 'attr2', 'attr3']}),
        ('Beschreibung', {'fields': ['beschreibung']})
    ]

    inlines = [WissenFertInLine]

    list_display = ('titel', 'attr1', 'attr2', 'attr3', 'fertigkeit_', 'beschreibung')
    list_filter = ['attr1', 'attr2', 'attr3', 'fertigkeit']
    search_fields = ['titel', 'attr1__titel', 'attr2__titel', 'attr3__titel']

    def fertigkeit_(self, obj):
        return ', '.join([a.titel for a in obj.fertigkeit.all()])


class SpeziesAdmin(admin.ModelAdmin):
    list_display = ('komplexität', 'titel',)
    search_fields = ('komplexität', 'titel',)

class GfsAdmin(admin.ModelAdmin):
    list_display = ('icon_', 'titel', 'ap', 'difficulty', 'vorteil_', 'nachteil_', 'zauber_',
                    "wesenschaden_waff_kampf", "wesenschaden_andere_gestalt", "wesenkraft_", "startmanifest",)
    list_filter = ['ap', 'startmanifest', "wesenschaden_waff_kampf"]
    search_fields = ('titel', 'ap')

    list_editable = ['wesenschaden_waff_kampf', 'wesenschaden_andere_gestalt', 'difficulty']
    list_display_links = ["icon_", "titel"]

    inlines = [GfsImageInLine, GfsAttributInLine, GfsFertigkeitInLine,
               GfsVorteilInLine, GfsNachteilInLine,
               GfsWesenkraftInLine, GfsZauberInLine,
               GfsStufenplanInLine]
    
    def icon_(self, obj):
        return format_html(f'<img src="{obj.icon.url}" style="max-width: 32px; max-height:32px;" />' if obj.icon else "-")

    def vorteil_(self, obj):
        return ', '.join([a.titel for a in obj.vorteile.all()])

    def nachteil_(self, obj):
        return ', '.join([a.titel for a in obj.nachteile.all()])

    def zauber_(self, obj):
        return ', '.join([a.item.name for a in GfsZauber.objects.prefetch_related("item").filter(gfs=obj)])

    def wesenkraft_(self, obj):
        return ', '.join([a.titel for a in obj.wesenkraft.all()])


class GfsAbilityAdmin(admin.ModelAdmin):
    list_display = ("name", "beschreibung", "needs_implementation", "has_choice")
    list_editable = ["needs_implementation", "has_choice"]


class PersönlichkeitAdmin(admin.ModelAdmin):
    list_display = ('titel', 'positiv', 'negativ')
    search_fields = ('titel', 'positiv', 'negativ')


class VorNachteilAdmin(admin.ModelAdmin):

    list_display = ('titel', 'ip', 'beschreibung', "wann_wählbar", "is_sellable", "_max_amount", "needs_ip", "needs_attribut", "needs_fertigkeit", "needs_engelsroboter", "needs_notiz")
    list_editable = ("is_sellable", "needs_ip", "needs_attribut", "needs_fertigkeit", "needs_engelsroboter", "needs_notiz")
    list_filter = ['ip', "wann_wählbar"]
    search_fields = ['titel', 'ip', "wann_wählbar"]

    def _max_amount(self, obj):
        return obj.max_amount or "unbegrenzt"


class BerufAdmin(admin.ModelAdmin):
    list_display = ['titel', 'beschreibung']
    search_fields = ['titel']
    list_filter = ['titel']


class ReligionAdmin(admin.ModelAdmin):
    list_display = ['titel', 'beschreibung']
    search_fields = ['titel']
    list_filter = ['titel']


class SpielerAdmin(admin.ModelAdmin):
    #readonly_fields = ["name"]
    fields = ["name", "geburtstag"]
    list_display = ["name", "geburtstag"]


class SkilltreeEntryWesenAdmin(admin.ModelAdmin):
    list_display = ["wesen", "context"]
    list_filter = ["wesen", "context"]


class GfsStufenplanBaseAdmin(admin.ModelAdmin):
    list_display = ["stufe", "ep", "ap", "fp", "fg", "tp"]
    list_editable = ["ep", "ap", "fp", "fg", "tp"]


class TalentAdmin(admin.ModelAdmin):
    list_display = ["titel", "tp", "beschreibung", "kategorie", "bedingung_"]

    def bedingung_(self, obj):
        return ", ".join([t.titel for t in obj.bedingung.all()])


class GfsSkilltreeEntryAdmin(admin.ModelAdmin):
    class IsCorrectlyFormattedFilter(admin.SimpleListFilter):
        title = 'correctly_formatted'
        parameter_name = 'correctly_formatted'

        def lookups(self, request, model_admin):
            return (
                ("y", "Korrekt"),
                ("n", "Falsch"),
            )

        def queryset(self, request, queryset):
            if self.value() is None: return queryset
            value = self.value() == "y"

            ids = []
            for e in queryset:
                is_correct = "error" not in e.__repr__().lower()
                if (value and is_correct) or (not value and not is_correct): ids.append(e.id)

            return queryset.filter(id__in=ids)

    list_display = ["context_", "entry", "operation", "correctly_formatted"]

    search_fields = ["gfs__titel", "base__stufe", "text", "vorteil__titel", "nachteil__titel", "spezialfertigkeit__titel", "wissensfertigkeit__titel", "amount", "stufe", "wesenkraft__titel"]
    list_filter = ["gfs", "base__stufe", "operation", IsCorrectlyFormattedFilter]

    def context_(self, obj):
        return f"{obj.gfs.titel} St. {obj.base.stufe}"

    def entry(self, obj):
        return obj.__repr__()
    
    def correctly_formatted(self, obj):
        return "error" not in obj.__repr__().lower()
    correctly_formatted.boolean = True


admin.site.register(Charakter, CharakterAdmin)
admin.site.register(Spezies, SpeziesAdmin)
admin.site.register(Gfs, GfsAdmin)
admin.site.register(Persönlichkeit, PersönlichkeitAdmin)
admin.site.register(Attribut, AttributAdmin)
admin.site.register(Fertigkeit, FertigkeitAdmin)
admin.site.register(Wesenkraft, WesenkraftAdmin)
admin.site.register(Spezialfertigkeit, SpezialfertigkeitAdmin)
admin.site.register(Religion, ReligionAdmin)
admin.site.register(Beruf, BerufAdmin)
admin.site.register(Nachteil, VorNachteilAdmin)
admin.site.register(Vorteil, VorNachteilAdmin)
admin.site.register(Wissensfertigkeit, WissensfertigkeitAdmin)

admin.site.register(SkilltreeBase, admin.ModelAdmin)
admin.site.register(Talent, TalentAdmin)

admin.site.register(GfsAbility, GfsAbilityAdmin)
admin.site.register(GfsStufenplanBase, GfsStufenplanBaseAdmin)

admin.site.register(Spieler, SpielerAdmin)

admin.site.register(GfsSkilltreeEntry, GfsSkilltreeEntryAdmin)
