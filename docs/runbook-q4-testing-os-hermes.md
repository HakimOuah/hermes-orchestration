# Runbook — monter le Q4 Testing OS v2 sur Hermes

**Orchestrateur : ChatGPT (`gpt-5.6-sol` via `openai-codex`). Workers : Grok (`grok-4.6` via `xai-oauth`).**

Écrit le 04/09/2026 à partir de l'installation réelle (`hermes v0.21.0`, Bot Mode, profils `oh-*`).
La semaine v2 qu'il implémente est décrite dans
`boutiques-drop/boutique-pipeline/plans/2026-09-04-audit-q4-testing-os.md`. Ce runbook ne porte
aucune méthode métier : il dit qui tourne où, sur quel modèle, et par quel mécanisme.

**Journal d'application.** Étape 1 faite par Hakim le 04/09 (workers sur `grok-4.6`, contradicteur sur
`gpt-6-astra`). Étapes 2 à 5 appliquées par Claude Code le 04/09 au soir ; les syntaxes ci-dessous
sont celles qui ont réellement fonctionné (trois corrections par rapport à la première rédaction,
signalées « corrigé le 04/09 »). Étape 6 (test de fumée) : à faire par Hakim — la chaîne C0 du
rasoir existe sur le board, carte de tête **bloquée** `needs_input` `t_e820a54d`.

---

## 0. État constaté le 04/09

| Profil | Rôle | Modèle actuel | Gateway |
|---|---|---|---|
| `oh-ventures` | manager, point d'entrée unique de Hakim | `gpt-5.6-sol` / `openai-codex` | **running**, Telegram (chat 1446617639) |
| `oh-contradicteur` | contrôle indépendant | `gpt-5.6-sol` / `openai-codex` | stopped |
| `oh-scout` `oh-ideation` `oh-filtre` `oh-demande` `oh-sourcing` `oh-concurrence` `oh-marge` | workers de phase | **`gpt-5.6-sol` / `openai-codex`** | stopped |

Trois constats qui changent la procédure :

1. **Les workers ne sont pas sur Grok.** Les sept profils de phase tournent sur GPT. « Workers Grok »
   n'est vrai aujourd'hui que pour les sous-agents `delegate_task` (clé `delegation.model` = `grok-4.6`),
   que le skill `recherche-produit` n'utilise qu'en repli. Les Bots `@oh-*` que le skill appelle par
   `message_agent` sont des sessions GPT. C'est l'écart n°1 à corriger.
2. **Le kanban a un modèle par tâche.** `hermes kanban create --model … --provider …` et
   `hermes kanban set-model` existent. La contrainte notée le 30/08 (« un modèle par rôle coûte un
   processus ») ne vaut que pour `delegate_task`. Le kanban lève cette limite sans Swarm.
3. **Aucun board OH, aucune routine OH.** Le seul board est `db-industrie` ; les deux crons actifs
   sont DB-Industrie. Les identifiants xAI et Codex sont bien présents dans chaque profil `oh-*`
   (`auth.json` partagé), donc le changement de modèle est immédiat.

Les skills sont portés dans chaque profil (`skills/oh-ventures/` et `skills/oh-ventures-roles/`) par
`boutiques-drop/scripts/porter-skills-hermes.py`. Chaque worker a un `SOUL.md` de rôle qui dit
« sous la direction du manager `@oh-ventures` ». Le `SOUL.md` de `oh-ventures`, lui, est le texte
générique de Hermes : le manager n'a pas d'identité écrite. Étape 5.

---

## 1. Architecture cible : trois mécanismes, chacun à sa place

```
Hakim ── Telegram / Desktop ──► @oh-ventures  (GPT, Bot Chat = conversation)
                                     │
                                     │ kanban_create / kanban_link      (toolset kanban)
                                     ▼
                        board `oh-ventures-q4`  (SQLite, durable, journalisé)
                        cartes = produit × couloir, tenant = slug produit
                                     │
            dispatcher (dans la gateway oh-ventures, tick 60 s)
                                     │  spawn `hermes -p <assignee> chat -q …`
          ┌──────────┬──────────┬────┴─────┬───────────┬────────────┐
       oh-scout  oh-ideation  oh-demande  oh-sourcing  oh-marge …   (Grok)
                                                       oh-contradicteur (GPT — autre modèle)
                                     │
                          branche agents/<mission>-<date>  → GitHub
                                     │
        cron (routines du profil oh-ventures) : samedi veille · lundi pool · jeudi contrôles · vendredi relevé
```

