# Guide simplifié pour débutants — Site "Les Petits Enquêteurs"

But: rendre le code simple à comprendre pour un examen.

Structure principale:
- `index.html`, `histoires.html`, `coldscases.html`, `updates.html`, `theories.html`, `top-dossiers.html`, `connexion.html`, `proposer-histoire.html` : pages HTML simples.
- `styles.css` : styles globaux.

Objectif: utiliser une navbar simple, lisible et facile à expliquer.

Snippet minimal — Navbar (HTML)

```html
<!-- Simple navbar: collez ce bloc dans le <body> où vous voulez la barre -->
<nav>
  <a href="index.html">Accueil</a>
  <a href="histoires.html">Histoires</a>
  <a href="coldscases.html">Cold Cases</a>
  <a href="updates.html">Updates</a>
  <a href="theories.html">Théories</a>
  <a href="top-dossiers.html">Top Dossiers</a>
</nav>
```

CSS simple pour la navbar

```css
/* Styles très simples à expliquer */
nav { background:#222; padding:8px; text-align:center; }
nav a { color:#fff; margin:0 8px; text-decoration:none; padding:6px 10px; display:inline-block; }
nav a:hover { background:#c0392b; color:#fff; }
```

JS minimal pour un bouton mobile (optionnel)

```html
<button id="menuBtn">Menu</button>
<script>
  const btn = document.getElementById('menuBtn');
  const nav = document.querySelector('nav');
  btn.addEventListener('click', () => {
    // bascule une classe simple; en CSS vous gérez l'affichage
    nav.classList.toggle('open');
  });
</script>
```

Conseils pédagogiques:
- Expliquez HTML: `nav` contient des liens (`a`).
- Expliquez CSS: sélecteurs simples, box model, couleur et hover.
- Expliquez JS: sélection d'éléments et écoute d'événements.

Souhaitez-vous que je remplace les navbar existantes par cette version simple sur toutes les pages ?
