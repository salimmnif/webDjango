from django.contrib import admin
from .models import (Participant,Reservation)
from categories.models import Category
admin.site.register(Category)



def make_confirmed(modeladmin, request, queryset):
    queryset.update(confirmed=True)  
    modeladmin.message_user(request, "Les réservations sélectionnées ont été marquées comme confirmées.")


def make_unconfirmed(modeladmin, request, queryset):
    queryset.update(confirmed=False)  
    modeladmin.message_user(request, "Les réservations sélectionnées ont été marquées comme non confirmées.")


class ReservationAdmin(admin.ModelAdmin):
    list_display = ('id', 'participant', 'conference', 'comfirmed', 'reservation_date')  
    list_filter = ('comfirmed', 'reservation_date')  
    search_fields = ('participant__username', 'conference__title')  
    actions = [make_confirmed, make_unconfirmed]



class ParticipantAdmin(admin.ModelAdmin):
    list_display = ("cin", "email", "first_name", "last_name")  # Colonnes affichées dans la liste
    search_fields = ("username",)  # Champs de recherche
    list_per_page = 10  # Pagination
    ordering = ("first_name", "last_name")  # Ordre de tri
    
    fieldsets = (
        ('Presentation', {
            'fields': ('username', 'first_name', 'last_name')
        }),
        ('Données', {
            'fields': ('email', 'cin')
        }),
        ('Catégorie de participant', {
            'fields': ('participants_category',)
        }),
        # Supprimez les réservations de fieldsets
    )

# Enregistrement de la classe dans l'admin
admin.site.register(Participant, ParticipantAdmin)

admin.site.register(Reservation,ReservationAdmin)
