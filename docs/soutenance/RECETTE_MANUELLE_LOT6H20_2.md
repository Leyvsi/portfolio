# Recette manuelle préparée — lot 6H.20.2

4 novembre 2026 — protocole à exécuter après autorisation de la séance. Aucune case de ce document n’atteste un résultat déjà obtenu. Les résultats 6H.18.x restent historiques.

## Conditions

Utiliser une copie isolée des sources actuelles, une nouvelle SQLite mémoire ou temporaire, avec données fictives et comptes de test. Neutraliser dotenv/Aiven avant import et bloquer toute autre base. Ne pas utiliser la SQLite persistante, sa clé, ses comptes ou ses contributions. Ne pas arrêter ni redémarrer les serveurs existants. Si une écoute navigateur est autorisée, choisir un port local libre sans libérer un port occupé. Ne pas journaliser mots de passe, cookies, jetons, HAR ou réponses privées. Ne pas lancer de migration.

## Notices et accessibilité

- [ ] Visiteur : inscription, connexion membre, connexion administrateur, dossier, théories et proposition restent accessibles selon leurs règles actuelles ; la notice précède les champs ou l’action.
- [ ] Membre et administrateur : relire la même information, sans dépendance au rôle pour accéder aux notices.
- [ ] Vérifier publication sans connexion des commentaires/théories, destination administrative des propositions/signalements, lien au compte des likes et absence de promesse d’anonymat.
- [ ] Parcourir au clavier : ordre cohérent, focus visible, champs et boutons décrits ; les formulaires masqués restent masqués jusqu’à leur ouverture normale.
- [ ] Edge ordinateur, puis largeurs émulées 390 px et 320 px, zoom 200 % : lisibilité, retour à la ligne, aucune perte d’action ni débordement. Distinguer émulation et téléphone physique.
- [ ] Vérifier les six illustrations, légendes IA, six textes et replis sans modifier les fichiers ni le catalogue.

## Parcours sur base isolée uniquement

- [ ] Créer un membre fictif, se connecter, vérifier rôle membre et refus de l’administration ; connexion administrateur avec un compte temporaire habilité.
- [ ] Publier commentaire et théorie, enregistrer une proposition, signaler un commentaire, ajouter puis retirer un like de dossier et de commentaire.
- [ ] Vérifier confirmations, totaux et absence de double envoi ou répétition automatique après résultat incertain.
- [ ] Vérifier déconnexion et relecture des permissions ; conserver les garde-fous des comptes suspendus et des dossiers archivés.
- [ ] Avec le client WSGI isolé, vérifier les refus CSRF absent/invalide/autre session sans modification des dix tables ; un jeton valide doit produire l’effet attendu. Ne pas prétendre que login ou les requêtes anonymes passent le même filtre.

## Cookies, réseau et non-publication

- [ ] Inspecter uniquement noms et attributs : HttpOnly, SameSite=Lax, Secure conforme au mode HTTP local ; vérifier émission à la connexion et suppression à la déconnexion, sans exporter leur valeur.
- [ ] Vérifier qu’aucune acceptation générale RGPD ou bannière pour le seul cookie nécessaire ne bloque les parcours.
- [ ] Relever les origines et finalités des requêtes externes et éventuels autres stockages ; examiner séparément Swagger et les images distantes. Aucun diagnostic général d’absence de traceurs sans cette inspection.
- [ ] Lanceur général : GET/HEAD des deux brouillons internes et `/confidentialite.html` refusés (404). Kit scolaire : brouillons hors liste refusés (403).
- [ ] Aucune page publique ne contient de lien de confidentialité provisoire ou de champ juridique vide.

## Après validation et autorisation de publication uniquement

- [ ] Identité/contact, bases légales, conservation, destinataires, hébergement et décisions D01–D12 confirmés ; aucun champ indispensable manquant.
- [ ] Créer la page publique finale, vérifier HTTP 200 sans connexion et les liens depuis les dix pieds de page et les notices, pour les trois rôles.
- [ ] Vérifier ancres et liens, clavier, focus, zoom et mobile ; autoriser précisément la page dans le kit et adapter ses tests sans exposer les documents internes.

Consigner date, version des sources, contexte Edge, résultats et limites dans le bilan, sans données d’accès. Une vérification manuelle non exécutée reste à faire ; aucun total de tests automatiques ne la remplace.
