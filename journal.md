# Journal de veille technologique & scientifique

Ce fichier sert de mémoire entre sessions : sujets déjà couverts, remarques, orientations.

---

## Sessions

| Date       | Thèmes couverts | Tags | Remarques |
|------------|-----------------|------|-----------|
| 2026-06-03 | Systèmes multi-agents (Fujitsu, Dr. MAS, MHGPO, PSMAS) · Avantage quantique MARL (arXiv:2605.14235) · Informatique quantique 2026 (atomes neutres, AlphaQubit) · ICML/ICLR 2026 highlights · Breakthrough Prize 2026 (muon g-2, thérapies géniques) · GitHub trending (Understand-Anything) | `#agents` `#MARL` `#quantum` `#conférences-ML` `#biologie` `#physique` `#github` | Première session — dépôt vierge. Axé sur l'état du terrain en juin 2026 : RL multi-agents LLM, ponts quantique-MARL, conférences de référence. |
| 2026-06-04 | Single-agent > multi-agent à budget égal (arXiv:2604.02460, Kiela/Stanford, Data Processing Inequality) · Prédictibilité des réseaux via verre de spin (PNAS, Parisi) · Complexité pleinement quantique (Yuen : state/unitary synthesis, stateQIP=statePSPACE) · ASKAP J1745−5051 (transitoire radio = binaire naine blanche, « Rosetta stone ») · GitHub (OpenClaw, builders visuels, Copilot AI Credits) | `#agents` `#systèmes-complexes` `#quantum` `#complexité` `#astrophysique` `#github` `#fondations` | Session « fondations / contrepoint » : remise en question du multi-agents, bornes fondamentales (réseaux, complexité quantique). Complète directement le 03/06. Fil rouge : où sont les limites + coût de calcul comme critère central. |
| 2026-06-05 | Courbe Yerkes-Dodson des agents LLM (arXiv:2603.07360, coopération en U inversé sous pression, sélection sexuelle élimine l'agression) · P≠NP via bornes Extended Frege (Pich & Santhanam, JACM, proof complexity) · Puce photonique valleytronique tout-en-un (Nature Photonics, Monash, generate/steer/read) · Mémoire d'agent comme infra (survey arXiv:2603.07670, MAGMA, Hippocampus, EverMemOS) · Thymus adulte prédicteur de longévité lu par IA (Nature, Mass General Brigham) | `#agents` `#systèmes-complexes` `#émergence` `#complexité` `#fondations` `#photonique` `#matériel` `#mémoire-agents` `#biologie` `#IA-appliquée` | Session « émergence & fondations ». Prolonge 03-04/06 : agents vus comme sociétés artificielles (émergence) ; pendant classique du Yuen quantique (Pich-Santhanam) ; réponse matérielle (photonique) et logicielle (mémoire) au fil « coût du calcul ». |
| 2026-06-06 | NVIDIA Cosmos 3 (world model ouvert pour IA physique, mixture-of-transformers raisonnement+génération, « think before it acts », 20T tokens, Cosmos Coalition) · COOPER (arXiv:2606.04359, réputation *émergente* end-to-end en MARL, ShanghaiTech/BIGAI/PKU) · Réfutation conjecture Aldous-Lyons (Bowen-Chapman-Vidick, arXiv:2408.00110 + 2501.00173, subgroup tests = jeux non-locaux + MIP\*=RE → réseaux non sofiques indécidables) · Record supraconductivité 151 K à pression ambiante (Paul Chu & Deng, PNAS, Hg-1223 + pressure quenching) | `#agents` `#world-models` `#IA-physique` `#émergence` `#systèmes-complexes` `#fondations` `#indécidabilité` `#complexité-quantique` `#supraconductivité` `#matériel` `#IA-pour-science` | Session « simuler le monde + frontière de l'indécidable ». Concrétise l'item NVIDIA Cosmos flagué le 04/06. Émergence : prolonge Yerkes-Dodson (canal = réputation). Limites : Aldous-Lyons = pendant probabiliste/réseaux de MIP\*=RE, complète Yuen (04/06) et Pich-Santhanam (05/06). Fil matériel/physique (photonique → world models → supra) confirmé. |

---

## Sujets à approfondir (suggestions)

- Architecture interne des agents Fujitsu Takane : publication académique à surveiller
- Résultats détaillés ICML 2026 (juillet 2026) : actes complets à paraître
- Suivi IBM Quantum roadmap : premier avantage quantique vérifié prévu fin 2026
- Systèmes complexes : travaux de Laurent Hébert-Dufresne (Erdős-Rényi Prize 2026, contagion sur réseaux)
- Causal Description Gap (ICML 2026 Spotlight) : théorie de l'information et hiérarchie de Pearl
- MIP* = RE (Yuen et al., 2020) et son lien avec la synthèse d'unitaires quantiques
- Indice de Prédictibilité (PNAS) appliqué aux réseaux de neurones artificiels — vérifier
- Sécurité des agents « couteau-suisse » type OpenClaw (exécution de code arbitraire)
- Débat single vs multi-agent : réponses/réfutations sur arXiv à surveiller
- Yerkes-Dodson des agents (arXiv:2603.07360) : objection « artefact du corpus humain » a-t-elle une réponse ? émergence réelle vs rejeu narratif
- Bornes Extended Frege elles-mêmes : progrès récents côté complexité de preuve ? (suite Pich-Santhanam, JACM 2026)
- Valleytronique / photonique intégrée : feuille de route vers l'intégration à grande échelle, autres groupes après Monash
- Benchmarks mémoire d'agents multi-sessions : comparer MAGMA / Hippocampus / EverMemOS
- NVIDIA Cosmos & world models open-source : à explorer (Physical AI, robotique/véhicules)
- Thymus (2 papiers Nature, MGB) : un essai d'intervention causale est-il envisagé ?
- Cosmos 3 : premiers retours d'usage en robotique réelle (sim-to-real) ? composition exacte du corpus 20T tokens et licence « ouverte » à vérifier
- World models comme « intermédiaire agent ↔ monde réel » : lire le papier-position et la littérature sim-to-real associée
- Aldous-Lyons / soficité : un contre-exemple **explicite** (constructif) de réseau non sofique est-il atteignable ? suites après la conférence Jérusalem (14-18 juin 2026)
- MIP\*=RE comme « moteur de transfert » : quels autres champs (théorie des groupes, algèbres d'opérateurs, probabilités) vont hériter d'indécidabilité ? (cf. arXiv:2409.08342)
- Record supra 151 K (Chu/Deng, PNAS) : réplications indépendantes ? stabilité de l'état métastable obtenu par pressure quenching ?
- COOPER (réputation émergente) : la métrique apprise est-elle interprétable ? généralise-t-elle hors des social dilemmas classiques ?
- Project Prometheus (Bezos) & vague « IA physique / embodied » : suivre la bascule industrielle (Gemini Robotics ER-1.6, Skild AI, etc.)
