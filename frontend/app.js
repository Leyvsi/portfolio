// IDs des catégories MySQL vérifiées pour le projet Portfolio.
const storyCategories = [
  { id: 1, label: 'Histoires résolues', type: 'resolved' },
  { id: 2, label: 'Cold Cases', type: 'coldcase' }
];
function getStoryCategory(story) {
  return storyCategories.find(category => category.id === story.category_id &&
    ['resolved', 'coldcase'].includes(category.type));
}

const defaultStoryImage = 'images/default-story.svg';
const demoStoryImages = Object.freeze({
  'demo-f32-20261024-v1-tableau-salle-bleue': 'images/tableau-salle-bleue.webp',
  'demo-f32-20261024-v1-medaille-pavillon-ferme': 'images/medaille-pavillon-ferme.webp',
  'demo-f32-20261024-v1-malle-quai-silencieux': 'images/malle-quai-silencieux.webp',
  'demo-f32-20261024-v1-carnet-tour-nord': 'images/carnet-tour-nord.webp'
});

function getStoryImageSources(story) {
  const sources = [];
  if (typeof story.image_url === 'string' && story.image_url.trim()) {
    const candidate = story.image_url.trim();
    try {
      const url = new URL(candidate, document.baseURI);
      if (['http:', 'https:'].includes(url.protocol)) sources.push(candidate);
    } catch {
      // Une URL inutilisable laisse la place au fichier local ou au placeholder.
    }
  }
  const localImage = demoStoryImages[story.slug];
  if (typeof localImage === 'string') sources.push(localImage);
  sources.push(defaultStoryImage);
  return [...new Set(sources)];
}

function createStoryImage(story, detail = false) {
  const frame = document.createElement('div');
  frame.className = 'story-media';
  const image = document.createElement('img');
  image.className = 'story-image';
  image.width = 1200;
  image.height = 675;
  image.loading = detail ? 'eager' : 'lazy';
  image.decoding = 'async';
  const sources = getStoryImageSources(story);
  let index = 0;
  let exhausted = false;
  function selectSource() {
    image.alt = sources[index] === defaultStoryImage ?
      'Image à venir pour le dossier : ' + story.title :
      'Illustration du dossier : ' + story.title;
    image.src = sources[index];
  }
  image.addEventListener('error', () => {
    if (exhausted) return;
    index += 1;
    if (index < sources.length) {
      selectSource();
      return;
    }
    exhausted = true;
    image.hidden = true;
    const message = document.createElement('p');
    message.className = 'story-image-unavailable';
    message.textContent = 'Image indisponible';
    frame.append(message);
  });
  frame.append(image);
  selectSource();
  return frame;
}

function makeCard(story) {
  const card = document.createElement('article');
  card.className = 'case-card';
  card.style.overflowWrap = 'anywhere';
  const badge = document.createElement('span');
  badge.className = 'tag';
  const category = getStoryCategory(story);
  badge.textContent = category ? category.label : 'Catégorie non configurée';
  const title = document.createElement('h3');
  title.textContent = story.title;
  const description = document.createElement('p');
  description.textContent = story.summary;
  const link = document.createElement('a');
  link.href = 'dossier.html?slug=' + encodeURIComponent(story.slug);
  link.textContent = 'Lire le dossier →';
  card.append(createStoryImage(story), badge, title, description, link);
  return card;
}

const storyList = document.querySelector('[data-story-type]');
const storyFeedback = document.getElementById('stories-feedback');
const search = document.getElementById('recherche');
let pageStories = [];
function showCards(items) {
  storyList.replaceChildren(...items.map(makeCard));
}
if (search) search.addEventListener('input', () => {
  const q = search.value.toLocaleLowerCase('fr').trim();
  const found = pageStories.filter(story =>
    (story.title + ' ' + story.summary).toLocaleLowerCase('fr').includes(q));
  showCards(found);
  document.getElementById('aucun-resultat').hidden =
    found.length > 0 || pageStories.length === 0;
});

async function loadStories() {
  storyFeedback.textContent = 'Chargement des histoires…';
  storyList.setAttribute('aria-busy', 'true');
  if (search) search.disabled = true;
  try {
    const stories = await getStories();
    const type = storyList.dataset.storyType;
    pageStories = type === 'all' ? stories.slice(0, 3) :
      stories.filter(story => getStoryCategory(story)?.type === type);
    showCards(pageStories);
    if (!stories.length) {
      storyFeedback.textContent = 'Aucune histoire n’est disponible pour le moment.';
    } else if (stories.some(story => !getStoryCategory(story))) {
      storyFeedback.textContent = 'Certaines catégories ne sont pas configurées. Les histoires concernées ne sont pas classées dans les rubriques.';
    } else if (!pageStories.length) {
      storyFeedback.textContent = type === 'coldcase' ?
        'Aucun Cold Case n’est disponible pour le moment.' :
        'Aucune histoire résolue n’est disponible pour le moment.';
    } else {
      storyFeedback.textContent = '';
    }
  } catch (error) {
    storyFeedback.textContent = error.message;
  } finally {
    storyList.setAttribute('aria-busy', 'false');
    if (search) search.disabled = pageStories.length === 0;
  }
}
if (storyList) loadStories();

