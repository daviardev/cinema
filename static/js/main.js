/* ════════════════════════════════════════════════════════════════
   MOCK DATA
════════════════════════════════════════════════════════════════ */
const mockData = {
  movies: [
    {
      id: 1,
      title: "Stellar Void",
      tagline: "Beyond the edge of the known universe",
      genre: ["Sci-Fi", "Aventura"],
      duration: 152,
      rating: 8.7,
      year: 2025,
      director: "Elena Voss",
      cast: ["Idris Elba", "Lupita Nyong'o", "Oscar Isaac"],
      synopsis:
        "Una tripulación de siete astronautas emprende una misión sin retorno hacia el borde del universo observable, donde las leyes de la física comienzan a colapsar y la realidad se vuelve indistinguible del sueño.",
      image:
        "https://images.unsplash.com/photo-1446776877081-d282a0f896e2?w=1200&q=80",
      poster:
        "https://images.unsplash.com/photo-1446776877081-d282a0f896e2?w=400&q=80",
      badge: "ESTRENO",
      accent: "#9580e0",
    },
    {
      id: 2,
      title: "The Last Signal",
      tagline: "They sent a message. We were not ready.",
      genre: ["Thriller", "Misterio"],
      duration: 118,
      rating: 8.2,
      year: 2025,
      director: "Marcus Webb",
      cast: ["Cate Blanchett", "Tom Hiddleston", "Tilda Swinton"],
      synopsis:
        "Cuando una estación de investigación submarina intercepta una señal cifrada de origen desconocido, el equipo debe descifrar su mensaje antes de que desencadene una serie de eventos catastróficos irreversibles.",
      image:
        "https://images.unsplash.com/photo-1478720568477-152d9b164e26?w=1200&q=80",
      poster:
        "https://images.unsplash.com/photo-1478720568477-152d9b164e26?w=400&q=80",
      badge: null,
      accent: "#0ea5e9",
    },
    {
      id: 3,
      title: "Ferro",
      tagline: "Algunas cadenas son invisibles",
      genre: ["Drama", "Historia"],
      duration: 138,
      rating: 9.1,
      year: 2025,
      director: "Camila Reyes",
      cast: ["Antonio Banderas", "Penélope Cruz", "Javier Bardem"],
      synopsis:
        "En la España de posguerra, un fundidor de hierro descubre un oscuro secreto enterrado bajo la fábrica donde trabaja. Una historia de memoria, redención y el peso invisible del pasado.",
      image:
        "https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?w=1200&q=80",
      poster:
        "https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?w=400&q=80",
      badge: "GANADOR",
      accent: "#e06030",
    },
    {
      id: 4,
      title: "Night Protocol",
      tagline: "Trust no one. Especially yourself.",
      genre: ["Acción", "Espionaje"],
      duration: 127,
      rating: 7.8,
      year: 2025,
      director: "James Harlow",
      cast: ["Idris Elba", "Ana de Armas", "Daniel Craig"],
      synopsis:
        "Una agente de inteligencia descubre que su propia organización ha infiltrado su memoria con recuerdos falsos. Para sobrevivir, debe descubrir quién es realmente antes de que la encuentren.",
      image:
        "https://images.unsplash.com/photo-1536440136628-849c177e76a1?w=1200&q=80",
      poster:
        "https://images.unsplash.com/photo-1536440136628-849c177e76a1?w=400&q=80",
      badge: null,
      accent: "#c4f030",
    },
    {
      id: 5,
      title: "Umbra",
      tagline: "What lives in the dark stays in the dark.",
      genre: ["Terror", "Suspenso"],
      duration: 108,
      rating: 7.5,
      year: 2025,
      director: "Ari Voss",
      cast: ["Florence Pugh", "Barry Keoghan", "Mia Goth"],
      synopsis:
        "Una familia se muda a una antigua mansión en los Alpes. Cada noche, las sombras adoptan formas que no deberían existir. Algo que lleva dormido siglos ha despertado con su llegada.",
      image:
        "https://images.unsplash.com/photo-1534073828943-f801091bb18c?w=1200&q=80",
      poster:
        "https://images.unsplash.com/photo-1534073828943-f801091bb18c?w=400&q=80",
      badge: "HOY",
      accent: "#8a1a10",
    },
    {
      id: 6,
      title: "Marea Alta",
      tagline: "El amor también puede ahogar",
      genre: ["Romance", "Drama"],
      duration: 115,
      rating: 8.0,
      year: 2025,
      director: "Sofía Leal",
      cast: ["Timothée Chalamet", "Zendaya", "Saoirse Ronan"],
      synopsis:
        "Dos jóvenes fotógrafos se conocen durante un naufragio en el Mediterráneo. Mientras esperan el rescate en una isla desierta, sus verdaderas naturalezas emergen bajo la presión del miedo y el deseo.",
      image:
        "https://images.unsplash.com/photo-1518709268805-4e9042af9f23?w=1200&q=80",
      poster:
        "https://images.unsplash.com/photo-1518709268805-4e9042af9f23?w=400&q=80",
      badge: null,
      accent: "#0ea5e9",
    },
  ],

  functions: [
    // Stellar Void
    {
      id: 101,
      movieId: 1,
      date: "2025-08-04",
      time: "14:30",
      hall: "Sala IMAX",
      price: 18.5,
      format: "IMAX 4K",
    },
    {
      id: 102,
      movieId: 1,
      date: "2025-08-04",
      time: "17:15",
      hall: "Sala Premium",
      price: 15.0,
      format: "Dolby Vision",
    },
    {
      id: 103,
      movieId: 1,
      date: "2025-08-04",
      time: "20:00",
      hall: "Sala 3",
      price: 12.5,
      format: "2D Digital",
    },
    {
      id: 104,
      movieId: 1,
      date: "2025-08-05",
      time: "16:00",
      hall: "Sala IMAX",
      price: 18.5,
      format: "IMAX 4K",
    },
    {
      id: 105,
      movieId: 1,
      date: "2025-08-05",
      time: "21:30",
      hall: "Sala Premium",
      price: 15.0,
      format: "Dolby Vision",
    },
    // The Last Signal
    {
      id: 201,
      movieId: 2,
      date: "2025-08-04",
      time: "15:00",
      hall: "Sala 2",
      price: 12.5,
      format: "2D Digital",
    },
    {
      id: 202,
      movieId: 2,
      date: "2025-08-04",
      time: "18:30",
      hall: "Sala Premium",
      price: 15.0,
      format: "Dolby Vision",
    },
    {
      id: 203,
      movieId: 2,
      date: "2025-08-04",
      time: "21:15",
      hall: "Sala 4",
      price: 12.5,
      format: "2D Digital",
    },
    {
      id: 204,
      movieId: 2,
      date: "2025-08-05",
      time: "19:00",
      hall: "Sala 2",
      price: 12.5,
      format: "2D Digital",
    },
    // Ferro
    {
      id: 301,
      movieId: 3,
      date: "2025-08-04",
      time: "16:45",
      hall: "Sala Premium",
      price: 15.0,
      format: "Dolby Atmos",
    },
    {
      id: 302,
      movieId: 3,
      date: "2025-08-04",
      time: "20:30",
      hall: "Sala 2",
      price: 12.5,
      format: "2D Digital",
    },
    {
      id: 303,
      movieId: 3,
      date: "2025-08-05",
      time: "17:00",
      hall: "Sala Premium",
      price: 15.0,
      format: "Dolby Atmos",
    },
    // Night Protocol
    {
      id: 401,
      movieId: 4,
      date: "2025-08-04",
      time: "14:00",
      hall: "Sala 3",
      price: 12.5,
      format: "2D Digital",
    },
    {
      id: 402,
      movieId: 4,
      date: "2025-08-04",
      time: "16:30",
      hall: "Sala IMAX",
      price: 18.5,
      format: "IMAX 4K",
    },
    {
      id: 403,
      movieId: 4,
      date: "2025-08-04",
      time: "19:45",
      hall: "Sala 3",
      price: 12.5,
      format: "2D Digital",
    },
    {
      id: 404,
      movieId: 4,
      date: "2025-08-05",
      time: "18:00",
      hall: "Sala IMAX",
      price: 18.5,
      format: "IMAX 4K",
    },
    // Umbra
    {
      id: 501,
      movieId: 5,
      date: "2025-08-04",
      time: "21:30",
      hall: "Sala 5",
      price: 12.5,
      format: "2D Digital",
    },
    {
      id: 502,
      movieId: 5,
      date: "2025-08-04",
      time: "23:00",
      hall: "Sala 5",
      price: 10.0,
      format: "2D Digital",
    },
    {
      id: 503,
      movieId: 5,
      date: "2025-08-05",
      time: "22:00",
      hall: "Sala 5",
      price: 12.5,
      format: "2D Digital",
    },
    // Marea Alta
    {
      id: 601,
      movieId: 6,
      date: "2025-08-04",
      time: "15:45",
      hall: "Sala 4",
      price: 12.5,
      format: "2D Digital",
    },
    {
      id: 602,
      movieId: 6,
      date: "2025-08-04",
      time: "18:00",
      hall: "Sala Premium",
      price: 15.0,
      format: "Dolby Vision",
    },
    {
      id: 603,
      movieId: 6,
      date: "2025-08-05",
      time: "16:30",
      hall: "Sala 4",
      price: 12.5,
      format: "2D Digital",
    },
  ],
};

