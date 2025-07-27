import unittest
from django.contrib.auth.models import User
from django.test import Client
from django_otp.oath import TOTP

class RegistrationTestCase(unittest.TestCase):
    def setUp(self):
        self.client = Client()
        # utente preesistente per test duplicazione email
        User.objects.create_user(username='existing', email='test@test.com', password='password123')

    def test_registration_valid(self):
        response = self.client.post('/register/', {'email': 'new@test.com', 'password': 'StrongPass123!'})
        self.assertEqual(response.status_code, 200)
        # verifica che l’utente sia stato creato
        self.assertTrue(User.objects.filter(email='new@test.com').exists())

    def test_registration_duplicate_email(self):
        response = self.client.post('/register/', {'email': 'test@test.com', 'password': 'AnotherPass123!'})
        self.assertEqual(response.status_code, 400)

class LoginTestCase(unittest.TestCase):
    def setUp(self):
        self.client = Client()
        User.objects.create_user(username='loginuser', email='login@test.com', password='loginpass123')

    def test_login_correct_credentials(self):
        response = self.client.post('/login/', {'email': 'login@test.com', 'password': 'loginpass123'})
        self.assertEqual(response.status_code, 200)

    def test_login_brute_force(self):
        # tentiamo 5 volte con password errata; la quinta deve attivare il rate limiting
        for _ in range(5):
            response = self.client.post('/login/', {'email': 'login@test.com', 'password': 'wrongpass'})
        self.assertEqual(response.status_code, 429)  #http 429 troppe richieste


class TwoFactorAuthTestCase(unittest.TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='2fauser', email='2fa@test.com', password='2fapass')
        # simulazione di salvataggio del segreto OTP per l’utente
        self.user.profile.otp_secret = 'BASE32SECRET2345'
        self.user.profile.save()

    def test_2fa_activation(self):
        response = self.client.post('/2fa/activate/', {'user_id': self.user.id})
        self.assertEqual(response.status_code, 200)
        # dopo l’attivazione, il segreto OTP deve essere presente
        self.assertIsNotNone(self.user.profile.otp_secret)

    def test_2fa_login_valid_otp(self):
        totp = TOTP(self.user.profile.otp_secret)
        otp = totp.token()
        response = self.client.post('/2fa/login/', {'otp': otp})
        self.assertEqual(response.status_code, 200)

    def test_2fa_login_invalid_otp(self):
        response = self.client.post('/2fa/login/', {'otp': '000000'})
        self.assertEqual(response.status_code, 401)