const detailTitle = document.getElementById('detail-titre');
async function loadStory() {
  const feedback = document.getElementById('detail-feedback');
  detailTitle.parentElement.style.overflowWrap = 'anywhere';
  const slug = new URLSearchParams(location.search).get('slug');
  if (!slug) {
    detailTitle.textContent = 'Dossier introuvable';
    feedback.textContent = 'Aucun slug de dossier n’a été fourni.';
    return;
  }
  detailTitle.textContent = 'Chargement du dossier…';
  try {
    const story = await getStoryBySlug(slug);
    const category = getStoryCategory(story);
    detailTitle.textContent = story.title;
    document.getElementById('detail-categorie').textContent =
      category ? category.label : 'Catégorie non configurée';
    document.getElementById('detail-resume').textContent = story.summary;
    const imageContainer = document.getElementById('detail-image');
    if (imageContainer) {
      imageContainer.replaceChildren(createStoryImage(story, true));
      imageContainer.hidden = false;
    }
    const content = document.getElementById('detail-contenu');
    story.content.split(/\r?\n/).forEach(line => {
      const paragraph = document.createElement('p');
      paragraph.textContent = line;
      content.append(paragraph);
    });
    if (category) {
      document.getElementById('retour-dossier').href =
        category.type === 'coldcase' ? 'coldcases.html' : 'histoires.html';
      feedback.textContent = '';
    } else {
      feedback.textContent = 'La catégorie de ce dossier n’est pas configurée.';
    }
  } catch (error) {
    detailTitle.textContent = error.status === 404 ?
      'Dossier introuvable' : 'Lecture impossible';
    feedback.textContent = error.status === 404 ?
      'Ce dossier n’existe pas.' : error.message;
  }
}
if (detailTitle) loadStory();

// La page Théories conserve sa démonstration locale, hors du périmètre F3.
const select = document.getElementById('sujet');
if (select) histoiresOriginales.forEach(item => {
  const opt = document.createElement('option');
  opt.value = item.id;
  opt.textContent = item.title;
  select.append(opt);
});

document.querySelectorAll('.demo-form:not(#login-form):not(#signup-form)').forEach(form => form.addEventListener('submit', event => {
  event.preventDefault();
  form.querySelector('.feedback').textContent = 'Ceci est une démonstration : aucune information n’a été envoyée ou enregistrée.';
}));

const signupForm = document.getElementById('signup-form');
if (signupForm) {
  signupForm.addEventListener('submit', async event => {
    event.preventDefault();
    const feedback = signupForm.querySelector('.feedback');
    const button = signupForm.querySelector('button');
    if (button.disabled) return;
    button.disabled = true;
    feedback.textContent = '';
    const username = signupForm.elements.username.value;
    const email = signupForm.elements.email.value;
    const password = signupForm.elements.password.value;
    let created = false;
    try {
      // Attendre la session et son CSRF avant toute inscription.
      try {
        await getCurrentUser();
      } catch (error) {
        if (error.status !== 401) throw error;
      }
      await register(username, email, password);
      created = true;
      signupForm.reset();
      feedback.textContent = 'Votre compte a été créé avec succès. Vous pouvez maintenant vous connecter.';
    } catch (error) {
      feedback.textContent = error.message;
    } finally {
      signupForm.elements.password.value = '';
      button.disabled = created;
    }
  });
}

const loginForm = document.getElementById('login-form');
if (loginForm) {
  loginForm.addEventListener('submit', async event => {
    event.preventDefault();
    const feedback = loginForm.querySelector('.feedback');
    const button = loginForm.querySelector('button');
    const adminLogin = loginForm.dataset.admin === 'true';
    feedback.textContent = '';
    button.disabled = true;
    try {
      const data = await login(
        loginForm.elements.username.value,
        loginForm.elements.password.value
      );
      if (adminLogin && data.user.is_admin !== true) {
        feedback.textContent = 'Accès administrateur requis';
        return;
      }
      location.href = adminLogin ? 'admin-dashboard.html' : 'index.html';
    } catch (error) {
      feedback.textContent = error.message;
    } finally {
      loginForm.elements.password.value = '';
      button.disabled = false;
    }
  });
}

const sessionControls = document.getElementById('session-controls');
if (sessionControls) {
  const loginLink = sessionControls.querySelector('a');
  const feedback = document.getElementById('session-feedback');
  getCurrentUser().then(data => {
    const username = document.createElement('span');
    username.textContent = data.user.username + ' ';
    const button = document.createElement('button');
    button.type = 'button';
    button.className = 'btn';
    button.textContent = 'Déconnexion';
    sessionControls.replaceChildren(username, button);
    button.addEventListener('click', async () => {
      feedback.textContent = '';
      button.disabled = true;
      try {
        await logout();
        sessionControls.replaceChildren(loginLink);
      } catch (error) {
        feedback.textContent = error.message;
        button.disabled = false;
      }
    });
  }).catch(error => {
    // Sans session, le lien Connexion est déjà affiché.
    if (error.status !== 401) feedback.textContent = error.message;
  });
}