/* ════════════════════════════════════════════════════════════════
   GLOBAL STATE
════════════════════════════════════════════════════════════════ */
const state = {
  currentView: "home",
  selectedMovie: null,
  selectedFunction: null,
  selectedSeats: [], // [{id, row, number, category, price}]
  seatMap: [], // full seat map for current function
  purchasing: false,
  ticketCode: null,
  activeGenreFilter: "all",
};

/* Persist/restore from localStorage */
function saveState() {
  try {
    const toSave = {
      selectedMovie: state.selectedMovie,
      selectedFunction: state.selectedFunction,
      selectedSeats: state.selectedSeats,
    };
    localStorage.setItem("cinevox_state", JSON.stringify(toSave));
  } catch (e) {}
}
function loadState() {
  try {
    const saved = JSON.parse(localStorage.getItem("cinevox_state") || "null");
    if (saved) {
      state.selectedMovie = saved.selectedMovie || null;
      state.selectedFunction = saved.selectedFunction || null;
      state.selectedSeats = saved.selectedSeats || [];
    }
  } catch (e) {}
}

/* ════════════════════════════════════════════════════════════════
   ROUTER
════════════════════════════════════════════════════════════════ */
const VIEWS = ["home", "detail", "seats", "confirm"];

function navigate(view, params = {}, pushToHistory = true) {
  if (!VIEWS.includes(view)) return;

  // Hide all views
  document.querySelectorAll(".view").forEach((v) => {
    v.classList.remove("active");
    v.style.display = "";
  });

  // Show target view
  const el = document.getElementById("view-" + view);
  if (!el) return;
  el.style.display = "block";
  setTimeout(() => el.classList.add("active"), 10);

  state.currentView = view;

  // Scroll to top
  window.scrollTo({ top: 0, behavior: "smooth" });

  // Update nav/progress
  updateNav(view);

  // Render view
  const renderers = {
    home: renderHome,
    detail: renderDetail,
    seats: renderSeats,
    confirm: renderConfirm,
  };
  if (renderers[view]) renderers[view]();

  // History API
  if (pushToHistory) {
    const url =
      "?view=" + view + (params.movieId ? "&m=" + params.movieId : "");
    history.pushState({ view, ...params }, "", url);
  }
}