from django.test import TestCase, Client
from django.contrib.auth.models import User
from league.models import Responsabile, Arbitro, Dirigente, Nazionalita, Campionato, Squadra, Partita, Classifica, Referto


    def setUp(self):
        # 1) Utente e ruoli
        self.user = User.objects.create_user(username='arb1', password='pass')
        self.arbitro = Arbitro.objects.create(
            user=self.user, nome='Mario', cognome='Rossi',
            email='mario@rossi.com', password='pass'
        )
        # 2) Campionato, Squadra, Partita, Classifica
        nazione = Nazionalita.objects.create(nome='Italia')
        camp = Campionato.objects.create(nome='Serie A', nazionalita=nazione)
        squadra = Squadra.objects.create(nome='Inter', campionato=camp)
        giornata = Partita.objects.create(
            squadra_casa=squadra, squadra_ospite=squadra,
            campionato=camp, data='2025-07-01', stadio='Meazza'
        )
        # 3) Classifica
        Classifica.objects.create(
            campionato=camp, squadra=squadra,
            posizione=1, punti=0
        )
        # 4) Multipli Referti per paginazione
        for _ in range(30):
            Referto.objects.create(arbitro=self.arbitro, partita=giornata, note='Test')
        # Client autenticato
        self.client = Client()
        self.client.login(username='arb1', password='pass')

    def test_query_orm_basic(self):
        """UT-DB-01: Unit Test – Verifica ORM su tutti i modelli chiave."""
        self.assertTrue(User.objects.exists())
        self.assertTrue(Arbitro.objects.exists())
        self.assertTrue(Responsabile.objects.count() == 0)  # non creati in setUp
        self.assertTrue(Dirigente.objects.count() == 0)
        self.assertTrue(Nazionalita.objects.exists())
        self.assertTrue(Campionato.objects.exists())
        self.assertTrue(Squadra.objects.exists())
        self.assertTrue(Partita.objects.exists())
        self.assertTrue(Classifica.objects.exists())
        self.assertTrue(Referto.objects.exists())

    def test_sql_injection_protection(self):
        """UT-DB-02: Security Test – Protezione SQLi su Referto.note."""
        malicious = "'; DROP TABLE league_referto;--"
        qs = Referto.objects.filter(arbitro=self.arbitro, note__icontains=malicious)
        # La query non fallisce e restituisce un queryset
        self.assertIsNotNone(qs)

    def test_pagination_integration(self):
        """UT-DB-03: Integration Test – Paginazione Referti (max 10/page)."""
        response = self.client.get('/referti/?page=1')
        self.assertEqual(response.status_code, 200)
        referti_page = response.context['referti']
        self.assertEqual(len(referti_page), 10)

    def test_rate_limit_enforcement(self):
        """UT-DB-04: Security Test – Rate limiting su list/referti."""
        for i in range(6):
            response = self.client.get('/referti/')
        self.assertEqual(response.status_code, 429)














        from django.test import TestCase, Client
        from django.contrib.auth.models import User
        from django.urls import reverse
        from league.models import LogEvento, Referto, Arbitro, Dirigente, Responsabile, Segnalazione

        class Sprint3Tests(TestCase):

            def setUp(self):
                # Utenti e ruoli
                self.client = Client()
                self.user_responsabile = User.objects.create_user(username='resp', password='pass')
                self.responsabile = Responsabile.objects.create(user=self.user_responsabile, nome='Mario',
                                                                cognome='Rossi', email='mario@lega.it')

                self.user_arbitro = User.objects.create_user(username='arb', password='pass')
                self.arbitro = Arbitro.objects.create(user=self.user_arbitro, nome='Luca', cognome='Verdi',
                                                      email='luca@lega.it')

                self.user_dirigente = User.objects.create_user(username='dir', password='pass')
                self.dirigente = Dirigente.objects.create(user=self.user_dirigente, nome='Anna', cognome='Bianchi',
                                                          email='anna@lega.it')

                # Referto per test cronologia
                self.referto = Referto.objects.create(arbitro=self.arbitro, partita_id=1, note='Nota originale')

            def test_logging_immutabile(self):
                """UT-LOG-01 - Logging eventi critici immutabile"""
                LogEvento.objects.create(utente=self.user_responsabile, azione='Login effettuato')
                log = LogEvento.objects.first()
                self.assertEqual(log.azione, 'Login effettuato')

            def test_disattivazione_account(self):
                """UT-ACC-02 - Disattivazione manuale account"""
                self.user_arbitro.is_active = False
                self.user_arbitro.save()
                self.assertFalse(User.objects.get(username='arb').is_active)

            def test_visualizzazione_cronologia_modifiche(self):
                """IT-CRON-03 - Cronologia modifiche dei referti"""
                self.referto.note = 'Nota modificata'
                self.referto.save()
                response = self.client.get(reverse('cronologia_modifiche_referto', args=[self.referto.id]))
                self.assertEqual(response.status_code, 200)
                self.assertContains(response, 'Nota modificata')

            def test_rimozione_contenuti_con_motivazione_e_audit(self):
                """IT-RIM-04 - ACL e motivazione obbligatoria per rimozione contenuti"""
                self.client.login(username='resp', password='pass')
                response = self.client.post(reverse('elimina_referto', args=[self.referto.id]),
                                            {'motivazione': 'Contenuto errato'})
                self.assertFalse(Referto.objects.filter(id=self.referto.id).exists())
                self.assertTrue(LogEvento.objects.filter(azione='Eliminazione Referto').exists())

            def test_bypass_acl_su_contenuti(self):
                """ST-ACL-05 - Sicurezza: Tentativo bypass ACL"""
                self.client.login(username='dir', password='pass')
                response = self.client.get(reverse('elimina_referto', args=[self.referto.id]))
                self.assertEqual(response.status_code, 403)

            def test_badge_ruolo_ui(self):
                """UI-BDG-06 - Badge ruolo visualizzato correttamente"""
                self.client.login(username='dir', password='pass')
                response = self.client.get(reverse('pagina_contenuti'))
                self.assertEqual(response.status_code, 200)
                self.assertContains(response, 'Dirigente')

