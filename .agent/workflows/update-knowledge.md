---
description: Workflow da seguire quando si modifica il vault Travel-Vault (prenotazioni, spese, itinerario, template, struttura). Rimanda al protocollo unico in AGENTS.md.
---

# Aggiornamento Knowledge Base

Il protocollo è **unico per tutti gli harness** ed è in `AGENTS.md` (root):

1. Leggi `AGENTS.md` → sezioni **Fonti di verità**, **Protocollo di lavoro** e **Cosa aggiornare quando cambia…**
2. Applica i quattro passi: analizza → valuta l'impatto → agisci → verifica
3. Verifica finale:

// turbo
```bash
python3 _AI/scripts/vault_check.py
```

Non aggiungere regole in questo file: aggiornare `AGENTS.md`.
