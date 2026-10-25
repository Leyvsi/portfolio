// Le frontend et l'API doivent être accessibles sur la même origine.
const API_BASE = '/api/v1';
const API_TIMEOUT_MS = 10000;
let csrfToken = null;

async function apiRequest(path, options = {}, expectedStatus = null) {
  const { timeoutMs = API_TIMEOUT_MS, signal, onAccessDenied, ...requestOptions } = options;
  if (!Number.isFinite(timeoutMs) || timeoutMs <= 0 || timeoutMs > 2147483647) {
    throw new RangeError('Le délai de requête doit être positif et inférieur ou égal à 2147483647 ms.');
  }
  const method = requestOptions.method || 'GET';
  const headers = {};

  if (requestOptions.body !== undefined) {
    headers['Content-Type'] = 'application/json';
  }
  if (['POST', 'PUT', 'PATCH', 'DELETE'].includes(method) &&
      path !== '/login' && csrfToken) {
    headers['X-CSRF-Token'] = csrfToken;
  }

  const controller = new AbortController();
  const forwardAbort = () => controller.abort();
  if (signal?.aborted) forwardAbort();
  else signal?.addEventListener('abort', forwardAbort, { once: true });
  let timedOut = false;
  const timeoutId = setTimeout(() => {
    timedOut = true;
    controller.abort();
  }, timeoutMs);

  try {
    const response = await fetch(API_BASE + path, {
      ...requestOptions,
      headers,
      credentials: 'include',
      signal: controller.signal
    });

    if (path === '/me' && [401, 403].includes(response.status)) {
      csrfToken = null;
    }

    if ([401, 403].includes(response.status) && typeof onAccessDenied === 'function') {
      const error = new Error(response.status === 401 ?
        'Session absente ou expirée.' : 'Accès administrateur requis.');
      error.status = response.status;
      error.code = 'HTTP_ERROR';
      onAccessDenied(error);
      throw error;
    }
    let data;
    try {
      data = await response.json();
    } catch (error) {
      if (timedOut || controller.signal.aborted) throw error;
      if (response.ok) {
        if (error.name !== 'SyntaxError') throw error;
        const invalidJson = new Error('Réponse du serveur illisible. Réessayez.');
        invalidJson.code = 'INVALID_JSON';
        throw invalidJson;
      }
    }
    if (!response.ok) {
      const error = new Error(data?.message || data?.error ||
        'Le serveur a renvoyé une erreur (HTTP ' + response.status + '). Réessayez.');
      error.status = response.status;
      error.code = 'HTTP_ERROR';
      throw error;
    }
    if (expectedStatus !== null && response.status !== expectedStatus) {
      const error = new Error('Réponse inattendue du serveur. Réessayez.');
      error.status = response.status;
      error.code = 'UNEXPECTED_STATUS';
      throw error;
    }
    return data;
  } catch (error) {
    if (timedOut) {
      const timeoutError = new Error('Le serveur met trop de temps à répondre. Réessayez.');
      timeoutError.code = 'TIMEOUT';
      throw timeoutError;
    }
    if (['HTTP_ERROR', 'INVALID_JSON', 'UNEXPECTED_STATUS'].includes(error.code)) throw error;
    const networkError = new Error('Impossible de contacter le serveur. Réessayez.');
    networkError.code = 'NETWORK_ERROR';
    throw networkError;
  } finally {
    clearTimeout(timeoutId);
    signal?.removeEventListener('abort', forwardAbort);
  }
}

async function login(username, password) {
  const data = await apiRequest('/login', {
    method: 'POST',
    body: JSON.stringify({ username: username.trim(), password })
  });
  csrfToken = data.csrf_token;
  return data;
}

async function getCurrentUser({ signal, onAccessDenied } = {}) {
  const data = await apiRequest('/me', { signal, onAccessDenied }, 200);
  csrfToken = data.csrf_token;
  return data;
}

async function logout() {
  const data = await apiRequest('/logout', { method: 'POST' });
  csrfToken = null;
  return data;
}

async function register(username, email, password) {
  return apiRequest('/users', {
    method: 'POST',
    body: JSON.stringify({ username: username.trim(), email: email.trim(), password })
  }, 201);
}

async function createProposal(title, content) {
  return apiRequest('/proposals', {
    method: 'POST',
    body: JSON.stringify({ title, content })
  }, 201);
}

async function createTheory(storyId, title, content) {
  if (!Number.isInteger(storyId) || storyId < 1 || storyId > 2147483647) {
    throw new Error('Choisissez un dossier valide.');
  }
  return apiRequest('/stories/' + storyId + '/theories', {
    method: 'POST',
    body: JSON.stringify({ title, content })
  }, 201);
}

function isStory(story) {
  return story && Number.isInteger(story.id) &&
    Number.isInteger(story.category_id) &&
    ['slug', 'title', 'summary', 'content'].every(field =>
      typeof story[field] === 'string') && story.slug.length > 0;
}

async function getStories({ signal, onAccessDenied } = {}) {
  const stories = await apiRequest('/stories', { signal, onAccessDenied }, 200);
  if (!Array.isArray(stories) || !stories.every(isStory)) {
    throw new Error('Réponse des histoires invalide.');
  }
  return stories;
}

async function getStoryBySlug(slug) {
  const story = await apiRequest('/stories/slug/' + encodeURIComponent(slug), {}, 200);
  if (!isStory(story)) {
    throw new Error('Réponse du dossier invalide.');
  }
  return story;
}

async function getStoryTheories(storyId, { signal } = {}) {
  if (!Number.isInteger(storyId) || storyId < 1 || storyId > 2147483647) {
    throw new Error('Choisissez un dossier valide.');
  }
  const theories = await apiRequest('/stories/' + storyId + '/theories', { signal }, 200);
  if (!Array.isArray(theories) || !theories.every(theory =>
    theory && Number.isInteger(theory.id) && theory.id > 0 &&
    theory.id <= 2147483647 && theory.story_id === storyId &&
    typeof theory.title === 'string' && typeof theory.content === 'string' &&
    (theory.created_at === null || typeof theory.created_at === 'string')) ||
    new Set(theories.map(theory => theory.id)).size !== theories.length) {
    throw new Error('Réponse des théories invalide.');
  }
  return theories;
}

async function getAdminStats({ signal, onAccessDenied } = {}) {
  const stats = await apiRequest('/stats', { signal, onAccessDenied }, 200);
  if (!stats || !['users', 'comments', 'reports'].every(key =>
    Number.isSafeInteger(stats[key]) && stats[key] >= 0)) {
    throw new Error('Réponse des statistiques invalide.');
  }
  return stats;
}

function isAdminList(items, fields) {
  return Array.isArray(items) && items.every(item =>
    item && Number.isInteger(item.id) && item.id > 0 && item.id <= 2147483647 &&
    fields.every(field => typeof item[field] === 'string') &&
    (item.created_at === null || typeof item.created_at === 'string')) &&
    new Set(items.map(item => item.id)).size === items.length;
}

async function getAdminProposals({ signal, onAccessDenied } = {}) {
  const proposals = await apiRequest('/proposals', { signal, onAccessDenied }, 200);
  if (!isAdminList(proposals, ['title', 'content', 'status'])) {
    throw new Error('Réponse des propositions invalide.');
  }
  return proposals;
}

async function getAdminReports({ signal, onAccessDenied } = {}) {
  const reports = await apiRequest('/admin/reports', { signal, onAccessDenied }, 200);
  if (!isAdminList(reports, ['type', 'target_id', 'reason', 'status'])) {
    throw new Error('Réponse des signalements invalide.');
  }
  return reports;
}
