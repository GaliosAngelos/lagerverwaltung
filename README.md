Lagerverwaltungssystem
Überblick

Das Lagerverwaltungssystem ist eine webbasierte Anwendung zur Verwaltung von Lagerbeständen, Artikeln und Benutzerzugriffen. Es ermöglicht mehreren Benutzern, zusammenzuarbeiten, Lagerbestände zu verwalten und Artikeltransaktionen wie Wareneingang und -ausgang effizient zu protokollieren. Der Fokus liegt auf Benutzerfreundlichkeit, Sicherheit und flexibler Zuweisung von Nutzern zu spezifischen Lagern.
Funktionen
1. Benutzerverwaltung

    Registrierung und Login:
        Benutzer können sich registrieren und anmelden.
        Nach der Registrierung werden Benutzer automatisch eingeloggt.
    Benutzerrollen:
        Der Eigentümer eines Lagers kann anderen Benutzern Zugriff gewähren oder diesen entziehen.
    Benutzerzuweisung:
        Besitzer eines Lagers können Benutzer zu einem Lager hinzufügen, sodass diese gemeinsam daran arbeiten können.

2. Lagerverwaltung

    Lager erstellen:
        Benutzer können Lager anlegen und verwalten.
    Lagerübersicht:
        Eine Übersicht aller Lager, die einem Benutzer zugewiesen sind.
    Detailansicht eines Lagers:
        Zeigt Artikel und Benutzer an, die einem Lager zugeordnet sind.
    Benutzerzugriffsverwaltung:
        Besitzer können Benutzer zu einem Lager hinzufügen oder entfernen.

3. Artikelverwaltung

    Artikel erstellen:
        Artikel können einem Lager hinzugefügt werden, mit Angaben wie Name, Beschreibung und Menge.
    Artikel bearbeiten:
        Eigenschaften von Artikeln wie Menge oder Beschreibung können geändert werden.
    Artikelübersicht:
        Eine Tabelle zeigt alle Artikel in einem Lager mit ihren aktuellen Beständen.

4. Transaktionen

    Wareneingang und -ausgang:
        Benutzer können Transaktionen für Artikel durchführen, z. B. die Menge erhöhen (Eingang) oder verringern (Ausgang).
    Protokollierung (optional):
        Transaktionen können für spätere Referenzen gespeichert werden, um Änderungen im Lagerbestand nachzuverfolgen.

Technischer Aufbau
1. Backend

    Framework: Django (Python-basiertes Webframework)
    Datenbankmodell:
        Lager: Enthält Informationen zu jedem Lager, wie Name und Besitzer.
        Artikel: Artikel sind einem Lager zugeordnet und haben Attribute wie Name, Beschreibung und Menge.
        Benutzer: Benutzer können Lager erstellen und gemeinsam verwalten.
        Lagerzugriff (LagerAccess): Speichert die Beziehung zwischen Benutzern und Lagern.
        Transaktionen: Dokumentieren die Änderungen im Lagerbestand.

2. Frontend

    HTML/CSS: Bootstrap für ein ansprechendes, responsives Design.
    Templates: Django-Templates für dynamische HTML-Seiten.
    Icons: Bootstrap Icons für Buttons und visuelle Hinweise.

3. Sicherheitsfeatures

    Benutzerauthentifizierung:
        Nur registrierte und angemeldete Benutzer können auf das System zugreifen.
    Berechtigungsprüfung:
        Nur der Besitzer eines Lagers kann Benutzer hinzufügen oder entfernen.
        Benutzer können nur auf Lager zugreifen, denen sie zugewiesen sind.
