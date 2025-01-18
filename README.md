# **Lagerverwaltungssystem**

## **Überblick**
Das Lagerverwaltungssystem ist eine webbasierte Anwendung zur Verwaltung von Lagerbeständen, Artikeln und Benutzerzugriffen. Es ermöglicht mehreren Benutzern, zusammenzuarbeiten, Lagerbestände zu verwalten und Artikeltransaktionen wie Wareneingang und -ausgang effizient zu protokollieren. Der Fokus liegt auf Benutzerfreundlichkeit, Sicherheit und flexibler Zuweisung von Nutzern zu spezifischen Lagern.

---

## **Funktionen**

### **1. Benutzerverwaltung**
- **Registrierung und Login:**
  - Benutzer können sich registrieren und anmelden.
  - Nach der Registrierung werden Benutzer automatisch eingeloggt.
- **Benutzerrollen:**
  - Der Eigentümer eines Lagers kann anderen Benutzern Zugriff gewähren oder diesen entziehen.
- **Benutzerzuweisung:**
  - Besitzer eines Lagers können Benutzer zu einem Lager hinzufügen, sodass diese gemeinsam daran arbeiten können.

### **2. Lagerverwaltung**
- **Lager erstellen:**
  - Benutzer können Lager anlegen und verwalten.
- **Lagerübersicht:**
  - Eine Übersicht aller Lager, die einem Benutzer zugewiesen sind.
- **Detailansicht eines Lagers:**
  - Zeigt Artikel und Benutzer an, die einem Lager zugeordnet sind.
- **Benutzerzugriffsverwaltung:**
  - Besitzer können Benutzer zu einem Lager hinzufügen oder entfernen.

### **3. Artikelverwaltung**
- **Artikel erstellen:**
  - Artikel können einem Lager hinzugefügt werden, mit Angaben wie Name, Beschreibung und Menge.
- **Artikel bearbeiten:**
  - Eigenschaften von Artikeln wie Menge oder Beschreibung können geändert werden.
- **Artikelübersicht:**
  - Eine Tabelle zeigt alle Artikel in einem Lager mit ihren aktuellen Beständen.

### **4. Transaktionen**
- **Wareneingang und -ausgang:**
  - Benutzer können Transaktionen für Artikel durchführen, z. B. die Menge erhöhen (Eingang) oder verringern (Ausgang).
- **Protokollierung (optional):**
  - Transaktionen können für spätere Referenzen gespeichert werden, um Änderungen im Lagerbestand nachzuverfolgen.

---
# Lagerverwaltungsprogramm

Dies ist ein Lagerverwaltungsprogramm, das es Benutzern ermöglicht, Artikel in Lägern zu verwalten, Benutzer zuzuweisen, Transaktionen durchzuführen und vieles mehr.

## **Voraussetzungen**

- **Python 3.10 oder höher** (Falls noch nicht installiert: [Download Python](https://www.python.org/downloads/))
- **Virtuelle Umgebung** (Empfohlen, um Abhängigkeiten zu isolieren)
- **Git** (Falls das Repository per Git geklont werden soll)
- **Installierte Python-Abhängigkeiten** aus `requirements.txt`

## **Schritte zur Ausführung des Projekts**

### 1. **Repository klonen**

Klonen Sie das Projekt-Repository auf Ihrem lokalen Rechner:
```bash
git clone git@github.com:GaliosAngelos/lagerverwaltung.git lagerverwaltungsprogramm
```
## Hinweise zur Einrichtung

### Hinweis:
Falls Sie **Git** nicht installiert haben, können Sie es [hier herunterladen](https://git-scm.com/).

### 2. In das Projektverzeichnis wechseln

Wechseln Sie in das Verzeichnis des geklonten Projekts:
```bash
cd lagerverwaltungsprogramm