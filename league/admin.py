from django.contrib import admin
from .models import Squadra, Partita, Classifica, Giornata, Responsabile, Arbitro, Dirigente

class ResponsabileAdmin(admin.ModelAdmin):
    list_display = ('nome', 'cognome', 'user')

class ArbitroAdmin(admin.ModelAdmin):
    list_display = ('nome', 'cognome', 'user')

class DirigenteAdmin(admin.ModelAdmin):
    list_display = ('nome', 'cognome', 'user')

admin.site.register(Squadra)
admin.site.register(Partita)
admin.site.register(Classifica)
admin.site.register(Giornata)
admin.site.register(Responsabile, ResponsabileAdmin)
admin.site.register(Arbitro, ArbitroAdmin)
admin.site.register(Dirigente, DirigenteAdmin)