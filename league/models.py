from django.db import models
from django.contrib.auth.models import User


class Responsabile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='responsabile')
    nome = models.CharField(max_length=100)
    cognome = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, primary_key=True, unique=True)
    password = models.CharField(max_length=100)
    otp_configured = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.nome} {self.cognome}"


class Arbitro(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='arbitro')
    nome = models.CharField(max_length=100)
    cognome = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, primary_key=True, unique=True)
    password = models.CharField(max_length=100)
    otp_configured = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.nome} {self.cognome}"


class Dirigente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='dirigente')
    nome = models.CharField(max_length=100)
    cognome = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, primary_key=True, unique=True)
    password = models.CharField(max_length=100)
    otp_configured = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.nome} {self.cognome}"

class Nazionalita(models.Model):
    nome = models.CharField(max_length=100, primary_key=True)
    def __str__(self):
        return self.nome


class Campionato(models.Model):
    nome = models.CharField(max_length=100, primary_key=True)
    nazionalita = models.ForeignKey(Nazionalita, on_delete=models.CASCADE,
                                    related_name='campionati')
    def __str__(self):
        return self.nome

class Squadra(models.Model):
    nome = models.CharField(max_length=100, primary_key=True)
    campionato = models.ForeignKey(Campionato, on_delete=models.CASCADE,
                                   related_name='squadre')
    data_fondazione = models.DateField(null=True, blank=True)
    stadio = models.CharField(max_length=100, null=True)
    capacita_stadio = models.IntegerField(null=True)
    citta = models.CharField(max_length=100, null=True)
    def __str__(self):
        return self.nome


class Giornata(models.Model):
    id = models.CharField(primary_key=True, max_length=100)
    numero = models.IntegerField()
    campionato = models.ForeignKey(Campionato, on_delete=models.CASCADE, related_name='giornate')

    class Meta:
        unique_together = ('numero', 'campionato')

    def __str__(self):
        return f"Giornata {self.numero} - {self.campionato.nome}"




class Partita(models.Model):
    id = models.AutoField(primary_key=True)
    squadra_casa = models.ForeignKey(Squadra, on_delete=models.CASCADE, related_name='partite_casa')
    squadra_ospite = models.ForeignKey(Squadra, on_delete=models.CASCADE, related_name='partite_ospite')
    campionato = models.ForeignKey(Campionato, on_delete=models.CASCADE, related_name='partite')
    giornata = models.ForeignKey(Giornata, on_delete=models.CASCADE, related_name='partite', null=True, blank=True)
    risultato = models.CharField(max_length=10, null=True, blank=True)
    data = models.DateTimeField()
    stadio = models.CharField(max_length=100)
    gol_casa = models.IntegerField(null=True, blank=True)
    gol_ospite = models.IntegerField(null=True, blank=True)

class Classifica(models.Model):
    campionato = models.ForeignKey(Campionato, on_delete=models.CASCADE, related_name='classifiche')
    squadra = models.ForeignKey(Squadra, on_delete=models.CASCADE, related_name='classifiche')
    posizione = models.IntegerField()
    punti = models.IntegerField(default=0)
    gol_fatti = models.IntegerField(default=0)
    gol_subiti = models.IntegerField(default=0)
    differenza_reti = models.IntegerField(default=0)
    partite_giocate = models.IntegerField(default=0)
    partite_vinte = models.IntegerField(default=0)
    partite_pareggiate = models.IntegerField(default=0)
    partite_perse = models.IntegerField(default=0)

    class Meta:
        unique_together = ('campionato', 'squadra')
        ordering = ['posizione']



class Referto(models.Model):
    arbitro = models.ForeignKey(Arbitro, on_delete=models.CASCADE, related_name='referti')
    partita = models.ForeignKey('Partita', on_delete=models.CASCADE, related_name='referti')
    data_referto = models.DateField(auto_now_add=True)
    note = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Referto {self.id} - Partita: {self.partita.id} - Arbitro: {self.arbitro.nome} {self.arbitro.cognome}"