// Browser back/forward
window.addEventListener("popstate", (e) => {
  if (e.state && e.state.view) {
    navigate(e.state.view, e.state, false);
  } else {
    navigate("home", {}, false);
  }
});

/* ════════════════════════════════════════════════════════════════
   NAV / PROGRESS HELPERS
════════════════════════════════════════════════════════════════ */
function updateNav(view) {
  const backBtn = document.getElementById("btn-back");
  const stepInd = document.getElementById("step-indicator");
  const cartChip = document.getElementById("cart-chip");
  const progFill = document.getElementById("progress-fill");

  const stepMap = { home: 1, detail: 2, seats: 3, confirm: 4 };
  const widths = { home: "25%", detail: "50%", seats: "75%", confirm: "100%" };

  // Back button
  if (view === "home") {
    backBtn.classList.remove("visible");
  } else {
    backBtn.classList.add("visible");
    backBtn.onclick = () => {
      const prev = { detail: "home", seats: "detail", confirm: "seats" };
      navigate(prev[view] || "home");
    };
  }

  // Step indicator
  if (view === "home") {
    stepInd.classList.remove("visible");
  } else {
    stepInd.classList.add("visible");
    const currentStep = stepMap[view];
    [1, 2, 3, 4].forEach((n) => {
      const el = document.getElementById("step-" + n);
      el.classList.remove("active", "done");
      if (n < currentStep) el.classList.add("done");
      if (n === currentStep) el.classList.add("active");
    });
  }

  // Cart chip
  const seatCount = state.selectedSeats.length;
  if (seatCount > 0 && (view === "seats" || view === "confirm")) {
    cartChip.classList.add("visible");
    document.getElementById("cart-count").textContent = seatCount;
  } else {
    cartChip.classList.remove("visible");
  }

  // Progress bar
  progFill.style.width = widths[view] || "25%";
}

