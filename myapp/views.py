from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .forms import LagerForm, ArtikelForm, CustomUserCreationForm
from .models import Lager, LagerAccess, Artikel, Transaction
from django.contrib.auth.models import User

def register(request):
    """Registrierung eines neuen Benutzers und automatisches Login."""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Automatisches Login nach der Registrierung
            return redirect('lager_list')  # Weiterleitung nach erfolgreichem Login
    else:
        form = CustomUserCreationForm()

    return render(request, 'register.html', {'form': form})

@login_required
def lager_create(request):
    """Erstellt ein neues Lager und ordnet es dem Benutzer zu."""
    if request.method == 'POST':
        form = LagerForm(request.POST)
        if form.is_valid():
            lager = form.save(commit=False)
            lager.owner = request.user  # Dem aktuellen Benutzer zuweisen
            lager.save()
            lager.users.add(request.user)  # Den Ersteller (User) zur Benutzerliste des Lagers hinzufügen
            return redirect('lager_list')  # Nach erfolgreichem Erstellen zur Lagerübersicht
    else:
        form = LagerForm()
    return render(request, 'lager_form.html', {'form': form})


@login_required
def lager_list(request):
    """Zeigt die Liste der Lager des angemeldeten Benutzers."""
    lager = Lager.objects.filter(users=request.user)  # Nur Lager anzeigen, denen der Benutzer zugewiesen ist
    return render(request, 'lager_list.html', {'lager': lager})


@login_required
def remove_user_from_lager(request, lager_id, user_id):
    """Entfernt einen Benutzer aus einem Lager."""
    lager = get_object_or_404(Lager, id=lager_id)

    # Stelle sicher, dass der Benutzer der Eigentümer des Lagers ist
    if lager.owner != request.user:
        return redirect('lager_list')  # Wenn der Benutzer nicht der Eigentümer ist, weiterleiten

    user = get_object_or_404(User, id=user_id)

    # Entferne den Benutzer aus dem Lager
    lager.users.remove(user)

    # Optional: Entferne auch die LagerAccess-Instanz, falls du sie gespeichert hast
    LagerAccess.objects.filter(lager=lager, user=user).delete()

    return redirect('lager_detail', lager_id=lager.id)  # Zurück zur Lager-Detailansicht


# View zum Bearbeiten eines Artikels
def artikel_edit(request, id):
    artikel = get_object_or_404(Artikel, id=id)

    if request.method == 'POST':
        form = ArtikelForm(request.POST, instance=artikel)
        if form.is_valid():
            form.save()
            return redirect('lager_detail', lager_id=artikel.lager.id)
    else:
        form = ArtikelForm(instance=artikel)

    return render(request, 'artikel_edit.html', {'form': form})


# View zum Hinzufügen eines neuen Artikels
def artikel_create(request, lager_id):
    lager = get_object_or_404(Lager, id=lager_id)

    if request.method == 'POST':
        form = ArtikelForm(request.POST)
        if form.is_valid():
            artikel = form.save(commit=False)
            artikel.lager = lager
            artikel.save()
            return redirect('lager_detail', lager_id=lager.id)
    else:
        form = ArtikelForm()

    return render(request, 'artikel_create.html', {'form': form})

@login_required
def artikel_management(request, lager_id):
    """Zeigt eine Übersicht aller Artikel im Lager mit Optionen zum Bearbeiten oder Hinzufügen."""
    lager = get_object_or_404(Lager, id=lager_id)

    # Sicherstellen, dass der Benutzer dem Lager zugeordnet ist
    if request.user not in lager.users.all():
        return redirect('lager_list')

    # Alle Artikel des Lagers abrufen
    artikel_list = lager.artikel.all()

    return render(request, 'artikel_management.html', {
        'lager': lager,
        'artikel_list': artikel_list,
    })

