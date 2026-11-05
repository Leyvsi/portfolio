# Validation de la candidate corrigée — lot 6H.22.4

> Résultats historiques du lot 6H.22.4. La revue 6H.22.5 a montré que le
> constructeur SQLite direct échappait au garde et que quatre documents locaux
> restaient dans la sélection publique. La [correction 6H.22.6](VALIDATION_LOT6H22_6.md)
> traite ces deux limites ; les compteurs historiques ci-dessous restent inchangés.

4 novembre 2026. Résultats de cette session dans une copie isolée ; aucune
publication, aucune application au dépôt original, aucune utilisation de la
SQLite persistante ou du serveur 5066.

| Campagne | Résultat réellement obtenu |
|---|---|
| Backend complet | 318 tests, aucun échec ou ignoré ; 32 connexions SQLite mémoire |
| Frontend complet | 591 tests, aucun échec ou ignoré ; inclut le contrôle des quatre WebP conservés |
| Persistance jetable | 21 tests ; bases synthétiques temporaires |
| RGPD public | 13 tests ; aucun texte juridique interne nécessaire |
| Chaîne Alembic | 6 tests ; sept révisions sur base vide puis peuplée, intégrité et rollback |
| Gardes du harnais | 30 sondes dans un test d’orchestration ; chemins, mutations, SQLite et réseau |
| Catalogue Python | 13 tests |
| Kit scolaire | 13 tests et parcours WSGI séparé |
| Lanceur | 10 tests |

Les sous-campagnes ne s’additionnent pas aux suites complètes. Les résultats
historiques restent datés dans leurs bilans. Le frontend comptait 590 tests dans
le lot précédent ; le contrôle de présence des quatre WebP porte le total à 591.

Commandes à lancer depuis la racine de la copie avec un environnement installé
selon le README ; elles n’ont besoin d’aucune donnée privée :

```powershell
python -I -B tools/valider_backend_isole.py --candidate-root .
node --test frontend/tests/*.test.cjs
python -I -B tests/test_demo_persistante.py
python -B -m unittest discover -s tests -p test_rgpd_information.py -v
python -I -B tests/test_migrations_sqlite_chain.py
python -I -B tests/test_backend_isolation_guards.py
```

Les journaux et reçus exacts, avec interpréteur, répertoire de travail et durées,
restent dans le dossier local de revue du lot. L’environnement virtuel installé
hors ligne au lot 6H.22.3 a été réutilisé ; aucune installation neuve n’est annoncée
dans ce lot. Les fichiers de dépendances n’ont pas changé.

Les six PNG et le SVG sont conservés octet pour octet. Les quatre WebP historiques
restent nécessaires aux anciens slugs et à leurs tests : ils sont conservés depuis
les blobs vérifiés de main. Leur présence ne vaut pas autorisation juridique de
diffusion. Le catalogue et les six correspondances PNG ne changent pas.

Les documents explicitement internes sont écartés de la candidate proposée ; les
index anciens sont marqués comme archives et les liens vers ces pièces ne
prétendent plus être publics. Les quatre fiches et leurs 76 questions sont
préservées. Le [complément des migrations](ERRATA_MIGRATIONS_LOT6H22_4.md) précise
les changements par rapport aux repères figés de 6H.21.1.

Le garde du harnais vérifie les API Python auditées et les connexions SQLite
ordinaires, y compris ATTACH, DETACH et VACUUM INTO. Il ne remplace pas une
sandbox système contre du code hostile ou des appels natifs non audités.

**NO-GO pour publication immédiate** : les lots pédagogiques suivants, la revue
des correctifs et du classement, la revalidation du main distant et l’autorisation
finale restent nécessaires. Aucun résultat MySQL, Edge nouveau, déploiement,
audit juridique ou conformité générale n’est déduit des essais synthétiques.