/* ════════════════════════════════════════════════════════════════
   HOME RENDER
════════════════════════════════════════════════════════════════ */
function renderHome() {
  const grid = document.getElementById("movies-grid");
  const sub = document.getElementById("home-sub-count");

  // Build genre filter pills
  const genres = new Set(["all"]);
  mockData.movies.forEach((m) => m.genre.forEach((g) => genres.add(g)));
  const filtersEl = document.getElementById("genre-filters");
  filtersEl.innerHTML = "";
  genres.forEach((g) => {
    const btn = document.createElement("button");
    btn.className =
      "filter-pill" + (g === state.activeGenreFilter ? " active" : "");
    btn.dataset.genre = g;
    btn.textContent = g === "all" ? "Todas" : g;
    btn.onclick = () => {
      state.activeGenreFilter = g;
      document
        .querySelectorAll(".filter-pill")
        .forEach((p) => p.classList.remove("active"));
      btn.classList.add("active");
      renderMovieCards();
    };
    filtersEl.appendChild(btn);
  });

  renderMovieCards();

  sub.textContent = `— ${mockData.movies.length} películas disponibles`;
}

function renderMovieCards() {
  const grid = document.getElementById("movies-grid");
  const countEl = document.getElementById("count-display");

  const filtered =
    state.activeGenreFilter === "all"
      ? mockData.movies
      : mockData.movies.filter((m) =>
          m.genre.includes(state.activeGenreFilter),
        );

  countEl.textContent =
    filtered.length +
    " " +
    (filtered.length === 1 ? "resultado" : "resultados");

  if (filtered.length === 0) {
    grid.innerHTML = `<div class="empty-state" style="grid-column:1/-1">
      <div class="empty-icon">🎬</div>
      <div class="empty-title">Sin resultados</div>
      <p>No hay películas en esta categoría</p>
    </div>`;
    return;
  }

  grid.innerHTML = filtered
    .map(
      (m, i) => `
    <div class="movie-card-home"
      tabindex="0"
      role="button"
      aria-label="Ver ${m.title}"
      onclick="selectMovie(${m.id})"
      onkeydown="if(event.key==='Enter')selectMovie(${m.id})"
      style="animation-delay:${i * 60}ms"
    >
      ${m.badge ? `<div class="card-badge">${m.badge}</div>` : ""}
      <img class="card-poster" src="${m.poster}" alt="${m.title}" loading="lazy"/>
      <div class="card-overlay"></div>
      <div class="card-lime-glow"></div>
      <div class="card-body">
        <p class="card-genre">${m.genre.join(" · ")}</p>
        <h3 class="card-title">${m.title}</h3>
        <div class="card-meta">
          <span class="card-rating">★ ${m.rating}</span>
          <span>${m.duration} min</span>
          <span>${m.year}</span>
        </div>
        <div class="card-cta">
          Ver funciones
          <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
            <path d="M5 12h14M12 5l7 7-7 7"/>
          </svg>
        </div>
      </div>
    </div>
  `,
    )
    .join("");
}

/* ════════════════════════════════════════════════════════════════
   DETAIL RENDER
════════════════════════════════════════════════════════════════ */
function selectMovie(movieId) {
  const movie = mockData.movies.find((m) => m.id === movieId);
  if (!movie) return;
  state.selectedMovie = movie;
  state.selectedFunction = null;
  state.selectedSeats = [];
  saveState();
  navigate("detail", { movieId });
}

