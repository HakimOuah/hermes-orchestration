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
