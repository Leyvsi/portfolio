// IDs des catégories MySQL vérifiées pour le projet Portfolio.
// L'association aux catégories 1 et 2 est une hypothèse actuelle de l'interface ;
// une autre base doit préparer ces identifiants ou ce classement sera incomplet.
const storyCategories = [
  { id: 1, label: 'Histoires résolues', type: 'resolved' },
  { id: 2, label: 'Cold Cases', type: 'coldcase' }
];
function getStoryCategory(story) {
  return storyCategories.find(category => category.id === story.category_id &&
    ['resolved', 'coldcase'].includes(category.type));
}

const defaultStoryImage = 'images/default-story.svg';

// Essayer l'URL HTTP(S), puis le SVG local permet
// de garder une carte lisible quand une image manque, sans accepter de schéma actif.
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
  sources.push(defaultStoryImage);
  return [...new Set(sources)];
}

// Avancer d'une source à la suivante sur l'événement error, puis masquer l'image
// si toutes échouent. La borne finale empêche une boucle sur le SVG indisponible.
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
  // Le texte alternatif précise si l'image affichée est le visuel de remplacement.
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

// Construire les éléments du DOM et utiliser textContent affiche les valeurs API
// comme du texte, au lieu de les interpréter comme du HTML provenant d’un membre.
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
// La recherche filtre en mémoire les dossiers déjà chargés, sans requête SQL
// ni appel API à chaque frappe ; elle porte sur le titre et le résumé.
if (search) search.addEventListener('input', () => {
  const q = search.value.toLocaleLowerCase('fr').trim();
  const found = pageStories.filter(story =>
    (story.title + ' ' + story.summary).toLocaleLowerCase('fr').includes(q));
  showCards(found);
  document.getElementById('aucun-resultat').hidden =
    found.length > 0 || pageStories.length === 0;
});

// Charger l'API puis filtrer selon la page ; l'accueil garde au plus trois dossiers.
// En cas d'erreur, un message remplace l'attente : donnees.js n'est pas un repli.
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
// Le slug de l'URL est transmis à l'API ; un 404 affiche un dossier introuvable.
// Les paragraphes du récit sont créés comme texte dans le DOM.
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
    // La même page accueille histoires et Cold Cases ; transmettre l'id de l'API.
    if (typeof mountStoryComments === 'function') mountStoryComments(story.id);
    if (typeof mountStoryLike === 'function') mountStoryLike(story);
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

  // Les options utilisent les vrais id de l'API, et non le rang dans une liste.
  // Bloquer l'envoi tant qu'ils ne sont pas disponibles évite une mauvaise référence.
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

  // Intercepter submit pour valider, bloquer le double envoi puis vérifier /me.
  // Un 201 efface la saisie ; un refus la conserve pour permettre une correction.
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

  // Même protection contre les doubles soumissions et même vérification de session.
  // La catégorie est ajoutée au contenu : elle n'est pas envoyée comme category_id.
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
  // Une inscription peut aussi partir avec une session existante : obtenir son
  // CSRF avant le POST ; un 401 de /me indique simplement une inscription anonyme.
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
  // Les deux écrans utilisent la même connexion API. L’entrée admin vérifie le
  // rôle avant de rediriger, mais seule l'autorisation Flask protège les données.
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