function renderDetail() {
  const movie = state.selectedMovie;
  if (!movie) {
    navigate("home");
    return;
  }

  document.getElementById("detail-bg").style.backgroundImage =
    `url('${movie.image}')`;
  document.getElementById("detail-poster").src = movie.poster;
  document.getElementById("detail-poster").alt = movie.title;
  document.getElementById("detail-title").textContent = movie.title;
  document.getElementById("detail-tagline").textContent = movie.tagline;
  document.getElementById("detail-synopsis").textContent = movie.synopsis;
  document.getElementById("detail-duration").textContent =
    movie.duration + " min";
  document.getElementById("detail-year").textContent = movie.year;
  document.getElementById("detail-director").textContent =
    "Dir. " + movie.director;
  document.getElementById("detail-rating").textContent = "★ " + movie.rating;

  // Genres
  document.getElementById("detail-genres").innerHTML = movie.genre
    .map((g) => `<span class="detail-genre-tag">${g}</span>`)
    .join("");

  // Cast
  document.getElementById("detail-cast").innerHTML = movie.cast
    .map((c) => `<span class="cast-chip">${c}</span>`)
    .join("");

  // Functions
  renderFunctions(movie.id);

  // Reset btn
  document.getElementById("btn-to-seats").disabled = true;
}

function renderFunctions(movieId) {
  const container = document.getElementById("functions-list");
  const fns = mockData.functions.filter((f) => f.movieId === movieId);

  if (fns.length === 0) {
    container.innerHTML =
      '<p class="text-muted" style="font-size:13px;">No hay funciones disponibles</p>';
    return;
  }

  // Group by date
  const byDate = {};
  fns.forEach((f) => {
    if (!byDate[f.date]) byDate[f.date] = [];
    byDate[f.date].push(f);
  });

  const dateLabels = {
    "2025-08-04": "Hoy — 4 Agosto",
    "2025-08-05": "Mañana — 5 Agosto",
  };

  container.innerHTML = Object.entries(byDate)
    .map(
      ([date, group]) => `
    <div class="functions-date-group">
      <div class="date-label">${dateLabels[date] || date}</div>
      <div class="function-cards">
        ${group
          .map(
            (fn) => `
          <div class="function-card ${state.selectedFunction && state.selectedFunction.id === fn.id ? "selected" : ""}"
            onclick="selectFunction(${fn.id})"
            role="button" tabindex="0"
            onkeydown="if(event.key==='Enter')selectFunction(${fn.id})"
            aria-label="${fn.time} - ${fn.hall}"
          >
            <div class="fn-time">${fn.time}</div>
            <div class="fn-details">
              <span class="fn-hall">${fn.hall}</span>
              <span class="fn-format">${fn.format}</span>
            </div>
            <div class="fn-price">
              <span class="fn-price-val">$${fn.price.toFixed(2)}</span>
              <span class="fn-price-label">por asiento</span>
            </div>
            <span class="fn-arrow">›</span>
          </div>
        `,
          )
          .join("")}
      </div>
    </div>
  `,
    )
    .join("");
}

function selectFunction(fnId) {
  const fn = mockData.functions.find((f) => f.id === fnId);
  if (!fn) return;
  state.selectedFunction = fn;
  state.selectedSeats = [];
  saveState();

  // Highlight selected
  document
    .querySelectorAll(".function-card")
    .forEach((c) => c.classList.remove("selected"));
  event.currentTarget.classList.add("selected");

  // Enable button
  const btn = document.getElementById("btn-to-seats");
  btn.disabled = false;
  btn.textContent = "";
  btn.innerHTML = `
    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
      <rect x="2" y="7" width="20" height="15" rx="2"/>
      <path d="M16 21V5a2 2 0 00-2-2h-4a2 2 0 00-2 2v16"/>
    </svg>
    Elegir asientos · ${fn.time}
  `;

  showToast("Función seleccionada: " + fn.time + " — " + fn.hall, "success");
}

function goToSeats() {
  if (!state.selectedFunction) return;
  navigate("seats", { movieId: state.selectedMovie.id });
}

/* ════════════════════════════════════════════════════════════════
   SEAT MAP LOGIC
════════════════════════════════════════════════════════════════ */
const ROWS = ["A", "B", "C", "D", "E", "F", "G", "H"];
const COLS = 10;

function getCategory(rowIndex) {
  if (rowIndex < 2) return "vip";
  if (rowIndex < 5) return "premium";
  return "standard";
}

function getPriceForCategory(basePrice, cat) {
  const add = { vip: 8, premium: 3, standard: 0 };
  return basePrice + add[cat];
}

