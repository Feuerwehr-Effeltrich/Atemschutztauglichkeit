# Atemschutztauglichkeit

.env
```
EMAIL="john@example.com"
PASSWORD="Sup3rS3cr3t"
```

```
docker compose up -d
```

# Zweiter Kopf

sortiert grün, gelb, rot

[ > Vorname Nachname :green_check: ]

[ v Vorname Nachname :green_check: ] :yellow_!: :red_x:
[ :green_doc: Untersuchung bis 05/2027 ]
[ :green_pen: Unterweisung für 2026 ]
[ :green_arm: Belastungsübung von 2025 ] -1y
[ :green_hammer: Übung/Einsatz 03/2025 ] -6M

ggf immer +15d auf jedes Datum rechnen

Untersuchung: nur Monat/Jahr beachten
Unterweisung: entry.y-1 == current.y -> ok
Belastungsübung: entry.y >= current.y -> ok
Übung/Einsatz: entry >= current -> ok | entry-6M.y >= current.y -> eh | nein

