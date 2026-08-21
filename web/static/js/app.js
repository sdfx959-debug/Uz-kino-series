
const tg = window.Telegram ? window.Telegram.WebApp : null;
if (tg) {
  tg.ready();
  tg.expand();
}

const scriptTag = document.currentScript;
const BOT_USERNAME = scriptTag ? scriptTag.getAttribute('data-bot-username') : '';

const grid = document.getElementById('movieGrid');
const loader = document.getElementById('loader');
const emptyState = document.getElementById('emptyState');
const searchInput = document.getElementById('searchInput');

let allMovies = [];
let searchTimeout = null;

async function fetchMovies(query = '') {
  loader.style.display = 'block';
  grid.innerHTML = '';
  emptyState.style.display = 'none';
  try {
    const url = query ? `/api/movies?q=${encodeURIComponent(query)}` : '/api/movies';
    const res = await fetch(url);
    const data = await res.json();
    allMovies = data;
    renderMovies(data);
  } catch (e) {
    loader.textContent = '❌ Xatolik yuz berdi';
  }
}

function renderMovies(movies) {
  loader.style.display = 'none';
  grid.innerHTML = '';
  if (!movies.length) {
    emptyState.style.display = 'block';
    return;
  }
  emptyState.style.display = 'none';
  movies.forEach(movie => {
    const card = document.createElement('div');
    card.className = 'movie-card';
    card.onclick = () => openModal(movie);

    const posterHtml = movie.poster_url
      ? `<img class="poster" src="${escapeHtml(movie.poster_url)}" alt="">`
      : `<div class="poster">🎬</div>`;

    card.innerHTML = `
      <span class="code-tag">${escapeHtml(movie.code)}</span>
      ${posterHtml}
      <div class="info">
        <h3>${escapeHtml(movie.title)}</h3>
        <div class="meta">
          <span>${escapeHtml(movie.genre || '—')}</span>
          <span>👁 ${movie.views}</span>
        </div>
      </div>
    `;
    grid.appendChild(card);
  });
}

function openModal(movie) {
  document.getElementById('modalTitle').textContent = movie.title;
  document.getElementById('modalDesc').textContent = movie.description || "Ma'lumot mavjud emas.";
  document.getElementById('modalGenre').textContent = '🎭 ' + (movie.genre || '—');
  document.getElementById('modalYear').textContent = '📅 ' + (movie.year || '—');
  document.getElementById('modalViews').textContent = '👁 ' + movie.views;

  const posterEl = document.getElementById('modalPoster');
  if (movie.poster_url) {
    posterEl.src = movie.poster_url;
    posterEl.style.display = 'block';
  } else {
    posterEl.style.display = 'none';
  }

  const watchBtn = document.getElementById('modalWatchBtn');
  watchBtn.href = `https://t.me/${BOT_USERNAME}?start=${encodeURIComponent(movie.code)}`;

  document.getElementById('modalOverlay').classList.add('active');
}

document.getElementById('modalClose').addEventListener('click', () => {
  document.getElementById('modalOverlay').classList.remove('active');
});
document.getElementById('modalOverlay').addEventListener('click', (e) => {
  if (e.target.id === 'modalOverlay') {
    document.getElementById('modalOverlay').classList.remove('active');
  }
});

searchInput.addEventListener('input', (e) => {
  clearTimeout(searchTimeout);
  const value = e.target.value.trim();
  searchTimeout = setTimeout(() => fetchMovies(value), 300);
});

function escapeHtml(str) {
  const div = document.createElement('div');
  div.textContent = str;
  return div.innerHTML;
}

fetchMovies();
  