// Deterministic seat reservation based on functionId
function generateSeatMap(functionId) {
  const reserved = new Set();
  // Simple seeded pseudo-random for consistent reservations per function
  const seeds = [
    functionId * 3,
    functionId * 7,
    functionId * 11,
    functionId * 13,
  ];
  seeds.forEach((seed) => {
    for (let i = 0; i < 8; i++) {
      const r =
        (((seed * (i + 3) * 17) % ROWS.length) + ROWS.length) % ROWS.length;
      const c = ((seed * (i + 5) * 13) % COLS) + 1;
      reserved.add(ROWS[r] + "-" + c);
    }
  });

  const seats = [];
  ROWS.forEach((row, ri) => {
    for (let c = 1; c <= COLS; c++) {
      const id = row + "-" + c;
      const cat = getCategory(ri);
      seats.push({
        id,
        row,
        number: c,
        category: cat,
        status: reserved.has(id) ? "reserved" : "available",
      });
    }
  });
  return seats;
}

function toggleSeat(seatId) {
  const fn = state.selectedFunction;
  const seat = state.seatMap.find((s) => s.id === seatId);
  if (!seat || seat.status === "reserved") return;

  const idx = state.selectedSeats.findIndex((s) => s.id === seatId);
  if (idx > -1) {
    // Deselect
    state.selectedSeats.splice(idx, 1);
  } else {
    // Limit: max 8 seats
    if (state.selectedSeats.length >= 8) {
      showToast("Máximo 8 asientos por compra", "error");
      return;
    }
    const price = getPriceForCategory(fn.price, seat.category);
    state.selectedSeats.push({ ...seat, price });
  }

  saveState();
  updateSeatVisuals();
  updateBookingPanel();
}

function updateSeatVisuals() {
  const selectedIds = new Set(state.selectedSeats.map((s) => s.id));
  document.querySelectorAll(".seat").forEach((el) => {
    const id = el.dataset.id;
    if (selectedIds.has(id)) {
      el.className = "seat selected";
    } else {
      const seat = state.seatMap.find((s) => s.id === id);
      if (seat) {
        el.className =
          seat.status === "reserved"
            ? "seat reserved"
            : "seat available-" +
              (seat.category === "vip"
                ? "vip"
                : seat.category === "premium"
                  ? "prm"
                  : "std");
      }
    }
  });
}

/* ════════════════════════════════════════════════════════════════
   SEATS VIEW RENDER
════════════════════════════════════════════════════════════════ */
function renderSeats() {
  const movie = state.selectedMovie;
  const fn = state.selectedFunction;
  if (!movie || !fn) {
    navigate("home");
    return;
  }

  document.getElementById("seat-movie-title").textContent = movie.title;
  document.getElementById("seat-fn-info").textContent =
    fn.date + " · " + fn.time + " · " + fn.hall + " · " + fn.format;

  // Generate seat map
  state.seatMap = generateSeatMap(fn.id);

  // Render grid
  const grid = document.getElementById("seat-grid");
  grid.innerHTML = "";

  const selectedIds = new Set(state.selectedSeats.map((s) => s.id));

  ROWS.forEach((row, ri) => {
    const rowWrap = document.createElement("div");
    rowWrap.className = "seat-row-wrap";

    // Row label
    const lbl = document.createElement("div");
    lbl.className = "row-label";
    lbl.textContent = row;
    rowWrap.appendChild(lbl);

    // Seats
    const rowEl = document.createElement("div");
    rowEl.className = "seat-row";

    state.seatMap
      .filter((s) => s.row === row)
      .forEach((seat, ci) => {
        // Aisle gap after seat 4
        if (ci === 4) {
          const aisle = document.createElement("div");
          aisle.className = "seat-aisle";
          rowEl.appendChild(aisle);
        }

        const btn = document.createElement("button");
        btn.dataset.id = seat.id;
        btn.setAttribute(
          "aria-label",
          `Fila ${seat.row} Asiento ${seat.number} (${seat.category})`,
        );

        if (seat.status === "reserved") {
          btn.className = "seat reserved";
          btn.disabled = true;
          btn.setAttribute("aria-disabled", "true");
        } else if (selectedIds.has(seat.id)) {
          btn.className = "seat selected";
        } else {
          const cls =
            seat.category === "vip"
              ? "available-vip"
              : seat.category === "premium"
                ? "available-prm"
                : "available-std";
          btn.className = "seat " + cls;
        }

        btn.onclick = () => toggleSeat(seat.id);
        rowEl.appendChild(btn);
      });

    rowWrap.appendChild(rowEl);
    grid.appendChild(rowWrap);
  });

  updateBookingPanel();
}