| Mécanisme | Sert à | Ne sert pas à |
|---|---|---|
| **Bot Mode + `message_agent`** | la conversation : comité du lundi, questions, gates. Hakim ne parle qu'à `@oh-ventures`. | exécuter des phases longues (une session Bot n'est ni durable ni rejouable) |
| **Kanban** | le tableau glissant à cinq couloirs (C0 à C4) : une carte par produit et par couloir, dépendances, logs, gates humaines (`blocked · needs_input`) | décider (aucune carte ne prononce GO_FINAL) |
| **Cron** | les rituels datés de la semaine v2 | remplacer Hakim sur Ads et GMC (Hermes n'y a aucun accès) |

Modèles : `oh-ventures` et `oh-contradicteur` restent GPT. Les sept workers passent Grok. Le
contradicteur doit rester sur un **autre modèle que les workers** (décision 31/08) : avec ce
partage, c'est automatique.

---

## 2. Étape 1 — passer les sept workers sur Grok (10 min)

```bash
for p in oh-scout oh-ideation oh-filtre oh-demande oh-sourcing oh-concurrence oh-marge; do
  hermes -p "$p" config set model.default grok-4.6
  hermes -p "$p" config set model.provider xai-oauth
done
hermes profile list        # colonne Model : grok-4.6 sur les sept, gpt-5.6-sol sur oh-ventures et oh-contradicteur
hermes -p oh-scout chat -q "Réponds en un mot : quel modèle es-tu ?"
```

Équivalent Desktop : clic droit sur le Bot → *Edit Profile* → *Model & provider pin*.

Ne pas toucher `delegation.model` dans ces profils (déjà `grok-4.6`) ni le profil `default`, qui
sert DB-Industrie.

**Limite à connaître.** `xai-oauth` est l'abonnement SuperGrok, pas une clé API : sept workers en
parallèle peuvent déclencher des 429. Le dispatcher les gère (`respawn_guarded · blocker_auth`,
la carte reste `ready` et repart au tick suivant), mais il faut plafonner la largeur :
`hermes kanban dispatch --max 3` au début, puis mesurer.

---

## 3. Étape 2 — créer le board du Q4 OS (5 min)

```bash
hermes kanban boards create oh-ventures-q4 \
  --name "OH Ventures — Q4 Testing OS" \
  --description "Tableau glissant produit × couloir. Méthode : boutique-pipeline/plans/2026-09-04-audit-q4-testing-os.md" \
  --default-workdir "/Users/Hakim/Documents/Boutiques drop/boutique-pipeline" \
  --switch
hermes -p oh-ventures kanban boards list      # le board doit être visible depuis le profil manager
```

Réglages du profil manager :

```bash
hermes -p oh-ventures config set kanban.orchestrator_profile oh-ventures
hermes -p oh-ventures config set kanban.auto_decompose false
```

**Corrigé le 04/09 — activer le toolset `kanban` sur le manager.** `hermes tools enable kanban`
répond « Unknown toolset » : le toolset est gardé, il n'apparaît pas dans le sélecteur. La garde
(`tools/kanban_tools.py`, `_profile_has_kanban_toolset`) lit une clé **de premier niveau**
`toolsets:` dans la `config.yaml` du profil, et seul ce module lit cette clé. Il suffit donc
d'ajouter dans `~/.hermes/profiles/oh-ventures/config.yaml` :

```yaml
toolsets:
  - kanban
```

Les outils `kanban_create`, `kanban_list`, `kanban_link`, `kanban_unblock` apparaissent alors dans
les sessions du profil (CLI, Telegram, cron). Ces réglages sont dans la config du **profil**, pas
dans la config racine, qui sert DB-Industrie et garde son `auto_decompose` à vrai : ne jamais poser
une carte OH en `triage`, c'est la seule colonne que le décomposeur générique touche.

`auto_decompose: false` est important : le décomposeur intégré fabrique un graphe générique à
partir des descriptions de profils. On veut que ce soit `@oh-ventures`, avec le skill
`recherche-produit`, qui crée les cartes selon la chaîne de phases. Mode Manuel, donc.

Le dispatcher tourne **dans la gateway** ; celle d'`oh-ventures` est déjà running. Les workers
n'ont pas besoin de gateway : ils sont lancés à la demande (`hermes -p oh-scout chat -q …`) dans
l'espace de travail de la carte. Après le premier tick, vérifier `hermes kanban diagnostics` : la
gateway `default` (DB-Industrie) tourne aussi, et chaque gateway balaie tous les boards. Les
réclamations sont atomiques, donc pas de double exécution, mais c'est à confirmer une fois.

---

## 4. Étape 3 — encoder les couloirs comme convention de cartes

Le kanban n'a pas de notion de couloir : on l'encode dans le titre, le tenant et l'assignee.

| Couloir | Titre | Tenant | Assignee | Terminaison |
|---|---|---|---|---|
| C0 veille | `[C0] <phase> — <produit>` | slug produit | chaîne `oh-scout → oh-ideation → oh-filtre → oh-demande → (oh-sourcing ‖ oh-concurrence) → oh-marge → oh-contradicteur`, liée par `--parent` | `kanban_complete` avec le chemin du rapport et la branche |
| C1 comité | `[C1] Décision — <produit>` | slug | `oh-ventures` : assemble le dossier puis `kanban_block(kind=needs_input, "GO_FINAL Hakim")` | Hakim commente `GO_FINAL` / `WATCH_FINAL` / `NO_GO_FINAL` puis `unblock` |
| C2 build | `[C2] <étape> — <produit>` | slug | **aujourd'hui Claude Code / Codex**, carte de suivi assignée à `oh-ventures` (voir §8) | `kanban_complete` avec l'URL de la boutique et le chemin de la croyance |
| C3 test | `[C3] Lancement — <produit>` puis `[C3] J+1 / J+3 / J+7 — <produit>` | slug | `oh-ventures`, `kanban_block(needs_input, "SAMPLE_OK + lancement Hakim")` ; les cartes J+n reçoivent les chiffres Ads **en commentaire** (Hermes n'a pas accès à Google Ads) | complète quand la dépense atteint le seuil écrit |
| C4 verdict | `[C4] Verdict — <produit>` | slug | `oh-marge` calcule la grille, écrit `mesures/`, propose ; `oh-contradicteur` relit ; Hakim tranche | `kanban_block(needs_input)` → décision Hakim |

Exemple, la chaîne C0 d'un candidat déjà en REVIEW :

```bash
B="--board oh-ventures-q4"
T="--tenant rasoir-surete"
P1=$(hermes kanban $B create "[C0] Phase 4A sourcing exact — rasoir de sûreté kit débutant" $T \
      --assignee oh-sourcing --skill phase4-sourcing --skill sourcing-aliexpress \
      --workspace "dir:/Users/Hakim/Documents/Boutiques drop/boutique-pipeline" \
      --body "Entrée : analyses/2026-09-04-approfondissement-rasoir-surete/README.md. Sortie : fiche fournisseur exacte, coût rendu, délai FR. Branche agents/rasoir-sourcing-$(date +%F). Jamais de GO." \
      --max-runtime 2h --json | jq -r .id)
P2=$(hermes kanban $B create "[C0] Phase 5 économie — rasoir de sûreté" $T \
      --assignee oh-marge --skill phase5-marge --parent "$P1" --json | jq -r .id)
hermes kanban $B create "[C0] Audit contradicteur — rasoir de sûreté" $T \
      --assignee oh-contradicteur --skill critique-candidat --skill contradiction --parent "$P2" \
      --body "Preuves brutes seulement : ne lis pas la synthèse de phase 5 avant d'avoir relu les rapports 3, 4A, 4B."
```

**Corrigé le 04/09 — une carte créée est exécutée dans la minute.** `--initial-status blocked` ne
tient pas : la carte a été promue et lancée par le dispatcher de la gateway au tick suivant
(pid tué, réclamation levée à la main). Pour préparer une chaîne sans la lancer, créer les cartes
puis bloquer la tête **immédiatement** avec le motif en positionnel, avant l'option :

```bash
hermes kanban --board oh-ventures-q4 block <id> "Motif du blocage" --kind needs_input
hermes kanban --board oh-ventures-q4 unblock <id>      # quand Hakim lance
```

Les enfants liés par `--parent` restent en `todo` tant que le parent n'est pas `done` : seule la
tête a besoin d'être bloquée.

Une carte dont la qualité exige un modèle plus fort se surcharge à l'unité, sans changer le profil :

```bash
hermes kanban set-model <id> gpt-5.6-sol --provider openai-codex
```

Dans la pratique, `@oh-ventures` crée ces cartes lui-même par `kanban_create` quand Hakim lui dit
« instruis le rasoir jusqu'au contradicteur ». La ligne de commande sert au premier test et au
dépannage.

---

## 5. Étape 4 — les quatre routines (cron du profil `oh-ventures`)

Chaque job est pinned sur GPT (c'est le manager qui parle), livré dans le Bot Chat pour que Hakim
le retrouve au même endroit, et tourne depuis `boutique-pipeline/` pour hériter d'`AGENTS.md`.

**Corrigé le 04/09 — les deux positionnels (horaire, prompt) doivent précéder les options**, sinon
`hermes: error: unrecognized arguments`. Forme qui marche :
`hermes -p oh-ventures cron create "<cron>" "<prompt>" --name … --workdir … --model … --provider … --deliver …`.
Les quatre jobs ci-dessous sont créés (prochains passages : samedi 05/09 8h, lundi 07/09 7h,
jeudi 10/09 9h, vendredi 11/09 9h). Les prompts sont reproduits ici pour la forme ; l'ordre réel des
arguments est celui de la note ci-dessus.

```bash
WD="/Users/Hakim/Documents/Boutiques drop/boutique-pipeline"
COMMON="--workdir $WD --model gpt-5.6-sol --provider openai-codex --deliver bot-chat:oh-ventures"

# Samedi 8h — C0 veille : remplir le pool, jamais décider
hermes -p oh-ventures cron create "0 8 * * 6" --name veille-weekend $COMMON --skill chasse-clusters \
  "Veille C0 du week-end. Lis registre-candidats.md (anti-doublon), prends la famille suivante de la rotation, crée sur le board oh-ventures-q4 la chaîne de cartes C0 (scout → idéation → filtre → demande → sourcing ‖ concurrence → marge → contradicteur) avec tenant = slug et dépendances parent → enfant. Aucun GO, aucune dépense, aucun push sur main."

# Lundi 7h — C1 pool prêt : ce que Hakim a à décider, rien d'autre
hermes -p oh-ventures cron create "0 7 * * 1" --name pool-lundi $COMMON \
  "Liste les cartes C0 terminées depuis lundi dernier dont le verdict est PASS_PREQUALIFICATION avec sourcing exact et audit contradicteur. Pour chacune : produit, volume cœur, coût rendu, prix cible, break-even CPA, réserves du contradicteur, chemin du dossier. Puis les REVIEW avec la preuve qui manque. Cinq lignes par produit maximum. Ne propose aucun GO."

# Jeudi 9h — C3 contrôles : rappeler, pas conclure
hermes -p oh-ventures cron create "0 9 * * 4" --name controles-jeudi $COMMON \
  "Pour chaque carte [C3] ouverte : jours depuis lancement, dépense relevée dans les commentaires vs seuil d'arrêt écrit dans la croyance, contrôle dû (J+1 technique, J+3 ou J+7 négatifs). Demande à Hakim les chiffres manquants. Ne tire aucune conclusion winner/loser avant le seuil."

# Vendredi 9h — C4 relevé : mesures puis grille
hermes -p oh-ventures cron create "0 9 * * 5" --name releve-vendredi $COMMON \
  "Lance instrumentation/mesure-hebdo.py pour chaque boutique du parc, puis pour chaque carte [C3] au seuil crée une carte [C4] Verdict assignée à oh-marge avec la grille de plans/2026-09-04-audit-q4-testing-os.md §4.3. Mets à jour le Mac Fund sur la marge nette réelle uniquement. Rien n'est promu en règle validée sans Hakim."
```

Vérifier : `hermes -p oh-ventures cron list`, puis `hermes -p oh-ventures cron run veille-weekend`
pour un premier passage à la main.

---

## 6. Étape 5 — donner une identité au manager (`SOUL.md` de `oh-ventures`)

Écrit le 04/09 dans `~/.hermes/profiles/oh-ventures/SOUL.md` (ancien texte conservé dans
`SOUL.md.bak-2026-09-04`, config précédente dans `config.yaml.bak-2026-09-04`) :

```markdown
# Identité
Tu es **OH Ventures**, manager de la flotte produit de Hakim. Tu réponds en français. Hakim ne parle
qu'à toi ; tu ne fais exécuter les phases que par tes Bots (`@oh-scout` … `@oh-contradicteur`) ou par
des cartes kanban sur le board `oh-ventures-q4`. Tu n'exécutes aucune phase toi-même.

# Méthode
- La méthode vit dans `boutique-pipeline/` : `PRODUCT-RESEARCH-CRITERIA.md` (seuils, verdicts),
  `METHODE-ANALYSE-MARCHE.md`, et le skill `recherche-produit` (routage des phases).
- La semaine : `boutique-pipeline/plans/2026-09-04-audit-q4-testing-os.md`. Cinq couloirs
  C0 veille · C1 comité · C2 build · C3 test · C4 verdict ; une carte par produit et par couloir,
  tenant = slug produit, titre préfixé `[Cn]`.
- Tu contrôles chaque livrable (fichier au chemin annoncé, daté, sections obligatoires, interdits
  respectés) avant d'ouvrir la carte suivante. Livrable non conforme = arrêt, jamais de rattrapage
  silencieux. Tu tiens seul `registre-candidats.md`.
- Le contradicteur reçoit les preuves brutes, jamais ta synthèse.

# Ce que tu ne fais jamais
`GO_FINAL` / `WATCH_FINAL` / `NO_GO_FINAL`, prix, commande test, publication, dépense publicitaire,
Google Ads, Merchant Center, promotion d'une règle en validée : ce sont les décisions de Hakim. Tu
les lui présentes en cinq lignes, sur une carte bloquée `needs_input`. Aucun push sur `main` : tes
Bots déposent sur `agents/<mission>-<date>` et t'en donnent le nom.
```

Le skill `recherche-produit` porté dans le profil reste la source du routage : ne pas recopier son
tableau ici. Après toute modification d'un skill ou d'un agent dans `.claude/`, relancer
`python3 scripts/porter-skills-hermes.py --tous` depuis `boutiques-drop`, sinon les Bots
travaillent sur une version périmée.

---

## 7. Étape 6 — test de fumée avant la semaine 37

1. `hermes -p oh-scout chat -q "Quel modèle ?"` répond Grok ; `hermes -p oh-contradicteur chat -q …`
   répond GPT.
2. Créer la chaîne C0 du rasoir (§4) et suivre : `hermes kanban --board oh-ventures-q4 tail <id>`.
   La carte doit finir par `kanban_complete` avec un chemin de rapport **et** un nom de branche.
3. Vérifier sur GitHub que la branche `agents/…` existe et ne touche pas `main`.
4. `hermes kanban --board oh-ventures-q4 runs <id>` : durée, sortie, coût dans les logs ; comparer
   à la passe humaine du 04/09 (0,42 USD DataForSEO, quelques heures d'agent).
5. Envoyer à `@oh-ventures` sur Telegram : « qu'est-ce qui attend ma décision ? ». La réponse doit
   citer la carte bloquée, pas résumer le dossier entier.

Tant que ce test n'est pas passé, la semaine 37 se pilote comme aujourd'hui : Claude Code + Bots
en conversation. Le kanban n'entre en service que sur une chaîne qui a tourné de bout en bout.

---

## 7 bis. Résultat du test de fumée (nuit du 04 au 05/09)

Chaîne C0 du rasoir de sûreté lancée par Hakim à 23h37 (`unblock`), terminée à 00h04 sans aucune
intervention entre les cartes.

| Carte | Profil | Modèle | Durée | Sortie |
|---|---|---|---:|---|
| Phase 4A sourcing exact | `oh-sourcing` | grok-4.6 | 9 min | `sourcing-exact.md`, `FOURNISSEUR À TESTER`, SKU 29,79 € livré FR 5–10 j, six PDP AliExpress lues en navigateur réel, confiance A |
| Phase 5 économie | `oh-marge` | grok-4.6 | 8 min | `economie.md` + calculs reproductibles, `TECHNICAL_WATCH`, marge contributive et BE-CVR à 69 € et 99 € |
| Audit contradicteur | `oh-contradicteur` | gpt-6-astra | 7 min | `contradiction.md`, NON RETENU en l'état (cas limite marché non levé), preuves recalculées, SHA vérifiés |

Les cinq points de l'étape 6 passent : modèles corrects, `kanban_complete` avec chemin et branche à
chaque carte, branches `agents/rasoir-*` sur GitHub sans toucher `main`, durées et sorties dans
`hermes kanban runs`, aucun GO prononcé nulle part. Coût DataForSEO : 0 USD (aucun nouvel appel,
les workers ont réutilisé les réponses du 03/09). Coût modèles : non exposé par Hermes, à
instrumenter (`hermes insights`).

**Trois leçons à appliquer avant la semaine 37.**

1. **Espace de travail `dir:` = le worker fait son checkout dans ton dépôt.** Le repo
   `boutique-pipeline` s'est retrouvé sur `agents/rasoir-contradiction-2026-09-04` jusqu'à ce que
   Claude Code le remette sur `main`. Les trois branches se sont empilées proprement (contradiction
   contient économie contient sourcing), mais toute autre session ouverte sur le dépôt aurait vu
   la mauvaise branche. Pour les prochaines cartes : `--workspace worktree --branch agents/<mission>-<date>`,
   ou `--project` après `hermes project` sur le dépôt. À tester sur une carte avant de généraliser.
2. **Le contradicteur a lu la synthèse de phase 5 avant les preuves**, et l'a dit lui-même : la
   carte dépendant de l'économie, le résumé de transmission était visible dès l'orientation. Pour
   un audit vraiment aveugle, la carte contradicteur doit dépendre du **sourcing**, pas de
   l'économie, et recevoir les chemins des rapports bruts seulement.
3. **Un rôle porté peut être périmé sans que personne le voie.** Le contradicteur a relevé que
   `critique-candidat.md` portait encore les seuils 10 000 / 30 000 (canoniques : 12 500 / 37 500
   depuis le 29/08). Corrigé le 05/09 et reporté ; le rôle renvoie désormais au fichier de critères
   au lieu de coder un chiffre.

Une fausse piste à ne pas refaire : `reports/` est dans le `.gitignore` de `boutique-pipeline`.
Les synthèses `phase4-*` et `phase5-*` que les workers y écrivent ne sont pas des oublis de commit,
ce sont des copies locales ; les livrables versionnés sont ceux d'`analyses/`.

Le dossier A6 lui-même reste `REVIEW_PREQUALIFICATION` : le `TECHNICAL_WATCH` économique n'écrase
pas le cas limite marché, et la décision est celle de Hakim.

## 8. Ce qui reste hors de Hermes, et ce qu'on décide plus tard

- **Google Ads et Merchant Center.** Aucun accès depuis Hermes. Les contrôles J+1/J+3/J+7 et le
  lancement restent des gestes de Hakim ; les chiffres entrent sur la carte en commentaire.
- **Le build (C2).** Le planning Notion l'attribue à Claude Code / Codex, et la flotte cloud du
  16/08 avait sorti design et GMC pour la même raison. Sous Hermes le worker lit les fichiers, donc
  l'objection tombe, mais Grok n'a jamais été mesuré sur du Liquid Shopify. Décision proposée :
  garder Claude Code / Codex sur C2 en semaine 37-38, avec la carte kanban comme objet de suivi ;
  créer ensuite un profil `oh-build` (skills `executant-boutique`, `webdesign-boutiques`,
  `gmc-acceptance`) et le tester sur **une** boutique avec `set-model` GPT, puis Grok, en comparant.
- **Écritures Shopify.** Le connecteur ne peut ni écrire les policies ni dépublier ; passer par
  l'admin. Un worker qui bute là-dessus doit `kanban_block(kind=capability)`, pas contourner.
- **Notion.** Le board kanban et `hermes dashboard` remplacent la vue « Par jour ». Notion reste
  une surface de lecture si Hakim y tient ; il n'est jamais la référence (règle du 30/08).
- **Mémoire à corriger.** `architecture-hermes-modele-par-role.md` dit qu'un modèle par rôle exige
  un processus par rôle. C'est vrai pour `delegate_task`, faux pour le kanban (`--model` par carte).

---

## 9. Décisions à prendre par Hakim avant l'étape 1

a. **Les sept workers passent Grok maintenant, ou seulement après le test de fumée sur GPT ?**
   Recommandation : Grok tout de suite sur C0 (les phases sont outillées, `kw_dfs.py` fait le
   travail), GPT conservé sur contradicteur et manager.
b. **Largeur du dispatcher** (`--max`) : 3 pour commencer, le temps de voir les 429 SuperGrok.
c. **Le comité du lundi se tient sur Telegram ou sur le Desktop ?** Le cron `pool-lundi` livre dans
   le Bot Chat ; Telegram le reçoit aussi si `home_channel` reste configuré.
d. **Notion : miroir ou abandon** pour ce tableau.
