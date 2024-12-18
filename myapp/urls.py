from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    # Login
    path('', auth_views.LoginView.as_view(
        template_name='login.html',
        next_page='lager_list'  # Nach dem Login zu Lagerliste weiterleiten
    ), name='login'),

    # Logout
    path('', auth_views.LogoutView.as_view(next_page='/'), name='logout'),

    # Registrierung
    path('register/', views.register, name='register'),

    # Lager-Übersicht (geschützt)
    path('lager/', login_required(views.lager_list), name='lager_list'),

    # Detailansicht eines Lagers (geschützt)
    path('lager/<int:lager_id>/', login_required(views.lager_detail), name='lager_detail'),

    # Benutzer aus Lager entfernen (geschützt)
    path('lager/<int:lager_id>/remove_user/<int:user_id>/', login_required(views.remove_user_from_lager), name='remove_user_from_lager'),

    # Aktueller Stand eines Lagers (geschützt)
    path('lager/<int:lager_id>/current_status/', login_required(views.current_status), name='current_status'),

    # Wareneingang oder -ausgang (geschützt)
    path('lager/<int:lager_id>/transaction/', login_required(views.transaction), name='transaction'),

    # Benutzer Berechtigungen (geschützt)
    path('lager/<int:lager_id>/grant_access/', login_required(views.grant_access), name='grant_access'),

    # Lager erstellen (geschützt)
    path('lager/create/', login_required(views.lager_create), name='lager_create'),

    # Artikelmanagement (geschützt)
    path('lager/<int:lager_id>/artikel_management/', login_required(views.artikel_management), name='artikel_management'),

    # Artikel erstellen (geschützt)
    path('lager/<int:lager_id>/artikel_management/artikel_create/', login_required(views.artikel_create), name='artikel_create'),

    # Artikel bearbeiten (geschützt)
    path('artikel/<int:id>/edit/', login_required(views.artikel_edit), name='artikel_edit'),
]