function updateBookingPanel() {
  const fn = state.selectedFunction;
  const movie = state.selectedMovie;
  const seats = state.selectedSeats;
  const count = seats.length;

  // Panel movie info
  const panelMovie = document.getElementById("panel-movie-info");
  if (panelMovie && movie && fn) {
    panelMovie.innerHTML = `
      <img class="panel-movie-poster" src="${movie.poster}" alt="${movie.title}"/>
      <div class="panel-movie-info">
        <div class="panel-movie-title">${movie.title}</div>
        <div class="panel-movie-fn">${fn.hall} · ${fn.format}</div>
        <div class="panel-movie-time">${fn.time}</div>
      </div>
    `;
  }

  // Selected list
  const listEl = document.getElementById("selected-list");
  if (listEl) {
    if (count === 0) {
      listEl.innerHTML = `<span class="no-seats-msg">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <circle cx="12" cy="12" r="10"/><path d="M12 8v4m0 4h.01"/>
        </svg>
        Toca un asiento para seleccionarlo
      </span>`;
    } else {
      listEl.innerHTML = seats
        .map(
          (s) => `
        <div class="seat-chip">
          ${s.row}${s.number}
          <button class="seat-chip-remove" onclick="toggleSeat('${s.id}')" aria-label="Quitar asiento">×</button>
        </div>
      `,
        )
        .join("");
    }
  }

  // Price
  const subtotal = seats.reduce((acc, s) => acc + s.price, 0);
  const fee = count > 0 ? parseFloat((subtotal * 0.08).toFixed(2)) : 0;
  const total = subtotal + fee;

  const fmt = (v) => "$" + v.toFixed(2);

  const setTxt = (id, val) => {
    const el = document.getElementById(id);
    if (el) el.textContent = val;
  };
  setTxt("seat-count-label", count);
  setTxt("subtotal-val", fmt(subtotal));
  setTxt("fee-val", fmt(fee));
  setTxt("total-val", fmt(total));

  // Mobile bar
  const mobileTotal = document.getElementById("mobile-total-val");
  const mobileSeats = document.getElementById("mobile-seats-label");
  if (mobileTotal) mobileTotal.textContent = fmt(total);
  if (mobileSeats)
    mobileSeats.textContent =
      count +
      " asiento" +
      (count !== 1 ? "s" : "") +
      " seleccionado" +
      (count !== 1 ? "s" : "");

  // Cart chip
  const cartChip = document.getElementById("cart-chip");
  if (count > 0) {
    cartChip.classList.add("visible");
    document.getElementById("cart-count").textContent = count;
  } else {
    cartChip.classList.remove("visible");
  }

  // Buttons
  const btnMain = document.getElementById("btn-purchase");
  const btnMobile = document.getElementById("btn-purchase-mobile");
  [btnMain, btnMobile].forEach((b) => {
    if (b) b.disabled = count === 0 || state.purchasing;
  });
}

/* ════════════════════════════════════════════════════════════════
   PURCHASE FLOW
════════════════════════════════════════════════════════════════ */
function generateTicketCode() {
  const alpha = "ABCDEFGHJKLMNPQRSTUVWXYZ";
  const nums = () => Math.floor(Math.random() * 9000 + 1000);
  const chars = () =>
    Array.from(
      { length: 3 },
      () => alpha[Math.floor(Math.random() * alpha.length)],
    ).join("");
  return `TKT-${nums()}-${chars()}${nums().toString().slice(0, 2)}`;
}

