# Accès de soutenance — procédure 6H.5

> Etat de diffusion scolaire du 3 novembre 2026 : suivre le [guide actuel](../../LIVRAISON_SCOLAIRE.md) et la [validation scolaire](VALIDATION_SCOLAIRE.md). Les sections de campagnes anterieures et leurs commandes sont historiques ; elles ne remplacent pas la procedure actuelle. Les chemins sous `C:\chemin\utilisateur` sont des exemples anonymises. Les archives internes signalees sont conservees localement.

2 novembre 2026. Procédure préparée, sans création de compte, lancement ou écriture en base. **C-02 — Fichier privé de comptes de démonstration : PARTIEL.** Le critère reste une fiche privée disponible, un détenteur désigné et des accès membre/administrateur correspondant au processus du jour J, avec vérification des deux connexions. Une description des permissions ne remplace pas cette preuve.

## Ce que le logiciel démontre déjà

| Mécanisme | Code et preuve existante | Limite |
|---|---|---|
| Attribution des droits | `User.is_admin` vaut faux par défaut ; `register_user()` ne reprend pas le rôle envoyé par le client. Le kit `seed()` attribue le rôle uniquement à son compte fictif admin. | Aucune interface de promotion/rétrogradation de rôle ; ne pas inventer une commande d'administration réelle |
| Authentification | `login_user()` vérifie le hachage du mot de passe et le bannissement, renouvelle la session et son CSRF. Tests historiques de login et recette HTTP 6H.2. | Aucun compte réel vérifié ici |
| Permissions | `get_authenticated_user()` relit le compte ; `admin_required()` vérifie son rôle actuel en base. `test_list_role_is_read_in_database_not_cookie`, `test_both_routes_require_current_admin_not_forged_role`. | Un menu visible ou un booléen client n'accorde aucun droit |
| CSRF | Filtre global sur POST/PUT/PATCH/DELETE portant une session authentifiée ; jeton de session comparé à `X-CSRF-Token`. Tests `test_missing_header_token_is_403`, `test_protected_post_with_correct_token_is_allowed`. | GET/HEAD/OPTIONS, login et absence de session sont exemptés de ce filtre ; les permissions de route restent distinctes |
| Bannissement | `ban_user_account()` ne change que `is_banned`, avec transaction ; `test_open_sessions_are_refused_and_new_login_is_blocked`. Le parcours HTTP 6H.2 atteste le refus de la session bannie. | Tous les administrateurs sont protégés du bannissement (409), y compris soi-même ; aucun débannissement dans l'interface |
| Session et sortie | Cookie signé, HttpOnly, SameSite=Lax ; Secure dépend de la configuration. `logout_user()` vide la session du navigateur ; tests CSRF/logout et contre-recette Edge. | Ni chiffrement du cookie ni registre central de révocation de toutes ses copies ; fermer un onglet ne prouve pas la révocation |

Ces tests sont des preuves de la campagne historique **854 PASS**, non relancée. Les 76 sources de son manifeste et les 40 sources du kit restent identiques. Références : 6H.4 (archive interne non livree), HTTP 6H.2 (archive interne non livree), `backend/tests/test_admin_users.py`, `test_csrf.py`, `test_proposals_ban.py`, `test_users_votes.py`, `backend/index.py`, `backend/api/v1/views/permissions.py`, `users.py`, `admin_users_support.py`.

## Organisation proposée, à confirmer

**L'utilisateur désigne Mahamadou en 6H.5 pour prendre en charge le lancement et les accès.** Le support privé, le renouvellement et les vérifications du lancement restent à confirmer ; un remplaçant peut être désigné si utile. Mahamadou conservera les accès dans un gestionnaire de mots de passe privé ou une fiche papier gardée hors caméra ; jamais dans le CSV du dépôt, Git, un chat, une capture ou un journal publié. Le choix du support appartient à l'équipe.

Seule la personne désignée manipule le compte administrateur pendant les actions prévues. Le compte membre sert aux contributions fictives. Le jury et les visiteurs n'ont pas besoin de recevoir un accès administrateur. Il s'agit d'une règle d'organisation proposée, pas d'une nouvelle restriction applicative.

1. Lors du prochain lancement **séparément autorisé**, utiliser le kit isolé 6G.4 vérifié et ses données synthétiques ; ne pas substituer le lanceur normal relié à une configuration réelle.
2. Hors projection, relever les accès générés pour ce processus. Le kit génère de nouveaux mots de passe et une nouvelle clé de session à chaque lancement ; une ancienne fiche ne convient pas après redémarrage.
3. Dans le navigateur de recette autorisé, vérifier successivement le membre et l'administrateur : connexion, rôle affiché et autorisation/refus de la page privée attendue. Ne pas bannir le compte indispensable à la démonstration pour ce simple contrôle.
4. Consigner uniquement : date, détenteur, référence non secrète du lancement, rôle vérifié, résultat, emplacement privé confirmé et renouvellement après redémarrage. Ne copier aucun identifiant, mot de passe, cookie ou jeton dans cette attestation.
5. À la fin, se déconnecter et arrêter le processus du kit selon le protocole existant. Sa base est en mémoire ; au prochain lancement, comptes et clé sont nouveaux. Ne pas confondre ce comportement du kit avec celui d'une base persistante.

## Révocation : distinguer les situations

- **Membre fictif** : un administrateur actif peut utiliser le bannissement existant, avec confirmation et CSRF, seulement dans le scénario autorisé. Le compte et ses contributions ne sont pas effacés ; les accès protégés et les nouvelles connexions sont refusés.
- **Administrateur du kit compromis** : le bannissement ne convient pas. Arrêter le processus du kit ; un redémarrage autorisé recrée la base mémoire, les accès et la clé. Refaire la fiche privée et les contrôles. Aucun redémarrage n'est effectué par ce document.
- **Administrateur d'une base persistante** : aucune procédure de retrait de rôle ou révocation globale n'est exécutée ou prétendue disponible dans le dashboard. Une intervention distincte, autorisée et préparée par le responsable technique serait nécessaire. Ne pas employer une suppression de compte ou une requête SQL improvisée.

## Attestation de clôture sans secret — à compléter

« Le [DATE], Mahamadou confirme disposer hors Git des accès fictifs membre et administrateur du lancement [RÉFÉRENCE NON SECRÈTE]. Le support privé est [TYPE DE SUPPORT, SANS CHEMIN SENSIBLE]. Les deux connexions ont été vérifiées dans la recette autorisée du [DATE] : [RÉSULTATS]. En cas de redémarrage, [PERSONNE] relève les nouveaux accès et renouvelle cette vérification. »

La réponse 6H.5 « Mahamadou » lève le manque de désignation. Elle ne confirme ni le support privé ni la disponibilité des accès ou leurs connexions pour le processus du jour J. Les autres champs ne sont pas remplis fictivement. **C-02 reste PARTIEL tant que la disponibilité réelle et les deux connexions du lancement retenu ne sont pas établies.**
