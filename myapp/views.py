from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .forms import LagerForm, ArtikelForm, CustomUserCreationForm
from .models import Lager, LagerAccess, Artikel, Transaction
from django.contrib.auth.models import User
from django.contrib import messages


def register(request):
    """Registrierung eines neuen Benutzers und automatisches Login."""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')

            if User.objects.filter(username=username).exists():
                messages.error(request, 'Dieser Benutzername ist bereits vergeben. Bitte wähle einen anderen.')
            elif User.objects.filter(email=email).exists():
                messages.error(request, 'Diese E-Mail-Adresse ist bereits registriert. Bitte benutze eine andere.')
            else:
                user = form.save()
                login(request, user)
                messages.success(request, 'Du hast dich erfolgreich registriert und bist nun eingeloggt!')
                return redirect('lager_list')
        else:
            messages.error(request, 'Bitte korrigiere die Fehler im Formular.')
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
            lager.owner = request.user
            lager.save()
            lager.users.add(request.user)
            messages.success(request, 'Lager wurde erfolgreich erstellt!')
            return redirect('lager_list')
        else:
            messages.error(request, 'Bitte korrigiere die Fehler im Formular.')
    else:
        form = LagerForm()
    return render(request, 'lager_form.html', {'form': form})


@login_required
def lager_list(request):
    """Zeigt die Liste der Lager des angemeldeten Benutzers."""
    lager = Lager.objects.filter(users=request.user)
    if not lager.exists():
        messages.info(request, 'Du hast noch keine Lager angelegt.')
    return render(request, 'lager_list.html', {'lager': lager})


@login_required
def remove_user_from_lager(request, lager_id, user_id):
    """Entfernt einen Benutzer aus einem Lager."""
    lager = get_object_or_404(Lager, id=lager_id)

    if lager.owner != request.user:
        messages.error(request, 'Du hast keine Berechtigung, diesen Benutzer zu entfernen.')
        return redirect('lager_list')

    user = get_object_or_404(User, id=user_id)
    lager.users.remove(user)
    LagerAccess.objects.filter(lager=lager, user=user).delete()

    messages.success(request, f'Benutzer {user.username} wurde erfolgreich aus dem Lager entfernt.')
    return redirect('lager_detail', lager_id=lager.id)


# View zum Bearbeiten eines Artikels
@login_required
def artikel_edit(request, lager_id, id):
    """Bearbeitet einen Artikel im Lager."""
    lager = get_object_or_404(Lager, id=lager_id)
    artikel = get_object_or_404(Artikel, id=id, lager=lager)

    if request.method == 'POST':
        form = ArtikelForm(request.POST, request.FILES, instance=artikel)
        if form.is_valid():
            form.save()
            messages.success(request, 'Artikel wurde erfolgreich bearbeitet!')
            return redirect('artikel_management', lager_id=lager.id)
        else:
            messages.error(request, 'Bitte korrigiere die Fehler im Formular.')
    else:
        form = ArtikelForm(instance=artikel)

    return render(request, 'artikel_edit.html', {'form': form, 'artikel': artikel, 'lager': lager})


# View zum Hinzufügen eines neuen Artikels
def artikel_create(request, lager_id):
    lager = get_object_or_404(Lager, id=lager_id)

    if request.method == 'POST':
        form = ArtikelForm(request.POST, request.FILES)
        if form.is_valid():
            artikel_name = form.cleaned_data['name']

            if Artikel.objects.filter(lager=lager, name=artikel_name).exists():
                messages.error(request, 'Dieser Artikel existiert bereits im Lager!')
                return render(request, 'artikel_create.html', {'form': form, 'lager': lager})

            artikel = form.save(commit=False)
            artikel.lager = lager
            artikel.save()

            messages.success(request, 'Artikel wurde erfolgreich erstellt!')
            return redirect('artikel_management', lager_id=lager.id)
        else:
            messages.error(request, 'Bitte korrigiere die Fehler im Formular.')
    else:
        form = ArtikelForm()

    return render(request, 'artikel_create.html', {'form': form, 'lager': lager})


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
    lager = get_object_or_404(Lager, id=lager_id)

    if lager.owner != request.user:
        messages.error(request, 'Du hast keine Berechtigung, Benutzer zu diesem Lager hinzuzufügen.')
        return redirect('lager_detail', lager_id=lager.id)

    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            messages.error(request, 'Der angegebene Benutzer existiert nicht.')
            return redirect('lager_detail', lager_id=lager.id)

        if user not in lager.users.all():
            lager.users.add(user)
            LagerAccess.objects.create(lager=lager, user=user)
            messages.success(request, f'Benutzer {user.username} wurde erfolgreich dem Lager zugewiesen.')
        else:
            messages.info(request, f'Benutzer {user.username} ist bereits dem Lager zugewiesen.')

        return redirect('lager_detail', lager_id=lager.id)

    users = User.objects.exclude(id=request.user.id).exclude(id__in=lager.users.values_list('id', flat=True))
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

from django.db.models import Q

@login_required
def current_status(request, lager_id):
    """Zeigt den aktuellen Status aller Artikel eines Lagers mit Bild oder Standard-Icon."""
    lager = get_object_or_404(Lager, id=lager_id)

    # Zugriffsprüfung
    if request.user not in lager.users.all():
        return redirect('lager_list')

    # Hole den Suchparameter aus der URL
    search_query = request.GET.get('q', '')  # Der Parameter q
    if search_query:
        # Filtere nach Artikeln, die den Suchbegriff enthalten
        articles = lager.artikel.filter(
            Q(name__icontains=search_query) & Q(menge__gt=0)
        )
    else:
        # Wenn kein Suchbegriff, zeige alle Artikel mit Bestand > 0
        articles = lager.artikel.filter(menge__gt=0)

    return render(request, 'current_status.html', {
        'lager': lager,
        'articles': articles,
    })



# Wareneingang oder -ausgang
@login_required
def transaction(request, lager_id):
    """Führt einen Wareneingang oder -ausgang durch."""
    lager = get_object_or_404(Lager, id=lager_id)

    if request.method == "POST":
        transaction_type = request.POST.get("transaction_type")
        article_id = request.POST.get("article")
        quantity = int(request.POST.get("quantity"))

        article = get_object_or_404(Artikel, id=article_id, lager=lager)

        if transaction_type == "in":
            article.menge += quantity
        elif transaction_type == "out":
            if article.menge >= quantity:
                article.menge -= quantity
            else:
                messages.error(request, "Nicht genügend Artikel für den Abgang verfügbar!")
                return redirect('transaction', lager_id=lager.id)

        article.save()
        Transaction.objects.create(article=article, lager=lager, type=transaction_type, quantity=quantity)
        messages.success(request, 'Transaktion erfolgreich durchgeführt!')
        return redirect('lager_detail', lager_id=lager.id)

    form = ArtikelForm()
    return render(request, 'transaction.html', {'lager': lager, 'form': form})
