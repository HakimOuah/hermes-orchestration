# Test des STOP Kraken — premier passage de la chaîne Hermes

**31/08/2026.** Premier test de bout en bout : orchestrateur `gpt-5.6-sol`, workers `grok-4.6`
via `delegation.model`, profil Hermes `oh-ventures`, skills et rôles du parc portés depuis
`.claude/`.

## Ce que le test mesure — et ce qu'il ne mesure pas

Le protocole initialement prévu était faux. Les 8 STOP du 08/08/2026 ne viennent pas de la mesure
de demande : la note de Hakim dit explicitement que *« la mesure express disait GO sur quasi
toutes — seule la phase 2 profonde révèle les verrous »*. Tester le skill de mesure contre eux
aurait interrogé la mauvaise couche.

De plus, **4 des 8 ne sont pas des réponses sûres** : la correction de Hakim du même soir retire
lunch box, puzzle 3D, théière et chien, dont les verdicts s'appuyaient sur des chiffres Brand
Search jugés non fiables. Restent **mercerie** et **basse-cour**, fondés sur du verrouillage
structurel.

Le test porte donc sur ces deux-là, et sur la chaîne complète : mesure → SERP → cartographie
déléguée → verdict.

## Protocole

Chemins interdits en dur dans le prompt, et propagés au sous-agent :
`competitor-profiles/`, les analyses `*kraken*`, `memoire/plafond-niches-kraken-evidentes.md`.
Intégrité vérifiée **après coup** dans `state.db` : les seules occurrences de ces chemins sont le
texte d'interdiction lui-même et sa recopie dans le `context` de la délégation. Aucune lecture.

## Résultats

| | Mercerie | Basse-cour |
|---|---|---|
| Verdict attendu | STOP — verrouillage | STOP |
| Verdict rendu | **STOP** ✅ | **STOP** ✅ |
| Motif retenu | institutions physiques historiques | un opérateur multi-domaines tient la tête |
| Motif de Hakim | spécialistes historiques, champ pris | sandwich marketplaces / marques propriétaires |
| Recoupement des concurrents | 1 sur 5 | partiel |
| Délégation | `delegate_task` → `cartographie-concurrence` | idem |

**Convergence, pas reproduction.** Les deux verdicts tombent juste, par des chemins de preuve
largement différents de ceux de l'étude humaine. C'est plus solide qu'une copie — et ça interdit
de parler de reproduction.

## Ce que la chaîne a trouvé en plus

- **Mercerie** : contamination « château la mercerie », **8 100/mois**, absente de l'étude du 08/08.
  C'est du bruit pur dans les 221 680 retenus à l'époque.
- **Basse-cour** : `poulailler-direct.fr` appartient à **WEERIDE** — vérifié dans ses mentions
  légales. L'étude humaine le listait comme un spécialiste indépendant parmi d'autres.

## Ce qui ne se vérifie pas — et c'est le résultat le plus utile

Le motif central du STOP basse-cour est *« le même opérateur occupe les deux premières positions
organiques »*, avec trois domaines nommés. Vérification :

| Domaine | Lien Weeride |
|---|---|
| `poulailler-direct.fr` | ✅ confirmé (mentions légales) |
| `animalvalley.com` | ❔ répond, aucune trace |
| « Chemin des Poulaillers » | ❌ aucun domaine plausible ne résout |

**Un sur trois.** Le verdict est juste, la justification est partiellement inventée. C'est
exactement le mode d'échec annoncé dans l'audit du 30/08 — la fiction confiante, qui se présente
avec l'assurance d'un vrai constat.

Conséquence de conception, à appliquer avant d'élargir : **le contrat de sortie doit exiger une
preuve vérifiable par affirmation** (URL, citation, mention légale), pas une prose de synthèse. Un
motif sans preuve attachée doit être rejeté par le contrôle de schéma, pas relu par un humain.

## Coût

| | |
|---|---|
| Jetons, run basse-cour | 419 159 au total, dont 357 376 lus en cache |
| Coût modèle | **0 $** — `cost_status: included`, abonnements ChatGPT et SuperGrok |
| Coût données | DataForSEO seul, ~0,13 USD la page neuve ; 0 sur graine en cache |

