// Le frontend et l'API doivent être accessibles sur la même origine.
const API_BASE = '/api/v1';
const API_TIMEOUT_MS = 10000;
let csrfToken = null;

async function apiRequest(path, options = {}, expectedStatus = null) {
  const { timeoutMs = API_TIMEOUT_MS, signal, ...requestOptions } = options;
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

async function getCurrentUser() {
  const data = await apiRequest('/me');
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

function isStory(story) {
  return story && Number.isInteger(story.id) &&
    Number.isInteger(story.category_id) &&
    ['slug', 'title', 'summary', 'content'].every(field =>
      typeof story[field] === 'string') && story.slug.length > 0;
}

async function getStories() {
  const stories = await apiRequest('/stories', {}, 200);
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
