from typing import Any
from django.contrib import admin
from django.db.models.query import QuerySet
from django.http.request import HttpRequest
from django.utils.html import format_html

from .models import *


class MonsterFormsInLineAdmin(admin.TabularInline):
    verbose_name = "andere Form"
    verbose_name_plural = "andere Formen"

    model = Monster.forms.through    
    fk_name = "from_monster"
    extra = 1
class GegenmonsterInLineAdmin(admin.TabularInline):
    verbose_name = "Gegenmonster"
    verbose_name_plural = "Gegenmonster"

    model = Monster.opposite.through    
    fk_name = "from_monster"
    extra = 1
class EvoliutionPreInLineAdmin(admin.TabularInline):
    verbose_name = "Vorentwicklung"
    verbose_name_plural = "Vorentwicklungen"

    model = Monster.evolutionPre.through    
    fk_name = "from_monster"
    extra = 1
class EvolutionPostInLineAdmin(admin.TabularInline):
    verbose_name = "Weiterentwicklung"
    verbose_name_plural = "Weiterentwicklungen"

    model = Monster.evolutionPost.through    
    fk_name = "from_monster"
    extra = 1

class AttackeInLineAdmin(admin.TabularInline):
    verbose_name = "Attacke"
    verbose_name_plural = "Attacken"

    model = Monster.attacken.through
    extra = 1

class MonsterAdmin(admin.ModelAdmin):
    change_list_template = "dex/admin/change_list_monster.html"


    fieldsets = [
        ("Basics", {'fields': ['number', "name", "types", "fähigkeiten", "visible"]}),
        ("Aussehen", {'fields': ['image', 'height', "weight", "description", "habitat"]}),
        ('Start-Werte', {'fields': ['wildrang', "base_schadensWI", "base_attackbonus", "base_reaktionsbonus", "base_initiative", "base_hp", "base_nahkampf", "base_fernkampf", "base_magie", "base_verteidigung_geistig", "base_verteidigung_körperlich"]}),
    ]

    inlines = [MonsterFormsInLineAdmin, GegenmonsterInLineAdmin, EvoliutionPreInLineAdmin, EvolutionPostInLineAdmin, AttackeInLineAdmin]

    list_display = ['image_', 'name_', 'types_', 'wildrang', "schadensWI_", "base_attackbonus", "rang_attackbonus", "base_reaktionsbonus", "rang_reaktionsbonus"]

    search_fields = ['number', 'name', 'description']
    list_display_links = ["name_"]
    list_editable = ['wildrang', "base_attackbonus", "base_reaktionsbonus"]

    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        return self.model.objects.with_rang()

    def image_(self, obj):
        return format_html(f"<img src='{obj.image.url}' style='max-width: 32px; max-height:32px;'>") if obj.image else "-"
    def name_(self, obj):
        return f"#{obj.number} {obj.name}"
    def types_(self, obj):
        return format_html("".join([t.tag() for t in obj.types.all()])) or "-"
    def schadensWI_(self, obj):
        base = obj.base_schadensWI_str
        rang = obj.rang_schadensWI_str
        return format_html(f"{base or ''}<span style='color: red'>{' + ' if base and rang else ''}{rang or ''}</span>")

    def rang_attackbonus(self, obj):
        return format_html(f"<span style='color: red'>+{obj.rang_angriffsbonus}</span> = <b>{obj.base_attackbonus + obj.rang_angriffsbonus}</b>")
    def rang_reaktionsbonus(self, obj):
        return format_html(f"<span style='color: red'>+{obj.rang_reaktionsbonus}</span> = <b>{obj.base_reaktionsbonus + obj.rang_reaktionsbonus}</b>")


class MonsterFähigkeitAdmin(admin.ModelAdmin):
    list_display = ["name", "description"]
    search_fields = ["name", "description"]