function purchase() {
  if (state.purchasing) return;
  if (state.selectedSeats.length === 0) {
    showToast("Selecciona al menos un asiento", "error");
    return;
  }

  state.purchasing = true;

  // Disable buttons + show loading
  const btnMain = document.getElementById("btn-purchase");
  const btnMobile = document.getElementById("btn-purchase-mobile");
  [btnMain, btnMobile].forEach((b) => {
    if (!b) return;
    b.disabled = true;
    b.innerHTML = `<span class="btn-ripple"></span>Procesando pago...`;
  });

  // Simulate network delay
  showToast("Procesando tu pago...", "info");

  setTimeout(() => {
    state.ticketCode = generateTicketCode();
    state.purchasing = false;

    // Mark seats as reserved in local map (simulate backend update)
    state.selectedSeats.forEach((s) => {
      const seat = state.seatMap.find((sm) => sm.id === s.id);
      if (seat) seat.status = "reserved";
    });

    saveState();
    showToast("¡Pago exitoso! Redirigiendo...", "success");

    setTimeout(() => navigate("confirm"), 600);
  }, 2200);
}

/* ════════════════════════════════════════════════════════════════
   CONFIRM RENDER
════════════════════════════════════════════════════════════════ */
function renderConfirm() {
  const movie = state.selectedMovie;
  const fn = state.selectedFunction;
  const seats = state.selectedSeats;

  if (!movie || !fn || !seats.length) {
    navigate("home");
    return;
  }

  const subtotal = seats.reduce((acc, s) => acc + s.price, 0);
  const fee = parseFloat((subtotal * 0.08).toFixed(2));
  const total = subtotal + fee;

  const setText = (id, val) => {
    const el = document.getElementById(id);
    if (el) el.textContent = val;
  };

  setText("ticket-movie", movie.title);
  setText("ticket-tagline", movie.tagline);
  setText("ticket-date", fn.date);
  setText("ticket-time", fn.time);
  setText("ticket-hall", fn.hall);
  setText("ticket-format", fn.format);
  setText("ticket-price", "$" + total.toFixed(2));
  setText("ticket-code", state.ticketCode || "TKT-0000-XXX");

  // Seat chips in ticket
  const seatsEl = document.getElementById("ticket-seats");
  if (seatsEl) {
    seatsEl.innerHTML = seats
      .map((s) => `<div class="ticket-seat-chip">${s.row}${s.number}</div>`)
      .join("");
  }

  // Generate decorative barcode bars
  const barcodeEl = document.getElementById("barcode");
  if (barcodeEl) {
    const heights = [
      20, 35, 28, 40, 18, 30, 38, 22, 40, 25, 32, 20, 38, 28, 18, 35, 40, 22,
      30, 25,
    ];
    barcodeEl.innerHTML = heights
      .map(
        (h, i) =>
          `<div class="barcode-bar" style="height:${h}px;opacity:${0.6 + (i % 3) * 0.13};animation-delay:${i * 30}ms"></div>`,
      )
      .join("");
  }
}

function resetAndGoHome() {
  state.selectedMovie = null;
  state.selectedFunction = null;
  state.selectedSeats = [];
  state.ticketCode = null;
  state.purchasing = false;
  state.seatMap = [];
  state.activeGenreFilter = "all";
  try {
    localStorage.removeItem("cinevox_state");
  } catch (e) {}
  navigate("home");
}

/* ════════════════════════════════════════════════════════════════
   TOAST SYSTEM
════════════════════════════════════════════════════════════════ */
const toastIcons = {
  success: "✓",
  error: "✕",
  info: "●",
};
function showToast(msg, type = "info") {
  const container = document.getElementById("toast-container");
  const toast = document.createElement("div");
  toast.className = "toast " + type;
  toast.innerHTML = `<span class="toast-icon">${toastIcons[type] || "●"}</span><span>${msg}</span>`;
  container.appendChild(toast);
  setTimeout(() => toast.remove(), 3000);
}

/* ════════════════════════════════════════════════════════════════
   INIT
════════════════════════════════════════════════════════════════ */
function init() {
  loadState();

  // Dismiss loading overlay after short delay
  setTimeout(() => {
    const overlay = document.getElementById("loading-overlay");
    overlay.classList.add("hidden");
    setTimeout(() => overlay.remove(), 500);
  }, 900);

  // Check URL params for deep linking
  const params = new URLSearchParams(window.location.search);
  const view = params.get("view");
  const mId = parseInt(params.get("m"));

  if (view && VIEWS.includes(view) && view !== "home") {
    if (mId) {
      const movie = mockData.movies.find((m) => m.id === mId);
      if (movie && !state.selectedMovie) state.selectedMovie = movie;
    }
    if (state.selectedMovie) {
      navigate(view, {}, false);
      return;
    }
  }

  navigate("home", {}, false);
}

init();
