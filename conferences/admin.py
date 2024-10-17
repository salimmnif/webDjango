from django.contrib import admin
from .models import Conference
from participants.models import Reservation
from django.utils import timezone

class ConferenceDateFilter(admin.SimpleListFilter):
    title = 'Conference Date'
    parameter_name = 'conference_date'

    def lookups(self, request, model_admin):
        # Les options proposées dans le filtre
        return (
            ('past', 'Past Conferences'),
            ('upcoming', 'Upcoming Conferences'),
            ('today', 'Today Conferences'),
        )

    def queryset(self, request, queryset):
        # Obtenir la date actuelle
        today = timezone.now().date()

        if self.value() == 'past':
            # Conférences dont la date de fin est avant aujourd'hui
            return queryset.filter(end_date__lt=today)
        elif self.value() == 'upcoming':
            # Conférences dont la date de début est après aujourd'hui
            return queryset.filter(start_date__gt=today)
        elif self.value() == 'today':
            # Conférences dont la date actuelle est entre la date de début et de fin
            return queryset.filter(start_date__lte=today, end_date__gte=today)

        return queryset

class TitleFilter(admin.SimpleListFilter):
    title = 'Title'
    parameter_name = 'title'

    def lookups(self, request, model_admin):
        # Récupère tous les titres des conférences disponibles
        titles = set(Conference.objects.values_list('title', flat=True))
        return [(title, title) for title in titles]

    def queryset(self, request, queryset):
        # Filtrer selon le titre sélectionné dans le filtre
        if self.value():
            return queryset.filter(title=self.value())
        return queryset

# Filtre personnalisé pour le nombre de participants
class ParticipantsFilter(admin.SimpleListFilter):
    title = 'Participants'  # Titre du filtre affiché dans l'admin
    parameter_name = 'participants'  # Nom du paramètre dans l'URL

    def lookups(self, request, model_admin):
        return (
            ('no_participants', 'No participants'),  # Conférences sans participants
            ('has_participants', 'Has participants'),  # Conférences avec participants
        )

    def queryset(self, request, queryset):
        # Filtrer les conférences selon le nombre de participants
        if self.value() == 'no_participants':
            return queryset.filter(participants__isnull=True)  # Sans participants
        elif self.value() == 'has_participants':
            return queryset.filter(particpants__isnull=False)  # Avec participants
        return queryset

# Inline pour afficher et gérer les réservations directement dans la page d'édition de la conférence
class ReservationInline(admin.TabularInline):
    model = Reservation  # Modèle Reservation
    extra = 1  # Nombre de lignes supplémentaires affichées dans l'inline
    readonly_fields = ("reservation_date",)  # Champs en lecture seule

# Configuration de l'admin pour le modèle Conference
class ConferenceAdmin(admin.ModelAdmin):
    list_display = ("title", "location", "start_date", "end_date", "price")  # Colonnes affichées dans la liste
    search_fields = ("title",)  # Champs de recherche
    list_per_page = 10  # Pagination
    ordering = ("start_date",)  # Ordre de tri
    readonly_fields = ("created_at", "updated_at")  # Champs en lecture seule
    inlines = [ReservationInline]  # Inline pour gérer les réservations
    list_filter = (ParticipantsFilter, TitleFilter,ConferenceDateFilter)  # Assurez-vous que le filtre est ici

    fieldsets = (
        ('Description', {
            'fields': ('title', 'description', 'category')
        }),
        ('Horaires de la conférence', {
            'fields': ('start_date', 'end_date')
        }),
        ('Localisation et détails', {
            'fields': ('location', 'price', 'capacity')
        }),
        ('Programme', {
            'fields': ('program',)
        }),
        ('Données de suivi', {  # Section pour les champs en lecture seule
            'fields': ('created_at', 'updated_at')
        }),
    )

# Enregistrement du modèle Conference avec la configuration personnalisée
admin.site.register(Conference, ConferenceAdmin)
