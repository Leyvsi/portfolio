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

document.querySelectorAll('.demo-form:not(#login-form):not(#signup-form):not(#proposal-form):not(#theory-form)').forEach(form => form.addEventListener('submit', event => {
  event.preventDefault();
  form.querySelector('.feedback').textContent = 'Ceci est une démonstration : aucune information n’a été envoyée ou enregistrée.';
}));

const theoryForm = document.getElementById('theory-form');
if (theoryForm) {
  const storySelect = theoryForm.elements.story_id;
  const titleField = theoryForm.elements.title;
  const contentField = theoryForm.elements.content;
  const feedback = theoryForm.querySelector('.feedback');
  const button = theoryForm.querySelector('button');
  const fields = [storySelect, titleField, contentField];
  let storyIds = new Set();
  let sending = false;

  async function loadTheoryStories() {
    storySelect.disabled = true;
    button.disabled = true;
    theoryForm.setAttribute('aria-busy', 'true');
    feedback.textContent = 'Chargement des dossiers...';
    try {
      const stories = await getStories();
      if (stories.some(story => !Number.isInteger(story.id) ||
          story.id < 1 || story.id > 2147483647) ||
          new Set(stories.map(story => story.id)).size !== stories.length) {
        throw new Error('La liste des dossiers contient des identifiants invalides.');
      }
      const placeholder = document.createElement('option');
      placeholder.value = '';
      placeholder.textContent = 'Choisir un dossier';
      const options = stories.map(story => {
        const option = document.createElement('option');
        option.value = String(story.id);
        option.textContent = story.title;
        return option;
      });
      storySelect.replaceChildren(placeholder, ...options);
      storyIds = new Set(stories.map(story => story.id));
      storySelect.disabled = storyIds.size === 0;
      button.disabled = storyIds.size === 0;
      feedback.textContent = storyIds.size ? '' : 'Aucun dossier n’est disponible pour le moment.';
    } catch (error) {
      feedback.textContent = 'Impossible de charger les dossiers. ' +
        (error.message || 'Réessayez.') + ' Rechargez la page.';
    } finally {
      theoryForm.setAttribute('aria-busy', 'false');
    }
  }

  theoryForm.addEventListener('submit', async event => {
    event.preventDefault();
    if (sending) return;
    if (storyIds.size === 0) {
      feedback.textContent = 'Les dossiers ne sont pas disponibles. Attendez la fin du chargement ou rechargez la page.';
      return;
    }
    sending = true;
    button.disabled = true;
    theoryForm.setAttribute('aria-busy', 'true');
    feedback.textContent = '';
    const disabledBefore = fields.map(field => field.disabled);

    try {
      const selected = storySelect.value;
      const storyId = Number(selected);
      const title = titleField.value.trim();
      const content = contentField.value.trim();
      if (!/^[1-9]\d*$/.test(selected) || !storyIds.has(storyId)) {
        throw new Error('Choisissez un dossier disponible dans la liste.');
      }
      if (!title || !content) {
        throw new Error('Renseignez un titre et une analyse non vides.');
      }
      if ([...title].length > 200) {
        throw new Error('Le titre ne doit pas dépasser 200 caractères.');
      }
      try {
        encodeURIComponent(title);
        encodeURIComponent(content);
      } catch {
        throw new Error('Le texte contient des caractères invalides.');
      }
      if (new TextEncoder().encode(content).length > 65535) {
        throw new Error('Votre analyse est trop longue. Raccourcissez-la avant l’envoi.');
      }

      fields.forEach(field => { field.disabled = true; });
      const current = await getCurrentUser();
      if (!current || typeof current.csrf_token !== 'string' ||
          !/^[\x21-\x7e]+$/.test(current.csrf_token)) {
        throw new Error('Impossible de vérifier votre session. Reconnectez-vous puis réessayez.');
      }
      await createTheory(storyId, title, content);
      theoryForm.reset();
      feedback.textContent = 'Votre théorie a été publiée.';
    } catch (error) {
      if (error.status === 401) {
        feedback.textContent = 'Votre session est absente ou a expiré. Connectez-vous pour proposer une théorie ; votre saisie est conservée.';
      } else if (error.status === 403) {
        feedback.textContent = 'Envoi refusé. ' + error.message + ' Rechargez la page ou reconnectez-vous.';
      } else if (error.status === 404) {
        feedback.textContent = 'Ce dossier n’est plus disponible. Votre saisie est conservée.';
      } else {
        feedback.textContent = error.message || 'Impossible d’envoyer votre théorie. Réessayez.';
      }
    } finally {
      fields.forEach((field, index) => { field.disabled = disabledBefore[index]; });
      button.disabled = false;
      theoryForm.setAttribute('aria-busy', 'false');
      sending = false;
    }
  });

  loadTheoryStories();
}

const proposalForm = document.getElementById('proposal-form');
if (proposalForm) {
  const feedback = proposalForm.querySelector('.feedback');
  const button = proposalForm.querySelector('button');
  const fields = [
    proposalForm.elements.title,
    proposalForm.elements.category,
    proposalForm.elements.content
  ];
  let sending = false;

  proposalForm.addEventListener('submit', async event => {
    event.preventDefault();
    if (sending) return;
    sending = true;
    button.disabled = true;
    proposalForm.setAttribute('aria-busy', 'true');
    feedback.textContent = '';
    const disabledBefore = fields.map(field => field.disabled);

    try {
      const title = proposalForm.elements.title.value.trim();
      const text = proposalForm.elements.content.value.trim();
      const category = proposalForm.elements.category.value;

      if (!title || !text) {
        throw new Error('Renseignez un titre et une présentation non vides.');
      }
      if ([...title].length > 200) {
        throw new Error('Le titre ne doit pas dépasser 200 caractères.');
      }
      if (!['Histoire', 'Cold case'].includes(category)) {
        throw new Error('Choisissez une catégorie proposée dans la liste.');
      }
      const content = 'Catégorie proposée : ' + category + '\n\n' + text;
      try {
        encodeURIComponent(title);
        encodeURIComponent(content);
      } catch {
        throw new Error('Le texte contient des caractères invalides.');
      }
      if (new TextEncoder().encode(content).length > 65535) {
        throw new Error('La présentation est trop longue. Raccourcissez-la avant l’envoi.');
      }

      fields.forEach(field => { field.disabled = true; });
      const current = await getCurrentUser();
      if (!current || typeof current.csrf_token !== 'string' ||
          !/^[\x21-\x7e]+$/.test(current.csrf_token)) {
        throw new Error('Impossible de vérifier votre session. Reconnectez-vous puis réessayez.');
      }
      await createProposal(title, content);
      proposalForm.reset();
      feedback.textContent = 'Votre proposition a été envoyée pour examen.';
    } catch (error) {
      if (error.status === 401) {
        feedback.textContent = 'Votre session est absente ou a expiré. Connectez-vous pour proposer une histoire ; votre saisie est conservée.';
      } else if (error.status === 403) {
        feedback.textContent = 'Envoi refusé. ' + error.message + ' Rechargez la page ou reconnectez-vous.';
      } else {
        feedback.textContent = error.message || 'Impossible d’envoyer votre proposition. Réessayez.';
      }
    } finally {
      fields.forEach((field, index) => { field.disabled = disabledBefore[index]; });
      button.disabled = false;
      proposalForm.setAttribute('aria-busy', 'false');
      sending = false;
    }
  });
}

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
