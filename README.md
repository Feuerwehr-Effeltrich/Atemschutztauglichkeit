# Atemschutz-Tauglichkeit Scraper

Dieses Projekt lädt automatisch die Atemschutztauglichkeits-Liste aus dem FW-Portal herunter, wertet sie aus und stellt sie als Webseite dar.

## Features

-   **Automatischer Download:** Lädt täglich die aktuelle Liste der Atemschutztauglichkeiten aus dem FW-Portal.
-   **Auswertung:** Analysiert die Liste und berechnet den Status für jeden Kameraden basierend auf den folgenden Kriterien:
    -   Ärztliche Untersuchung (G26.3)
    -   Jährliche Unterweisung
    -   Belastungsübung in der Atemschutz-Übungsanlage
    -   Letzte Übung oder Einsatz unter Atemschutz
-   **Web-Oberfläche:** Zeigt eine übersichtliche Liste aller Atemschutzgeräteträger mit ihrem jeweiligen Status (grün, gelb, rot).
-   **Sortierung:** Die Liste ist nach dem Gesamtstatus und anschließend alphabetisch nach Nachnamen sortiert.
-   **API:** Stellt die aufbereiteten Daten auch als JSON-API unter `/api.json` zur Verfügung.

## Setup

1.  **Umgebungsvariablen:**
    Erstelle eine `.env` Datei im Hauptverzeichnis des Projekts. Diese Datei wird von `docker-compose` automatisch geladen.

    ```env
    EMAIL="deine-email@deinedomain.de"
    PASSWORD="dein-passwort"
    ```

2.  **Docker:**
    Stelle sicher, dass Docker und Docker Compose auf deinem System installiert sind.

## Verwendung

Starte die Anwendung mit folgendem Befehl:

```bash
docker compose up -d
```

Die Web-Oberfläche ist dann unter [http://localhost:8000](http://localhost:8000) erreichbar.

Die Daten werden automatisch jeden Tag um 02:00 Uhr morgens aktualisiert. Eine manuelle Aktualisierung kann durch einen POST-Request auf `/update` ausgelöst werden, z.B. mit `curl`:

```bash
curl -X POST http://localhost:8000/update
```

## Funktionsweise

Die Anwendung besteht aus mehreren Komponenten:

-   **`download.py`:** Meldet sich im FW-Portal an und lädt die Excel-Datei mit den Tauglichkeitsdaten herunter.
-   **`parse.py`:** Liest die heruntergeladene Excel-Datei und extrahiert die relevanten Informationen für jeden Kameraden.
-   **`main.py`:**
    -   Verwendet `FastAPI` um einen Webserver bereitzustellen.
    -   Kombiniert die Funktionalität von `download.py` und `parse.py`.
    -   Berechnet den Status für die einzelnen Kriterien und den Gesamtstatus.
    -   Stellt die Daten für die Web-Oberfläche und die JSON-API bereit.
    -   Verwendet `schedule` um die Daten täglich zu aktualisieren.
-   **`templates/index.html`:** Eine Jinja2-Vorlage, die die aufbereiteten Daten als HTML-Seite darstellt.
-   **`static/`:** Enthält statische Dateien wie CSS und JavaScript.
-   **`Dockerfile` & `compose.yml`:** Definieren den Docker-Container und den Service für die einfache Bereitstellung.