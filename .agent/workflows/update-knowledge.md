---
description: Workflow da seguire quando si modificano template, si aggiungono documenti o si cambiano strutture nel vault Travel-Vault. Garantisce che la knowledge base AI rimanga sincronizzata.
---

# Aggiornamento Knowledge Base

Ogni volta che si modifica la struttura o il contenuto del vault, seguire questi passaggi per mantenere la knowledge base AI sincronizzata.

## Quando eseguire questo workflow

- Dopo aver creato/modificato un **template** in `_templates/`
- Dopo aver aggiunto una **nuova destinazione**
- Dopo aver aggiunto/rimosso **file significativi** (itinerari, location, info)
- Dopo aver cambiato la **struttura delle cartelle**

## Passaggi

### 1. Aggiornare `_AI/INDEX.md`

// turbo
Verificare che l'albero delle cartelle e la quick reference table riflettano la struttura attuale:

```
File: _AI/INDEX.md
- Aggiornare il tree se ci sono nuove cartelle o file
- Aggiornare la tabella "Quick Reference" se ci sono nuovi entry point
```

### 2. Aggiornare la knowledge base per destinazione

Se i cambiamenti riguardano una destinazione specifica, aggiornare i file in `_AI/knowledge/destinations/<dest>/`:

- `locations.md` → se aggiunti/rimossi/modificati luoghi
- `itinerari.md` → se aggiunti/rimossi itinerari
- `logistica.md` → se cambiata info su trasporti, pass, budget

### 3. Aggiornare la skill `travel-vault-agent`

Se il cambiamento riguarda template, convenzioni o struttura del vault:

```
File: .agents/skills/travel-vault-agent/SKILL.md
- Aggiornare la sezione "Template Types" se ci sono nuovi template
- Aggiornare "Vault Structure" se cambiata struttura cartelle
- Aggiornare "Key Conventions" se nuovi pattern
```

```
File: .agents/skills/travel-vault-agent/references/templates.md
- Aggiornare la documentazione dettagliata del template modificato
```

### 4. Aggiornare `_AI/knowledge/workspace.md`

// turbo
Solo se cambiate convenzioni globali o struttura vault principale.

### 5. Verificare consistenza

// turbo
Controllare che il frontmatter dei nuovi file segua lo standard (campo `type`, `destination`, `tags`). Se necessario, eseguire:

```bash
python _AI/scripts/add_frontmatter.py
```
