from django.contrib import admin
from .models import Lager, Artikel

# Lager-Modell für das Admin-Interface registrieren
admin.site.register(Lager)
admin.site.register(Artikel)