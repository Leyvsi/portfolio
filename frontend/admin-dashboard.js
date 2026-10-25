(() => {
  'use strict';

  const dashboard = document.getElementById('admin-dashboard');
  if (!dashboard) return;

  const dataRegion = document.getElementById('admin-data');
  const refresh = document.getElementById('admin-refresh');
  const feedback = document.getElementById('admin-feedback');
  const loginLink = document.getElementById('admin-login-link');
  const proposalsList = document.getElementById('admin-proposals-list');
  const reportsList = document.getElementById('admin-reports-list');
  const categoriesFeedback = document.getElementById('admin-categories-feedback');
  const proposalsFeedback = document.getElementById('admin-proposals-feedback');
  const reportsFeedback = document.getElementById('admin-reports-feedback');
  const counters = Object.fromEntries([
    'stories', 'resolved', 'coldcases', 'users', 'comments', 'reports'
  ].map(name => [name, document.getElementById('admin-' + name + '-count')]));
  const statuses = new Map([
    ['pending', 'En attente'], ['approved', 'Acceptée'], ['rejected', 'Refusée'],
    ['resolved', 'Traité'], ['dismissed', 'Classé']
  ]);
  let requestVersion = 0;
  let activeRequest = null;

  dataRegion.style.overflowWrap = 'anywhere';

  function clearData() {
    dataRegion.hidden = true;
    Object.values(counters).forEach(counter => { counter.textContent = '—'; });
    proposalsList.replaceChildren();
    reportsList.replaceChildren();
    categoriesFeedback.textContent = '';
    proposalsFeedback.textContent = '';
    reportsFeedback.textContent = '';
  }

  function cancelRequest() {
    requestVersion += 1;
    activeRequest?.abort();
    activeRequest = null;
    return requestVersion;
  }

  function blockAccess(error, version) {
    if (version !== requestVersion) return;
    cancelRequest();
    clearData();
    dashboard.setAttribute('aria-busy', 'false');
    refresh.disabled = false;
    loginLink.hidden = false;
    feedback.textContent = error.status === 401 ?
      'Votre session est absente ou a expiré. Connectez-vous avec un compte administrateur.' :
      'Accès refusé. Un compte administrateur autorisé est nécessaire.';
  }

  function publicationDate(value) {
    const time = document.createElement('time');
    if (typeof value === 'string' &&
        /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d{1,6})?(?:Z|[+-]\d{2}:\d{2})?$/i.test(value)) {
      // This API serializes UTC dates without their timezone suffix.
      const iso = /(?:Z|[+-]\d{2}:\d{2})$/i.test(value) ? value : value + 'Z';
      const date = new Date(iso);
      if (Number.isFinite(date.getTime())) {
        time.dateTime = date.toISOString();
        time.textContent = new Intl.DateTimeFormat('fr-FR', {
          dateStyle: 'medium', timeStyle: 'short', timeZone: 'Europe/Paris'
        }).format(date) + ' (heure de Paris)';
        return time;
      }
    }
    time.textContent = 'Date indisponible';
    return time;
  }

  function paragraph(text) {
    const node = document.createElement('p');
    node.textContent = text;
    return node;
  }

  function proposalCard(proposal) {
    const card = document.createElement('article');
    card.className = 'panel';
    const title = document.createElement('h3');
    title.textContent = proposal.title;
    card.append(title, paragraph('Statut : ' + (statuses.get(proposal.status) || proposal.status)),
      publicationDate(proposal.created_at));
    proposal.content.split(/\r?\n/).forEach(line => card.append(paragraph(line)));
    return card;
  }

  function reportCard(report) {
    const card = document.createElement('article');
    card.className = 'panel';
    const title = document.createElement('h3');
    title.textContent = report.type === 'comment' ? 'Signalement de commentaire' : 'Signalement : ' + report.type;
    card.append(title, paragraph('Cible : ' + report.target_id),
      paragraph('Statut : ' + (statuses.get(report.status) || report.status)),
      publicationDate(report.created_at));
    report.reason.split(/\r?\n/).forEach(line => card.append(paragraph(line)));
    return card;
  }

  function displayData(stats, stories, proposals, reports) {
    if (stories.some(story => story.id < 1 || story.id > 2147483647) ||
        new Set(stories.map(story => story.id)).size !== stories.length) {
      throw new Error('Identifiants de dossiers invalides.');
    }
    const resolved = stories.filter(story => getStoryCategory(story)?.type === 'resolved').length;
    const coldcases = stories.filter(story => getStoryCategory(story)?.type === 'coldcase').length;
    const others = stories.length - resolved - coldcases;
    const values = { stories: stories.length, resolved, coldcases,
      users: stats.users, comments: stats.comments, reports: stats.reports };
    Object.entries(values).forEach(([name, value]) => {
      counters[name].textContent = String(value);
    });
    categoriesFeedback.textContent = !stories.length ? 'Aucun dossier disponible.' :
      others ? others + ' dossier(s) dans une catégorie non configurée.' : '';
    proposalsList.replaceChildren(...proposals.map(proposalCard));
    reportsList.replaceChildren(...reports.map(reportCard));
    proposalsFeedback.textContent = proposals.length ? '' : 'Aucune proposition reçue.';
    reportsFeedback.textContent = reports.length ? '' : 'Aucun signalement.';
    dataRegion.hidden = false;
  }

  async function loadDashboard() {
    const version = cancelRequest();
    const controller = new AbortController();
    activeRequest = controller;
    clearData();
    loginLink.hidden = true;
    refresh.disabled = true;
    dashboard.setAttribute('aria-busy', 'true');
    feedback.textContent = 'Vérification de votre accès...';
    const options = {
      signal: controller.signal,
      onAccessDenied: error => blockAccess(error, version)
    };
    try {
      const session = await getCurrentUser(options);
      if (version !== requestVersion) return;
      if (session?.user?.is_admin !== true) {
        blockAccess({ status: 403 }, version);
        return;
      }
      feedback.textContent = 'Chargement des données...';
      const [stats, stories, proposals, reports] = await Promise.all([
        getAdminStats(options), getStories(options),
        getAdminProposals(options), getAdminReports(options)
      ]);
      if (version !== requestVersion) return;
      displayData(stats, stories, proposals, reports);
      feedback.textContent = 'Données chargées.';
    } catch (error) {
      if (version !== requestVersion) return;
      if ([401, 403].includes(error.status)) {
        blockAccess(error, version);
        return;
      }
      controller.abort();
      clearData();
      feedback.textContent = error.code === 'TIMEOUT' ?
        'Le serveur met trop de temps à répondre. Utilisez Actualiser pour réessayer.' :
        'Impossible de charger le tableau de bord. Utilisez Actualiser pour réessayer.';
    } finally {
      if (version === requestVersion) {
        activeRequest = null;
        dashboard.setAttribute('aria-busy', 'false');
        refresh.disabled = false;
      }
    }
  }

  refresh.addEventListener('click', () => {
    if (refresh.disabled) return;
    return loadDashboard();
  });
  window.addEventListener('pagehide', () => {
    cancelRequest();
    clearData();
  });
  window.addEventListener('pageshow', event => {
    if (event.persisted) return loadDashboard();
  });
  loadDashboard();
})();