// La même zone est présente sur toutes les pages. /me décide de l'identité ;
// ni le nom affiché ni le lien Administration ne donnent un droit côté serveur.
const sessionControls = document.getElementById('session-controls');
if (sessionControls) {
  const loginLink = sessionControls.querySelector('a');
  const feedback = document.getElementById('session-feedback');
  let currentUser = null;
  let version = 0;
  let reading = null;
  let writing = false;
  let returnedFromCache = false;

  function sessionData(data) {
    if (data?.status !== 'success' || !isContributionId(data.user?.id) || typeof data.user.username !== 'string' ||
        !data.user.username || typeof data.user.is_admin !== 'boolean' ||
        typeof data.csrf_token !== 'string' || !data.csrf_token) {
      throw new Error('État de connexion incohérent.');
    }
    return data.user;
  }

  function endDisplayedSession() {
    if (typeof window.dispatchEvent === 'function' && typeof Event === 'function') {
      window.dispatchEvent(new Event('session-ended'));
    }
  }

  function anonymous(message = '') {
    if (currentUser) endDisplayedSession();
    currentUser = null;
    loginLink.hidden = false;
    sessionControls.replaceChildren(loginLink);
    feedback.textContent = message;
  }

  function unknown() {
    if (currentUser) endDisplayedSession();
    currentUser = null;
    const retry = document.createElement('button');
    retry.type = 'button'; retry.className = 'outline'; retry.textContent = 'Vérifier la connexion';
    retry.addEventListener('click', refreshSession);
    sessionControls.replaceChildren(retry);
    feedback.textContent = 'État de connexion indisponible. Vérifiez avant de continuer.';
  }

  function connected(data) {
    const user = sessionData(data);
    if (currentUser && (currentUser.id !== user.id || currentUser.is_admin !== user.is_admin)) endDisplayedSession();
    currentUser = user;
    const username = document.createElement('span');
    username.textContent = user.username + (user.is_admin ? ' — Administrateur' : ' — Membre');
    const button = document.createElement('button');
    button.type = 'button'; button.className = 'btn'; button.textContent = 'Déconnexion';
    sessionControls.replaceChildren(username, button);
    if (user.is_admin) {
      const admin = document.createElement('a');
      admin.href = 'admin-dashboard.html'; admin.className = 'outline'; admin.textContent = 'Administration';
      sessionControls.append(admin);
    }
    button.addEventListener('click', () => disconnect(button, user.id));
  }

  async function refreshSession() {
    if (writing) return;
    const current = ++version;
    reading?.abort(); reading = new AbortController();
    sessionControls.setAttribute('aria-busy', 'true');
    try {
      const data = await getCurrentUser({ signal: reading.signal });
      if (current !== version) return;
      connected(data); feedback.textContent = '';
    } catch (error) {
      if (current !== version) return;
      if ([401, 403].includes(error.status)) anonymous(error.status === 403 ? 'Compte indisponible. Reconnectez-vous.' : '');
      else unknown();
    } finally {
      if (current === version) sessionControls.setAttribute('aria-busy', 'false');
    }
  }

  async function disconnect(button, displayedId) {
    if (writing || button.disabled) return;
    writing = true; button.disabled = true;
    const current = ++version;
    reading?.abort(); reading = new AbortController();
    let sent = false;
    sessionControls.setAttribute('aria-busy', 'true');
    feedback.textContent = 'Vérification de la session…';
    try {
      const data = await getCurrentUser({ signal: reading.signal });
      if (current !== version) return;
      const user = sessionData(data);
      if (user.id !== displayedId) {
        connected(data); feedback.textContent = 'Compte modifié : état relu, aucune déconnexion envoyée.';
        return;
      }
      sent = true;
      await logout();
      if (current !== version) return;
      anonymous('Vous êtes déconnecté.');
    } catch (error) {
      if (current !== version) return;
      if (!sent && [401, 403].includes(error.status)) anonymous('Votre session est absente ou expirée.');
      else {
        // Une réponse perdue ne prouve pas la déconnexion. Relire sans renvoyer
        // le POST et ne jamais annoncer un succès avec un ancien état local.
        try {
          const data = await getCurrentUser({ signal: reading.signal });
          if (current !== version) return;
          connected(data);
          feedback.textContent = 'Déconnexion non confirmée. Votre session est encore active.';
        } catch (readError) {
          if (current !== version) return;
          if ([401, 403].includes(readError.status)) anonymous('Session absente après vérification.');
          else unknown();
        }
      }
    } finally {
      writing = false;
      if (current === version) {
        button.disabled = false;
        sessionControls.setAttribute('aria-busy', 'false');
      } else if (returnedFromCache) {
        returnedFromCache = false;
        endDisplayedSession();
        refreshSession();
      }
    }
  }

  window.addEventListener('pagehide', () => {
    version += 1; reading?.abort(); currentUser = null; returnedFromCache = false;
    sessionControls.replaceChildren(); feedback.textContent = '';
  });
  window.addEventListener('pageshow', event => {
    if (!event.persisted) return;
    if (writing) {
      returnedFromCache = true;
      feedback.textContent = 'Déconnexion en cours : vérification de la session à sa fin.';
    } else refreshSession();
  });
  window.addEventListener('focus', refreshSession);
  refreshSession();
}