Le coût marginal d'une mission est donc aujourd'hui **celui des données, pas celui de
l'intelligence**. Cela invalide une partie du raisonnement de `cost-strategy.md`, écrit en
supposant une facturation au jeton.

## Ce qui reste ouvert

- n = 2. Deux niches, un run chacune, sur les deux cas les plus solides.
- Les 4 STOP « en re-vérification » n'ont pas été testés — la chaîne pourrait justement trancher
  ce que Brand Search avait faussé.
- `mineur-brandsearch` n'a pas été exercé (clé TrendTrack posée le 31/08, jamais appelée).
- Le contradicteur tourne sur le même modèle que les workers : `delegation.model` est global.

---

# Addendum — 31/08, deuxième passage sur basse-cour

Expérience destinée à mesurer la charge du worker : `delegation.model` repointé sur
`gpt-5.6-sol` le temps d'un run, pour que la consommation du sous-agent tombe dans le même
compteur.

## Charge mesurée

| | Orchestrateur seul | Orch. + worker | Worker |
|---|---:|---:|---:|
| Entrée fraîche | 57 392 | 98 224 | **40 832** |
| Entrée relue en cache | 357 376 | 1 632 768 | **1 275 392** |
| Sortie | 4 391 | 10 112 | **5 721** |
| Appels API | 11 | 32 | **21** |
| Total | 419 159 | 1 741 104 | **1 321 945** |

Aux prix Kimi K3 (3 / 0,30 / 15 $ le million) : **worker 0,59 $**, orchestrateur 0,35 $. Une
mission avec orchestrateur sur abonnement et worker sur K3 revient donc à **≈ 0,59 $**.

Le worker consomme 3× l'orchestrateur, et l'essentiel est du cache relu — d'où l'importance du
tarif cache-hit dans tout arbitrage de fournisseur.

## Le résultat qui compte : le verdict s'est inversé

Même niche, même chaîne, **verdict opposé** : `STOP` au premier passage, **`GO` au second**.
Le second contredit aussi le verdict humain du 08/08.

Motif rendu au second passage : *« page 1 partagée entre spécialistes établis, grandes enseignes,
comparateur et contenu, sans domination d'un type unique »*. Exactement la même structure que
Hakim décrit comme un **sandwich sans interstice** — lue comme une ouverture au lieu d'un verrou.

