// Frontend autonome : aucune requête fetch et aucun serveur nécessaire.
const allCases = histoiresOriginales;
function makeCard(item) {
  const card = document.createElement('article');
  card.className = 'case-card';
  const badge = document.createElement('span');
  badge.className = 'tag';
  badge.textContent = item.category;
  const title = document.createElement('h3');
  title.textContent = item.title;
  const description = document.createElement('p');
  description.textContent = item.summary;
  const link = document.createElement('a');
  link.href = 'dossier.html?id=' + encodeURIComponent(item.id);
  link.textContent = 'Lire le dossier →';
  card.append(badge, title, description, link);
  return card;
}
function showCards(id, items) {
  const el = document.getElementById(id);
  if (!el) return;
  el.replaceChildren(...items.map(makeCard));
}
showCards('accueil-cartes', allCases.slice(0, 3));
showCards('histoires-cartes', allCases.filter(c => c.category === 'Résolue'));
showCards('coldcases-cartes', allCases.filter(c => c.category === 'Cold case'));
const search = document.getElementById('recherche');
if (search) search.addEventListener('input', () => {
  const q = search.value.toLocaleLowerCase('fr').trim();
  const found = allCases.filter(c => c.category === 'Résolue' && (c.title + ' ' + c.summary).toLocaleLowerCase('fr').includes(q));
  showCards('histoires-cartes', found);
  document.getElementById('aucun-resultat').hidden = found.length > 0;
});
const detailTitle = document.getElementById('detail-titre');
if (detailTitle) {
  const id = new URLSearchParams(location.search).get('id');
  const item = allCases.find(c => c.id === id);
  if (item) {
    detailTitle.textContent = item.title;
    document.getElementById('detail-categorie').textContent = item.category;
    document.getElementById('detail-resume').textContent = item.summary;
    document.getElementById('retour-dossier').href = item.category === 'Cold case' ? 'coldcases.html' : 'histoires.html';
  } else {
    detailTitle.textContent = 'Dossier introuvable';
    document.getElementById('detail-resume').textContent = 'Ce dossier n’existe pas dans la version de démonstration.';
  }
}
const select = document.getElementById('sujet');
if (select) allCases.forEach(item => {
  const opt = document.createElement('option');
  opt.value = item.id;
  opt.textContent = item.title;
  select.append(opt);
});
document.querySelectorAll('.demo-form').forEach(form => form.addEventListener('submit', event => {
  event.preventDefault();
  form.querySelector('.feedback').textContent = 'Ceci est une démonstration : aucune information n’a été envoyée ou enregistrée.';
}));
