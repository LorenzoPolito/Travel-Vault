---
name: git-flow-expert
description: Workflow rigoroso per la gestione di feature, release e hotfix utilizzando la metodologia Git Flow.
---

# Git Flow Expert

Questa skill descrive come gestire lo sviluppo del codice nel progetto Travel-Vault seguendo la filosofia Git Flow.

## Struttura dei Branch

- **`main`**: Codice di produzione. Solo merge stabili. Ogni push qui attiva il deploy automatico.
- **`develop`**: Branch d'integrazione principale. Tutte le nuove feature convergono qui.
- **`feature/*`**: Branch dedicati a singole funzionalità. Partono da `develop` e tornano in `develop`.

## Workflow Operativo

### 1. Iniziare una Feature

```bash
git checkout develop
git pull origin develop
git checkout -b feature/nome-feature
```

### 2. Committare Modifiche

Utilizzare messaggi semantici:
- `feat: ...` per nuove funzionalità.
- `fix: ...` per correzioni di bug.
- `chore: ...` per aggiornamenti di setup o infrastruttura.

### 3. Integrare una Feature

```bash
git checkout develop
git merge --no-ff feature/nome-feature -m "Merge feature/nome-feature into develop - Descrizione"
git push origin develop
```

### 4. Rilascio in Produzione (Release)

```bash
git checkout main
git merge --no-ff develop -m "Release: Descrizione del rilascio"
git push origin main
```

## Regole d'Oro

1. **Mai committare direttamente su `main`**.
2. Usare sempre `--no-ff` nei merge per mantenere la storia dei branch visibile.
3. Assicurarsi di aver eseguito un build locale (`npm run build`) prima del merge in `main`.
4. Stashare o committare modifiche a `.obsidian/workspace.json` prima di cambiare branch.
