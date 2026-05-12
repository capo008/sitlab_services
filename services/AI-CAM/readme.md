# AI-CAM - Monitoraggio Intelligente con YOLO

Benvenuto nel portale **AI-CAM**, una web-app avanzata per il monitoraggio video in tempo reale potenziata da algoritmi di Intelligenza Artificiale (YOLO) per il rilevamento degli oggetti.

## 🚀 Accesso Rapido
L'applicazione è accessibile pubblicamente al seguente indirizzo:
👉 **[https://aicam.sitai2.duckdns.org/](https://aicam.sitai2.duckdns.org/)**

![screenshot](shot1.png)

---

## 🛠 Funzionalità Principali

### 1. Visualizzazione Fluidi e AI
L'interfaccia principale mostra lo stream video della telecamera selezionata. Puoi scegliere tra due modalità di visualizzazione:
- **Modalità AI (Predefinita)**: Visualizza il video con sovrimpresse le "bounding box" (rettangoli rossi) che identificano gli oggetti rilevati (persone, veicoli, ecc.) in tempo reale, comprensivi di percentuale di confidenza.
- **Modalità Raw**: Visualizza lo stream originale della telecamera senza elaborazione AI, utile per risparmiare banda o per una visione pulita.

### 2. Multi-Camera
Sotto lo schermo principale troverai una griglia di **anteprime (previews)**. 
- Le anteprime si aggiornano automaticamente ogni pochi secondi.
- Per passare da una telecamera all'altra, basta cliccare sul riquadro corrispondente nella griglia.
- La telecamera attiva è evidenziata con un bordo verde brillante.

### 3. Statistiche in Tempo Reale
Nell'angolo in alto a destra dello stream AI, puoi monitorare:
- **FPS (Frames Per Second)**: La fluidità effettiva della visualizzazione.
- **Stato AI**: Indica se la connessione con il server di intelligenza artificiale è attiva.
- **ID Frame**: Il conteggio progressivo dei fotogrammi elaborati.

---

## 🎮 Come Interagire con l'App

### Cambiare Modalità (AI/Raw)
In basso a sinistra, sopra l'etichetta del nome della telecamera, troverai un interruttore (toggle) con la scritta **"Raw"**.
- Sposta l'interruttore verso destra per attivare lo stream diretto.
- Riportalo a sinistra per riattivare il rilevamento oggetti AI.

### Modificare le Telecamere (EDIT IPCAM)
Se desideri aggiungere una nuova telecamera o modificare gli indirizzi (URL) di quelle esistenti:
1. Clicca sul pulsante verde **"EDIT IPCAM"** in alto a destra.
2. Verrà richiesta una **password di amministrazione** (configurata a lato server).
3. Una volta autenticato, potrai inserire nomi e URL degli stream MJPEG.
4. Clicca su **"Salva"** per rendere le modifiche effettive per tutti gli utenti connessi.

---

## ℹ️ Informazioni Tecniche
L'applicazione utilizza una tecnologia basata su **WebSockets (Socket.IO)** per garantire la minima latenza possibile e sincronizzare il cambio di telecamera tra il server e l'interfaccia utente. L'elaborazione delle immagini avviene tramite un cluster AI remoto che comunica costantemente con il proxy video.

---

**Developed by { sitlab team } esperia - bergamo**
