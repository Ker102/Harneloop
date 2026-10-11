<a id="security"></a>
# Sicherheit

Harneloop ist ein lokal ausgerichtetes Framework für agentenerstellte Harness-Einheiten. Sicherheitsgrenzen sind wichtig, weil Agenten Werkzeuge erstellen, Befehle ausführen und wiederverwendbare Einheiten paketieren können.

<a id="current-status"></a>
## Aktueller Stand

Dies ist eine frühe öffentliche Alpha. Betrachtet Harneloop oder eine Harness-Einheit nicht als gehärtete Sandbox oder Sicherheitsgrenze.

<a id="rules"></a>
## Regeln

- Speichert niemals Geheimnisse in Harness-Einheiten.
- Paketiert standardmäßig keine `.env`-Dateien, privaten Schlüssel, Zugangsdaten, Caches oder rohen Laufzeitspuren.
- Behandelt erzeugte Kandidatenwerkzeuge bis zur Prüfung als nicht vertrauenswürdig.
- Nutzt Framework-Befehle für Promotion, Rollback und Paketierung.
- Führt destruktive Aktionen nur mit ausdrücklicher Zustimmung des Nutzers aus.

<a id="reporting"></a>
## Meldungen

Veröffentlicht vermutete Schwachstellen nicht in einem öffentlichen Issue. Nutzt GitHubs privates Formular zur Schwachstellenmeldung, sofern es für dieses Repository verfügbar ist. Andernfalls kontaktiert den Eigentümer privat über das verlinkte GitHub-Profil und nennt Reproduktionsschritte, betroffene Versionen und mögliche Auswirkungen.