**Confusion assumée dans le protocole :** deux choses ont changé entre les deux runs — le modèle
du worker, et le prompt (au second, j'ai nommé les graines et imposé la requête SERP au lieu de
laisser l'agent choisir). L'inversion n'est donc **pas attribuable au modèle**. C'est un défaut
de conception d'expérience, à ne pas reproduire.

## Diagnostic

Ce n'est pas une défaillance de modèle, c'est une **règle manquante**. Rien dans les skills portés
ne dit quand une page 1 mixte signifie « marché ouvert » et quand elle signifie « sandwich sans
interstice ». Ce critère vit dans le jugement de Hakim et n'est écrit nulle part qu'un agent
puisse lire.

Conséquence : **n = 2 ne valait rien.** Les deux STOP corrects du premier passage n'étaient pas
robustes — le troisième run sur l'un d'eux donne l'inverse. Aucun verdict ne doit être délégué
avant que ce critère soit écrit et que la stabilité soit re-mesurée sur plusieurs passages de la
même niche.

---

# Addendum 2 — la règle écrite supprime l'instabilité

Critère de verrou dicté par Hakim le 31/08, écrit dans `cartographie-concurrence`, porté vers
Hermes, puis re-testé **en ne changeant qu'une variable** : même prompt et même configuration que
le passage qui avait rendu `GO`.

| Passage | Worker | Règle écrite | Critère A | Prix plancher | Verdict |
|---|---|---|---|---|---|
| 1 | grok-4.6 | non | — | — | `STOP` |
| 2 | gpt-5.6-sol | non | — | — | `GO` |
| 3 | gpt-5.6-sol | **oui** | 2/9 — NON | 99,99 € | **`REVIEW`** |
| 4 | gpt-5.6-sol | **oui** | 2/9 — NON | 99,00 € | **`REVIEW`** |

Les passages 3 et 4 sont identiques en tout point. Mêmes acteurs, même comptage, même verdict, un
centime d'écart sur le plancher relevé.

## Ce que ça démontre

**L'instabilité ne venait pas du modèle, elle venait de la règle absente.** Tant que le critère
restait interprétatif, deux passages pouvaient lire la même page 1 comme une ouverture ou comme un
sandwich. Écrit sous forme de procédure déterminée — compter les acteurs grand public, comparer le
plancher au coût rendu — le verdict devient reproductible.

**Le `REVIEW` est plus juste que les deux verdicts précédents.** Le coût rendu du sourcing est
inconnu ; aucun verdict n'était donc possible. `STOP` comme `GO` prétendaient conclure sans la
donnée qui décide. La règle force l'agent à le dire au lieu de trancher.

## Ce qui reste manquant

La chaîne ne retrouve pas le `STOP` humain du 08/08, et la raison est identifiée : **la requête
décisive n'est pas la même.** L'étude humaine portait sur « porte automatique poulailler » —
l'angle accessoire, où Leroy Merlin aligne 238 offres. Les passages 3 et 4 portent sur « poulailler
4 poules », le poulailler lui-même, dont la page 1 est tenue par des spécialistes. Deux
sous-marchés réels, deux structures concurrentielles différentes, deux verdicts légitimes.

**Rien ne spécifie comment choisir la requête décisive**, et c'est elle qui commande le verdict.
C'est la prochaine règle à écrire, et elle est plus lourde que celle-ci : elle décide de ce qu'on
regarde, pas de comment on le lit.

---

# Addendum 3 — la règle d'expédiabilité fait converger le choix de requête

Après écriture de RULE-2026-003, l'agent choisit seul ses graines et sa requête décisive.

**Il bascule sur « porte automatique poulailler » — la requête décisive de l'étude humaine du
08/08.** Motif rendu : *« intention d'achat exacte correspondant à une fiche produit ; 8 100/mois,
bande 17,70–210 € ; produit compact expédiable en colis standard »*. Et il écarte explicitement
« poulailler 4 poules » pour *« hors gabarit et origine inconnue »*.

La règle a donc produit exactement l'effet attendu : elle a retiré au panier son pouvoir de décider
seul, et le choix de requête a convergé avec celui de Hakim sans que la réponse lui soit accessible.

## Le contrat a corrigé l'erreur de chiffre

Le champ `mot_cle_exact`, rendu obligatoire après le ×9 du passage précédent, a fonctionné :
l'agent donne cette fois la chaîne précise. Vérification par `verifier-volumes.py` :

| Mot-clé | Annoncé | Réel | |
|---|---:|---:|---|
| porte automatique poulailler | 8 100 | 8 100 | ✅ |
| mangeoire poule anti nuisible | 4 400 | 4 400 | ✅ |
| poulailler 4 poules | 8 100 | 8 100 | ✅ |
| mangeoire poule | 9 900 | 9 900 | ✅ |
| abreuvoir poule | 9 900 | 9 900 | ✅ |

**5 sur 5.** Le passage précédent annonçait 4 400 pour « mangeoire anti-nuisible poules », qui en
vaut 480 : deux chaînes différentes, deux volumes différents. Exiger la chaîne exacte a suffi.

## Ce qui diverge encore, et le prochain trou

Même requête que Hakim, **verdict différent** : `REVIEW` contre son `STOP`. Critère A compté
2 acteurs grand public sur 8, là où son relevé du 08/08 montrait Leroy Merlin (238 offres),
ManoMano et Cdiscount en haut de SERP. Trois semaines d'écart, ou un comptage différent — non
tranché.

**Trou probable sur le critère B.** Le prix plancher retenu est **17,70 €** pour une porte
automatique de poulailler, dans une bande annoncée 17,70–210 €. Un écart de ×12 entre plancher et
plafond signale que le plancher n'est pas comparable — c'est très probablement un accessoire ou une
pièce, pas le produit. Or le skill dit déjà d'écarter « marques officielles, marques à récit, bas de
gamme marketplace » et de se comparer au **concurrent comparable**.

Conséquence si on n'y touche pas : le critère B deviendrait presque toujours bloquant, puisque rien
de sourçable ne bat un plancher aberrant. **Le plancher doit être le plancher comparable, pas le
plancher absolu** — c'est la prochaine règle à écrire, et elle est de la même famille que les trois
précédentes : une distinction que Hakim fait sans effort et qui n'était écrite nulle part.
