from django.shortcuts import render, redirect
from .models import Campionato, Classifica, Partita, Giornata, Responsabile, Arbitro, Dirigente, Referto
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages
import hashlib


def benvenuto(request):
    return render(request, 'benvenuto.html')

def principale(request):
    # Get Serie A campionato
    try:
        serie_a = Campionato.objects.get(nome='Serie A')

        # Get Serie A standings
        classifiche = Classifica.objects.filter(campionato=serie_a).order_by('posizione')

        # Get all Serie A matchdays
        giornate = Giornata.objects.filter(campionato=serie_a).order_by('numero')

        # Get selected matchday or default to the first one
        giornata_selezionata_id = request.GET.get('giornata')
        if giornata_selezionata_id:
            giornata_selezionata = Giornata.objects.get(id=giornata_selezionata_id)
        elif giornate.exists():
            giornata_selezionata = giornate.first()
        else:
            giornata_selezionata = None

        # Get Serie A matches for the selected matchday or all if none selected
        if giornata_selezionata:
            partite = Partita.objects.filter(campionato=serie_a, giornata=giornata_selezionata)
        else:
            partite = Partita.objects.filter(campionato=serie_a)

        context = {
            'classifiche': classifiche,
            'partite': partite,
            'giornate': giornate,
            'giornata_selezionata': giornata_selezionata
        }
    except Campionato.DoesNotExist:
        # Handle case where Serie A doesn't exist
        context = {
            'error': 'Campionato Serie A non trovato nel database.'
        }

    return render(request, 'principale.html', context)

def login_responsabile(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
        print(f"Email: {email}, Password: {password}, Hash: {hashed_password}")

        try:
            responsabile = Responsabile.objects.get(email=email)
            if responsabile.password == password:
                # Authentication successful
                request.session['user_id'] = responsabile.email
                request.session['user_type'] = 'responsabile'
                return redirect('principale_responsabile')
            else:
                # Password incorrect
                return render(request, 'login_responsabile.html', {'error': 'Password non corretta'})
        except Responsabile.DoesNotExist:
            # User not found
            return render(request, 'login_responsabile.html', {'error': 'Email non trovata'})

    return render(request, 'login_responsabile.html')


def authenticated_arbitro(email, password):
    return Arbitro.objects.filter(email=email, password=password).exists()


def login_arbitro(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        hashed_password = request.POST.get('password')
        print(f"Email: {email}, Password: {hashed_password}")

        if authenticated_arbitro(email, hashed_password):
            request.session['arbitro_email'] = email
            return redirect('principale_arbitro')
        else:
            print("Login fallito")
            return render(request, 'login_arbitro.html', {'error_message': "Credenziali errate"})
    else:
        return render(request, 'login_arbitro.html')



def login_dirigente(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
        print(f"Email: {email}, Password: {password}, Hash: {hashed_password}")

        try:
            dirigente = Dirigente.objects.get(email=email)
            if dirigente.password == password:
                # Authentication successful
                request.session['user_id'] = dirigente.email
                request.session['user_type'] = 'dirigente'
                return redirect('principale_dirigente')
            else:
                # Password incorrect
                return render(request, 'login_dirigente.html', {'error': 'Password non corretta'})
        except Dirigente.DoesNotExist:
            # User not found
            return render(request, 'login_dirigente.html', {'error': 'Email non trovata'})

    return render(request, 'login_dirigente.html')

# Viste protette con 2FA
@login_required
def principale_responsabile(request):
    # Get the logged-in responsabile
    try:
        responsabile_email = request.session.get('user_id')
        responsabile = Responsabile.objects.get(email=responsabile_email)

        # Handle referto deletion
        if request.method == 'POST' and 'delete_referto' in request.POST:
            referto_id = request.POST.get('delete_referto')
            try:
                referto = Referto.objects.get(id=referto_id)
                referto.delete()
                messages.success(request, 'Referto eliminato con successo!')
                return redirect('principale_responsabile')
            except Referto.DoesNotExist:
                messages.error(request, 'Referto non trovato.')

        # Get all referti
        referti = Referto.objects.all().order_by('-data_referto')

        context = {
            'user_type': 'Responsabile',
            'user': request.user,
            'responsabile': responsabile,
            'referti': referti,
        }
        return render(request, 'principale_responsabile.html', context)
    except Responsabile.DoesNotExist:
        return redirect('login_responsabile')

@login_required
def principale_arbitro(request):
    # Get the logged-in arbitro
    try:
        arbitro_email = request.session.get('arbitro_email')
        arbitro = Arbitro.objects.get(email=arbitro_email)

        # Get all partite for the form
        partite = Partita.objects.all().order_by('-data')

        # Get existing referti for this arbitro
        referti = Referto.objects.filter(arbitro=arbitro).order_by('-data_referto')

        # Handle form submission
        if request.method == 'POST':
            partita_id = request.POST.get('partita')
            note = request.POST.get('note')

            if partita_id:
                try:
                    partita = Partita.objects.get(id=partita_id)

                    # Create new referto
                    referto = Referto(
                        arbitro=arbitro,
                        partita=partita,
                        note=note
                    )
                    referto.save()

                    messages.success(request, 'Referto creato con successo!')
                    return redirect('principale_arbitro')
                except Partita.DoesNotExist:
                    messages.error(request, 'Partita non trovata.')
            else:
                messages.error(request, 'Seleziona una partita.')

        context = {
            'user_type': 'Arbitro',
            'user': request.user,
            'arbitro': arbitro,
            'partite': partite,
            'referti': referti,
        }
        return render(request, 'principale_arbitro.html', context)
    except Arbitro.DoesNotExist:
        return redirect('login_arbitro')

@login_required
def principale_dirigente(request):
    # Logica per la pagina del dirigente
    context = {
        'user_type': 'Dirigente',
        'user': request.user,
        # aggiungi i tuoi dati specifici
    }
    return render(request, 'principale_dirigente.html', context)