@login_required
def grant_access(request, lager_id):
    """Zuweisung von Benutzern zu einem Lager."""
    # Hole das Lager anhand der ID, überprüfe, ob der Benutzer der Eigentümer ist
    lager = get_object_or_404(Lager, id=lager_id)

    # Stelle sicher, dass der angemeldete Benutzer der Besitzer des Lagers ist
    if lager.owner != request.user:
        return redirect('lager_list')  # Wenn der Benutzer nicht der Eigentümer ist, zurück zur Liste

    if request.method == 'POST':
        # Hole die User-ID aus dem POST-Request
        user_id = request.POST.get('user_id')

        # Vergewissere dich, dass die ID ein gültiger Benutzer ist
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return redirect('lager_list')  # Falls der Benutzer nicht existiert, zurück zur Lagerliste

        # Füge den Benutzer dem Lager hinzu
        lager.users.add(user)

        # Erstelle den Lager-Zugriffsdatensatz für den Benutzer (optional, falls du dies auch benötigst)
        LagerAccess.objects.create(lager=lager, user=user)

        return redirect('lager_detail', lager_id=lager.id)  # Nach der Zuweisung zurück zur Lager-Detailansicht

    # Hole alle Benutzer außer dem aktuellen Benutzer und denen, die bereits zum Lager gehören
    users = User.objects.exclude(id=request.user.id)  # Exkludiere den aktuellen Benutzer
    users = users.exclude(id__in=lager.users.values_list('id', flat=True))  # Exkludiere Benutzer, die bereits zum Lager gehören

    # Render das Template mit den verfügbaren Benutzern, die dem Lager zugewiesen werden können
    return render(request, 'grant_access.html', {'lager': lager, 'users': users})


@login_required
def lager_detail(request, lager_id):
    """Zeigt die Detailansicht eines Lagers mit den zugewiesenen Artikeln und Personen."""
    lager = get_object_or_404(Lager, id=lager_id)

    # Sicherstellen, dass der Benutzer zu diesem Lager gehört
    if request.user not in lager.users.all():
        return redirect('lager_list')  # Wenn der Benutzer nicht zu diesem Lager gehört, weiterleiten

    # Holen der Artikel und der zugewiesenen Personen
    context = {
        'lager': lager,
        'personen': lager.users.all(),  # Alle Benutzer (Personen), die dem Lager zugewiesen sind
    }
    return render(request, 'lager_detail.html', context)


@login_required
def current_status(request, lager_id):
    """Zeigt den aktuellen Status aller Artikel eines Lagers."""
    lager = get_object_or_404(Lager, id=lager_id)

    # Zugriffsprüfung
    if request.user not in lager.users.all():
        return redirect('lager_list')

    # Artikel des Lagers abrufen und nach Beständen sortieren
    articles = lager.artikel.all()

    # Sicherstellen, dass nur Artikel mit einem Bestand größer als 0 angezeigt werden (optional)
    articles = articles.filter(menge__gt=0)

    return render(request, 'current_status.html', {'lager': lager, 'articles': articles})


# Wareneingang oder -ausgang
@login_required
def transaction(request, lager_id):
    """Führt einen Wareneingang oder -ausgang durch."""
    lager = get_object_or_404(Lager, id=lager_id)

    if request.method == "POST":
        # Hole den Transaktionstyp (Zugang oder Abgang) und die Artikel-ID aus dem POST-Request
        transaction_type = request.POST.get("transaction_type")
        article_id = request.POST.get("article")
        quantity = int(request.POST.get("quantity"))

        # Hole den Artikel aus der Datenbank
        article = get_object_or_404(Artikel, id=article_id, lager=lager)

        # Führe die Transaktion durch (Zugang oder Abgang)
        if transaction_type == "in":  # Wareneingang
            article.menge += quantity  # Menge erhöhen
        elif transaction_type == "out":  # Warenabgang
            if article.menge >= quantity:  # Sicherstellen, dass genügend Menge vorhanden ist
                article.menge -= quantity  # Menge verringern
            else:
                # Fehlermeldung, wenn nicht genügend Artikel vorhanden sind
                return render(request, 'transaction.html', {
                    'lager': lager,
                    'form': ArtikelForm(),
                    'error_message': "Nicht genügend Artikel für den Abgang verfügbar!"
                })

        # Speichere die Änderungen am Artikel
        article.save()

        # Erstelle eine Transaktion, um sie zu protokollieren (optional)
        Transaction.objects.create(
            article=article,
            lager=lager,
            type=transaction_type,
            quantity=quantity
        )

        # Nach der Transaktion zur Lager-Detailansicht zurückkehren
        return redirect('lager_detail', lager_id=lager.id)

    else:
        form = ArtikelForm()

    return render(request, 'transaction.html', {'lager': lager, 'form': form})
