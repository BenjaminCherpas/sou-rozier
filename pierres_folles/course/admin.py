# -*- coding: utf-8 -*-

from django.contrib import admin
from pierres_folles.course.models import (
    Partner, Runner, Competition, License, InstantPaymentNotification, Category, Course, Inscrit,
    InfoSource
)


def archive(modeladmin, request, queryset):
    queryset.update(is_archived=True)
archive.short_description = u'Archiver'


def unarchive(modeladmin, request, queryset):
    queryset.update(is_archived=False)
unarchive.short_description = u'Désarchiver'


class PartnerAdmin(admin.ModelAdmin):
    list_display = ('name', 'url', 'is_archived', 'ordering', 'best_partner')
    list_filter = ('best_partner', 'is_archived', )
    actions = [archive, unarchive]

admin.site.register(Partner, PartnerAdmin)


class DepartementFilter(admin.SimpleListFilter):
    """filter"""
    title = u'Departement?'
    parameter_name = 'departement'

    def lookups(self, request, model_admin):
        all_deps = set([runner.zip_code[:2] for runner in Runner.objects.all()])
        return [
            (dep, dep) for dep in sorted(all_deps)
        ]

    def queryset(self, request, queryset):
        value = self.value()
        if value:
            return queryset.filter(zip_code__startswith=value)
        return queryset


class CompetitionYearFilter(admin.SimpleListFilter):
    """filter"""
    title = u'Année'
    parameter_name = 'year'

    def lookups(self, request, model_admin):
        years = set([competition.before_date.year for competition in Competition.objects.all()])
        return [
            (year, str(year)) for year in sorted(years)
        ]

    def queryset(self, request, queryset):
        value = self.value()
        if value:
            return queryset.filter(competition__before_date__year=value)
        return queryset



class RunnerAdmin(admin.ModelAdmin):
    list_display = ('lastname', 'firstname', 'competition', 'source_info', 'zip_code', )
    list_filter = (CompetitionYearFilter, 'competition', DepartementFilter, 'source_info', )

admin.site.register(Runner, RunnerAdmin)


class CompetitionAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'price_before', 'before_date', 'is_archived')
    list_filter = ('is_archived', )
    actions = [archive, unarchive]

admin.site.register(Competition, CompetitionAdmin)


admin.site.register(License)
admin.site.register(InstantPaymentNotification)
#admin.site.register(Category)
#admin.site.register(Course)

#
# class ArriveFilter(admin.SimpleListFilter):
#     """filter items which are below their stock threshold"""
#     title = u'Arrivé?'
#     parameter_name = 'arrived'
#
#     def lookups(self, request, model_admin):
#         return [
#             ('1', u'Oui'),
#             ('2', u'Non'),
#         ]
#
#     def queryset(self, request, queryset):
#         value = self.value()
#         if value:
#             if value == '1':
#                 return queryset.filter(arrivee__isnull=False)
#             else:
#                 return queryset.filter(arrivee__isnull=True)
#         return queryset
#
#
# class InscritAdmin(admin.ModelAdmin):
#     list_display = ('numero', 'nom', 'prenom', 'gender', 'category', 'course', 'arrivee', 'temps')
#     list_editable = ('arrivee',)
#     readonly_fields = ('temps',)
#     search_fields = ('numero', 'nom')
#     list_filter = ('course', 'category', 'gender', ArriveFilter)
#
# admin.site.register(Inscrit, InscritAdmin)

admin.site.register(InfoSource)