class MonsterRangAdmin(admin.ModelAdmin):
    list_display = ["rang", "schadensWI_", "attackenpunkte", "reaktionsbonus", "angriffsbonus"]
    list_editable = ["attackenpunkte", "reaktionsbonus", "angriffsbonus"]

    def schadensWI_(self, obj):
        return " + ".join([t.__str__() for t in obj.schadensWI.all()]) or "-"


class MonsterTeamAdmin(admin.ModelAdmin):
    list_display = ["name_", "monster_"]
    list_display_links = ["name_"]

    def name_(self, obj):
        return format_html(f"<div style='color: {obj.textfarbe}; background-color: {obj.farbe}; padding: .1em .3em'>{obj.name}</div>")
    def monster_(self, obj):
        return ", ".join([t.__str__() for t in obj.monster.all()]) or "-"

class TypAdmin(admin.ModelAdmin):

    list_display = ['Aussehen_', "stark_gegen_", "schwach_gegen_", "trifft_nicht_"]

    list_filter = ['name', "stark_gegen", "schwach_gegen", "trifft_nicht"]
    search_fields = ['name']

    def stark_gegen_(self, obj):
        return format_html("".join([t.tag() for t in obj.stark_gegen.all()])) or "-"
    def schwach_gegen_(self, obj):
        return format_html("".join([t.tag() for t in obj.schwach_gegen.all()])) or "-"
    def trifft_nicht_(self, obj):
        return format_html("".join([t.tag() for t in obj.trifft_nicht.all()])) or "-"
    def Aussehen_(self, obj):
        return obj.tag()


class AttackeAdmin(admin.ModelAdmin):

    list_display = [
        'name', 'types_', 'description', 'damage_', 'macht_schaden', 'macht_effekt', 'cost', 'kosten_vorschlag',
    ]

    list_filter = ["draft", "types", "macht_schaden", "macht_effekt", 'angriff_nahkampf', 'angriff_fernkampf', 'angriff_magie', 'verteidigung_geistig', 'verteidigung_körperlich']
    search_fields = ['name', "description"]
    list_display_links = ["name"]

    def damage_(self, obj):
        return " + ".join([t.__str__() for t in obj.damage.all()]) or "-"
    def types_(self, obj):
        return format_html(", ".join([t.tag() for t in obj.types.all()])) or "-"
    def kosten_vorschlag(self, obj):
        from dex.management.commands.calc_attack_cost import cost_estimate as estimate
        return format_html(f"<i>{estimate(obj)}</i>")

class StatInlineAdmin(admin.TabularInline):
    model = RangStat

    fields = ["stat", "wert", "skilled", "trained"]
    readonly_fields = ["stat"]
    extra = 0

    def has_add_permission(self, *args, **kwargs) -> bool:
        return False
    def has_delete_permission(self, *args, **kwargs) -> bool:
        return False

class SpielerMonsterAttackInlineAdmin(admin.TabularInline):
    model = SpielerMonsterAttack

    fields = ["attacke", "cost"]
    extra = 1

    def has_add_permission(self, *args, **kwargs) -> bool:
        return False
    def has_delete_permission(self, *args, **kwargs) -> bool:
        return False

class SpielerMonsterAdmin(admin.ModelAdmin):

    list_display = ['spieler', 'name', 'monster', 'rang', "attackenpunkte"]

    list_filter = ["spieler", "monster"]
    search_fields = ['spieler__name", "monster__name']

    fields = ['spieler', "monster", "name", "rang", "attackenpunkte"]
    inlines = [StatInlineAdmin, SpielerMonsterAttackInlineAdmin]


admin.site.register(Typ, TypAdmin)
admin.site.register(Monster, MonsterAdmin)
admin.site.register(SpielerMonster, SpielerMonsterAdmin)
admin.site.register(MonsterTeam, MonsterTeamAdmin)
admin.site.register(Attacke, AttackeAdmin)
admin.site.register(MonsterRang, MonsterRangAdmin)
admin.site.register(MonsterFähigkeit, MonsterFähigkeitAdmin)