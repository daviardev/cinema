/* ════════════════════════════════════════════════════════════════
   UTILITY FUNCTIONS
════════════════════════════════════════════════════════════════ */
function formatPrice(value) {
  if (!value && value !== 0) return "$0,00";
  const num = parseFloat(value);
  return new Intl.NumberFormat("es-CO", {
    style: "currency",
    currency: "COP",
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  }).format(num);
}

/* ════════════════════════════════════════════════════════════════
   DATA
════════════════════════════════════════════════════════════════ */
let appData = {
  movies: [],
  functions: [],
};

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
  searchQuery: "",
};

/* Persist/restore from localStorage */
function saveState() {
  try {
    const toSave = {
      selectedMovie: state.selectedMovie,
      selectedFunction: state.selectedFunction,
      selectedSeats: state.selectedSeats,
      ticketCode: state.ticketCode,
    };
    console.log("💾 Guardando estado:", toSave);
    localStorage.setItem("cinevox_state", JSON.stringify(toSave));
  } catch (e) {
    console.error("Error al guardar estado:", e);
  }
}
function loadState() {
  try {
    const saved = JSON.parse(localStorage.getItem("cinevox_state") || "null");
    console.log("📂 Cargando estado:", saved);
    if (saved) {
      state.selectedMovie = saved.selectedMovie || null;
      state.selectedFunction = saved.selectedFunction || null;
      state.selectedSeats = saved.selectedSeats || [];
      state.ticketCode = saved.ticketCode || null;
      console.log("   state.ticketCode restaurado:", state.ticketCode);
    }
  } catch (e) {
    console.error("Error al cargar estado:", e);
  }
}

/* ════════════════════════════════════════════════════════════════
   ROUTER
════════════════════════════════════════════════════════════════ */
const VIEWS = [
  "home",
  "search",
  "detail",
  "seats",
  "confirm",
  "validate",
  "mytickets",
];

function navigate(view, params = {}, pushToHistory = true) {
  if (!VIEWS.includes(view)) return;

  console.log(`🔄 Navegando a vista: ${view}`);

  // Detener polling de asientos si salimos de seats
  if (view !== "seats") {
    stopSeatPolling();
  }

  // Si vamos a confirm, cargar el estado primero
  if (view === "confirm") {
    console.log("📂 Cargando estado antes de renderizar confirm");
    loadState();
  }

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
    validate: () => {
      resetValidateForm();
      document.getElementById("validate-code-input").focus();
    },
    mytickets: renderMyTickets,
  };
  const renderer = renderers[view];
  if (renderer) {
    const result = renderer();
    if (result instanceof Promise) {
      result.catch((err) => console.error("Error en renderer:", err));
    }
  }

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
      const prev = {
        detail: "home",
        seats: "detail",
        confirm: "seats",
        validate: "home",
        mytickets: "home",
      };
      navigate(prev[view] || "home");
    };
  }

  // Step indicator
  if (view === "home" || view === "validate" || view === "mytickets") {
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

  // Active view indicator in navbar
  const btnMyTickets = document.getElementById("btn-mytickets-nav");
  const btnValidate = document.getElementById("btn-validate-nav");
  if (btnMyTickets) {
    if (view === "mytickets") {
      btnMyTickets.style.background = "var(--cyan)";
      btnMyTickets.style.borderColor = "var(--cyan)";
      btnMyTickets.style.color = "var(--black)";
    } else {
      btnMyTickets.style.background = "rgba(0, 184, 212, 0.15)";
      btnMyTickets.style.borderColor = "var(--cyan)";
      btnMyTickets.style.color = "var(--white)";
    }
  }
  if (btnValidate) {
    if (view === "validate") {
      btnValidate.style.background = "var(--purple)";
      btnValidate.style.borderColor = "var(--purple)";
      btnValidate.style.color = "var(--black)";
    } else {
      btnValidate.style.background = "rgba(149, 128, 224, 0.15)";
      btnValidate.style.borderColor = "var(--purple)";
      btnValidate.style.color = "var(--white)";
    }
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
  const widths2 = {
    home: "0%",
    detail: "33%",
    seats: "66%",
    confirm: "100%",
    validate: "50%",
    mytickets: "0%",
  };
  progFill.style.width = widths2[view] || "0%";
}

/* ════════════════════════════════════════════════════════════════
   HOME RENDER
════════════════════════════════════════════════════════════════ */

function renderHome() {
  const sub = document.getElementById("home-sub-count");
  const searchInput = document.getElementById("movie-search-input");

  // Agregar búsqueda
  if (searchInput) {
    searchInput.value = state.searchQuery;
    searchInput.addEventListener("input", (e) => {
      state.searchQuery = e.target.value;
      renderMovieCards();
    });
  }

  // Cargar películas desde la API
  fetch("/api/peliculas")
    .then((response) => response.json())
    .then((data) => {
      // Mapear datos de la API al formato esperado
      appData.movies = data.map((p) => {
        console.log("Película:", p.titulo, "Actores DB:", p.actores);
        return {
          id: p.id,
          title: p.titulo,
          genre: p.categorias ? p.categorias.split(" · ") : ["Sin categoría"],
          duration: p.duracion,
          rating: p.puntuacion || 0,
          year: p.anio,
          director: p.director || "Desconocido",
          cast: p.actores ? p.actores.split(" · ") : [],
          synopsis: p.descripcion || "Sin sinopsis disponible",
          image: p.imagen_url,
          poster: p.imagen_url,
          badge:
            p.estado && p.estado !== "activa" ? p.estado.toUpperCase() : null,
          accent: "#9580e0",
          clasificacion: p.clasificacion,
        };
      });
      renderMovieCardsFromAPI();
    })
    .catch((err) => {
      console.error("Error cargando películas:", err);
      sub.textContent = "— Error al cargar películas";
    });
}

function renderMovieCardsFromAPI() {
  const filtersEl = document.getElementById("genre-filters");
  const sub = document.getElementById("home-sub-count");

  // Build genre filter pills desde datos cargados
  const genres = new Set(["all"]);
  appData.movies.forEach((m) => m.genre.forEach((g) => genres.add(g)));
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

  sub.textContent = `— ${appData.movies.length} películas disponibles`;
}

function renderMovieCards() {
  const grid = document.getElementById("movies-grid");
  const countEl = document.getElementById("count-display");

  let filtered =
    state.activeGenreFilter === "all"
      ? appData.movies
      : appData.movies.filter((m) => m.genre.includes(state.activeGenreFilter));

  // Agregar búsqueda por nombre
  if (state.searchQuery.trim()) {
    const query = state.searchQuery.toLowerCase();
    filtered = filtered.filter((m) => m.title.toLowerCase().includes(query));
  }

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
          ${m.clasificacion ? `<span class="card-rating-age">${m.clasificacion}</span>` : ""}
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
  const movie = appData.movies.find((m) => m.id === movieId);
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
  document.getElementById("detail-clasificacion").textContent =
    movie.clasificacion || "SIN CLASIFICAR";
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

  // Cargar funciones desde la API
  fetch(`/api/funciones/${movieId}`)
    .then((response) => response.json())
    .then((data) => {
      if (!data || data.length === 0) {
        container.innerHTML =
          '<p class="text-muted" style="font-size:13px;">No hay funciones disponibles</p>';
        return;
      }

      // Guardar funciones en appData
      appData.functions = data;

      // Mapear datos de la API y agrupar por fecha
      const byDate = {};
      data.forEach((f) => {
        if (!byDate[f.fecha]) byDate[f.fecha] = [];
        byDate[f.fecha].push(f);
      });

      // Formatear fechas dinámicamente
      const formatearFecha = (fechaStr) => {
        const hoy = new Date();
        const mañana = new Date(hoy);
        mañana.setDate(mañana.getDate() + 1);

        const formattedHoy = hoy.toISOString().split("T")[0];
        const formattedMañana = mañana.toISOString().split("T")[0];

        if (fechaStr === formattedHoy) {
          return `Hoy — ${new Date(fechaStr).toLocaleDateString("es-CO")}`;
        } else if (fechaStr === formattedMañana) {
          return `Mañana — ${new Date(fechaStr).toLocaleDateString("es-CO")}`;
        }
        return new Date(fechaStr).toLocaleDateString("es-CO");
      };

      container.innerHTML = Object.entries(byDate)
        .map(
          ([fecha, group]) => `
        <div class="functions-date-group">
          <div class="date-label">${formatearFecha(fecha)}</div>
          <div class="function-cards">
            ${group
              .map(
                (fn) => `
              <div class="function-card ${state.selectedFunction && state.selectedFunction.id === fn.id ? "selected" : ""}"
                onclick="selectFunction(${fn.id})"
                role="button" tabindex="0"
                onkeydown="if(event.key==='Enter')selectFunction(${fn.id})"
                aria-label="${fn.hora} - ${fn.sala}"
              >
                <div class="fn-time">${fn.hora}</div>
                <div class="fn-details">
                  <span class="fn-hall">${fn.sala}</span>
                  <span class="fn-format">${fn.tecnologia}</span>
                </div>
                <div class="fn-price">
                  <span class="fn-price-val">${formatPrice(fn.precio)}</span>
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
    })
    .catch((err) => {
      console.error("Error cargando funciones:", err);
      container.innerHTML =
        '<p class="text-muted" style="font-size:13px;">Error al cargar funciones</p>';
    });
}

function selectFunction(fnId) {
  const fn = appData.functions.find((f) => f.id === fnId);
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
    Elegir asientos · ${fn.hora}
  `;

  showToast("Función seleccionada: " + fn.hora + " — " + fn.sala, "success");
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
let seatPollingInterval = null;

function getCategory(rowIndex) {
  if (rowIndex < 2) return "vip";
  if (rowIndex < 5) return "premium";
  return "standard";
}

function getPriceForCategory(basePrice, cat) {
  const add = { vip: 8, premium: 3, standard: 0 };
  return basePrice + add[cat];
}

// Polling en tiempo real: Actualizar asientos cada 1.2 segundos
function startSeatPolling() {
  console.log("🔄 Iniciando polling de asientos en tiempo real");

  // Ejecutar inmediatamente
  pollSeatUpdates();

  // Luego cada 1.2 segundos
  seatPollingInterval = setInterval(pollSeatUpdates, 1200);
}

function stopSeatPolling() {
  if (seatPollingInterval) {
    console.log("⏹️ Deteniendo polling de asientos");
    clearInterval(seatPollingInterval);
    seatPollingInterval = null;
  }
}

function pollSeatUpdates() {
  const fn = state.selectedFunction;
  if (!fn) return;

  fetch(`/api/asientos/${fn.id}`)
    .then((res) => res.json())
    .then((data) => {
      const newSeatMap = data.map((a) => ({
        id: parseInt(a.id),
        numero: a.numero,
        row: a.fila,
        number: a.columna,
        category:
          a.tipo.toLowerCase() === "estandard"
            ? "std"
            : a.tipo.toLowerCase() === "premium"
              ? "prm"
              : "vip",
        tipo: a.tipo,
        precio: parseFloat(a.precio) || 0,
        // Mapear estados: "ocupado" y "reservado" = reserved, "disponible" = available
        status: a.estado === "disponible" ? "available" : "reserved",
      }));

      // Comparar y detectar cambios
      let changesDetected = false;
      for (let i = 0; i < newSeatMap.length; i++) {
        if (
          state.seatMap[i] &&
          state.seatMap[i].status !== newSeatMap[i].status
        ) {
          console.log(
            `📍 Cambio detectado en asiento ${newSeatMap[i].numero}: ${state.seatMap[i].status} → ${newSeatMap[i].status}`,
          );
          changesDetected = true;
        }
      }

      if (changesDetected) {
        console.log("🔄 Actualizando mapa de asientos desde servidor...");
        state.seatMap = newSeatMap;
        updateSeatVisuals();
      }
    })
    .catch((err) => console.error("Error en polling de asientos:", err));
}

// Deterministic seat reservation based on functionId
async function generateSeatMap(functionId) {
  try {
    const response = await fetch(`/api/asientos/${functionId}`);
    const data = await response.json();

    // Mapear datos de la API a formato esperado
    const seats = data.map((a) => ({
      id: parseInt(a.id),
      numero: a.numero,
      row: a.fila,
      number: a.columna,
      category:
        a.tipo.toLowerCase() === "estandard"
          ? "std"
          : a.tipo.toLowerCase() === "premium"
            ? "prm"
            : "vip",
      tipo: a.tipo,
      precio: parseFloat(a.precio) || 0,
      // Mapear: "disponible" = available, "ocupado" o "reservado" = reserved
      status: a.estado === "disponible" ? "available" : "reserved",
    }));

    return seats;
  } catch (err) {
    console.error("Error cargando asientos:", err);
    return [];
  }
}

function toggleSeat(seatId) {
  console.log("toggleSeat called with:", seatId);

  const fn = state.selectedFunction;
  const numSeatId = parseInt(seatId);
  console.log("numSeatId:", numSeatId);

  if (!fn || !state.seatMap) {
    console.error("Missing function or seatMap");
    return;
  }

  const seat = state.seatMap.find((s) => s.id === numSeatId);
  console.log("seat found:", seat);

  // Buscar si ya está seleccionado
  const isSelected = state.selectedSeats.some((s) => s.id === numSeatId);
  console.log("isSelected:", isSelected);

  // Si ya está seleccionado, no permitir hacer nada desde el grid
  if (isSelected) {
    console.log("Seat already selected, ignoring click");
    return;
  }

  // Si no está seleccionado
  if (!seat || seat.status === "reserved") {
    showToast("Este asiento no está disponible", "error");
    return;
  }

  // Limit: max 8 seats
  if (state.selectedSeats.length >= 8) {
    showToast("Máximo 8 asientos por compra", "error");
    return;
  }

  // Usar precio del asiento desde la API
  const price = parseFloat(seat.precio) || parseFloat(fn.precio) || 0;
  const newSeat = { ...seat, id: numSeatId, price };
  state.selectedSeats.push(newSeat);
  console.log("Seat added, selectedSeats:", state.selectedSeats);

  // Crear reserva temporal en la BD
  console.log("Calling API to create reservation...");
  fetch("/api/reserva-temporal/crear", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      funcion_id: fn.id,
      asiento_id: numSeatId,
    }),
  })
    .then((res) => {
      console.log("API Response status:", res.status);
      return res.json();
    })
    .then(async (data) => {
      console.log("API Response data:", data);
      if (data.success) {
        saveState();
        // Refrescar datos de asientos desde BD
        state.seatMap = await generateSeatMap(fn.id);
        console.log("Updated seatMap from API, length:", state.seatMap.length);
        console.log(
          "Before rebuildSeatGrid, selectedSeats:",
          state.selectedSeats,
        );
        rebuildSeatGrid();
        console.log("After rebuildSeatGrid");
        updateBookingPanel();
        console.log("After updateBookingPanel");
      } else {
        // Deshacer selección si falló la reserva
        state.selectedSeats = state.selectedSeats.filter(
          (s) => s.id !== numSeatId,
        );
        showToast("No se pudo reservar el asiento", "error");
        rebuildSeatGrid();
        updateBookingPanel();
      }
    })
    .catch((err) => {
      console.error("Error creating reservation:", err);
      state.selectedSeats = state.selectedSeats.filter(
        (s) => s.id !== numSeatId,
      );
      showToast("Error de red al reservar", "error");
      rebuildSeatGrid();
      updateBookingPanel();
    });
}

function removeSeat(seatId) {
  const numSeatId = parseInt(seatId);
  const idx = state.selectedSeats.findIndex((s) => s.id === numSeatId);

  if (idx > -1) {
    state.selectedSeats.splice(idx, 1);

    // Limpiar reserva temporal en la BD
    const fn = state.selectedFunction;
    fetch("/api/reserva-temporal/limpiar", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        funcion_id: fn.id,
        asiento_id: numSeatId,
      }),
    })
      .then((res) => res.json())
      .then(async (data) => {
        if (data.success) {
          saveState();
          // Refrescar datos de asientos desde BD
          state.seatMap = await generateSeatMap(fn.id);
          rebuildSeatGrid();
          updateBookingPanel();
        } else {
          showToast("Advertencia: no se limpió la reserva", "warning");
        }
      })
      .catch((err) => {
        console.error("Error limpiando reserva:", err);
        showToast("Error al deseleccionar asiento", "error");
      });
  }
}

function updateSeatVisuals() {
  const selectedIds = new Set(state.selectedSeats.map((s) => s.id));
  document.querySelectorAll(".seat").forEach((el) => {
    const id = parseInt(el.dataset.id);
    if (selectedIds.has(id)) {
      el.className = "seat selected";
      el.disabled = true;
      el.setAttribute("aria-disabled", "true");
    } else {
      const seat = state.seatMap.find((s) => s.id === id);
      if (seat) {
        if (seat.status === "reserved") {
          el.className = "seat reserved";
          el.disabled = true;
          el.setAttribute("aria-disabled", "true");
        } else {
          el.className =
            "seat available-" +
            (seat.category === "vip"
              ? "vip"
              : seat.category === "premium"
                ? "prm"
                : "std");
          el.disabled = false;
          el.removeAttribute("aria-disabled");
        }
      }
    }
  });
}

function rebuildSeatGrid() {
  console.log("rebuildSeatGrid called");
  const grid = document.getElementById("seat-grid");
  console.log("grid element:", grid);

  if (!grid || !state.seatMap) {
    console.error("Missing grid or seatMap");
    return;
  }

  grid.innerHTML = "";

  if (state.seatMap.length === 0) {
    grid.innerHTML =
      '<p class="text-muted" style="padding: 20px; text-align: center;">Cargando asientos...</p>';
    return;
  }

  console.log("Building grid with", state.seatMap.length, "seats");

  // Mostrar instrucción
  const instruction = document.createElement("div");
  instruction.style.cssText =
    "text-align: center; padding: 15px; color: #aaa; font-size: 13px; border-bottom: 1px solid #333; margin-bottom: 15px;";
  instruction.textContent = "Haz clic en un asiento para seleccionarlo";
  grid.appendChild(instruction);

  const selectedIds = new Set(state.selectedSeats.map((s) => s.id));
  console.log("selectedIds:", selectedIds);

  ROWS.forEach((row, ri) => {
    const rowWrap = document.createElement("div");
    rowWrap.className = "seat-row-wrap";

    const lbl = document.createElement("div");
    lbl.className = "row-label";
    lbl.textContent = row;
    rowWrap.appendChild(lbl);

    const rowEl = document.createElement("div");
    rowEl.className = "seat-row";

    state.seatMap
      .filter((s) => s.row === row)
      .forEach((seat, ci) => {
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
          btn.disabled = true;
          btn.setAttribute("aria-disabled", "true");
        } else {
          const cls =
            seat.category === "vip"
              ? "available-vip"
              : seat.category === "premium"
                ? "available-prm"
                : "available-std";
          btn.className = "seat " + cls;
          btn.disabled = false;
          btn.removeAttribute("aria-disabled");
        }

        btn.onclick = () => toggleSeat(seat.id);
        rowEl.appendChild(btn);
      });

    rowWrap.appendChild(rowEl);
    grid.appendChild(rowWrap);
  });

  console.log("Grid rebuilt complete");
}

/* ════════════════════════════════════════════════════════════════
   SEATS VIEW RENDER
════════════════════════════════════════════════════════════════ */
async function renderSeats() {
  const movie = state.selectedMovie;
  const fn = state.selectedFunction;
  if (!movie || !fn) {
    navigate("home");
    return;
  }

  document.getElementById("seat-movie-title").textContent = movie.title;
  document.getElementById("seat-fn-info").textContent =
    fn.fecha + " · " + fn.hora + " · " + fn.sala + " · " + fn.tecnologia;

  // Generate seat map desde la API
  state.seatMap = await generateSeatMap(fn.id);

  // Render grid using the rebuild function
  rebuildSeatGrid();

  updateBookingPanel();

  // ✨ Iniciar polling de asientos en tiempo real
  startSeatPolling();
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
        <div class="panel-movie-fn">${fn.sala} · ${fn.tecnologia}</div>
        <div class="panel-movie-time">${fn.hora}</div>
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
          <button class="seat-chip-remove" onclick="removeSeat('${s.id}')" aria-label="Quitar asiento">×</button>
        </div>
      `,
        )
        .join("");
    }
  }

  // Price
  const subtotal = seats.reduce((acc, s) => {
    const price = parseFloat(s.price) || 0;
    return acc + price;
  }, 0);
  const fee = count > 0 ? parseFloat((subtotal * 0.08).toFixed(2)) : 0;
  const total = subtotal + fee;

  const fmt = (v) => formatPrice(typeof v === "number" ? v : 0);

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
  console.log("purchase() called");

  if (state.purchasing) {
    console.log("Already purchasing");
    return;
  }
  if (state.selectedSeats.length === 0) {
    showToast("Selecciona al menos un asiento", "error");
    return;
  }

  console.log("Generating ticket code...");
  // Generar código de ticket
  state.ticketCode = generateTicketCode();
  console.log("Ticket code generated:", state.ticketCode);

  // Mostrar modal de confirmación
  console.log("Opening confirmation modal...");
  openConfirmationModal();
}

function openConfirmationModal() {
  const movie = state.selectedMovie;
  const fn = state.selectedFunction;
  const seats = state.selectedSeats;
  const subtotal = seats.reduce((acc, s) => acc + parseFloat(s.price || 0), 0);
  const fee = parseFloat((subtotal * 0.08).toFixed(2));
  const total = subtotal + fee;

  let modal = document.getElementById("confirmation-modal");

  if (!modal) {
    const modalHtml = `
      <div id="confirmation-modal" class="confirmation-modal" style="position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.9); display: flex; align-items: center; justify-content: center; z-index: 10000; padding: 20px; overflow-y: auto;">
        <div style="background: #1a1a1a; border: 1px solid #333; border-radius: 12px; padding: 40px; max-width: 500px; width: 100%;">
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 30px;">
            <h2 style="margin: 0; color: #fff; font-size: 24px; font-weight: bold;">Resumen de Compra</h2>
            <button onclick="closeConfirmationModal()" style="background: none; border: none; color: #999; font-size: 28px; cursor: pointer; padding: 0; line-height: 1;">×</button>
          </div>
          
          <div style="margin-bottom: 30px; padding-bottom: 30px; border-bottom: 1px solid #333;">
            <h3 style="color: #9580e0; font-size: 14px; text-transform: uppercase; letter-spacing: 1px; margin: 0 0 15px 0;">Película</h3>
            <p style="color: #fff; margin: 0; font-size: 18px; font-weight: bold;" id="conf-movie"></p>
            <p style="color: #aaa; margin: 5px 0 0 0; font-size: 13px;" id="conf-tagline"></p>
          </div>
          
          <div style="margin-bottom: 30px; padding-bottom: 30px; border-bottom: 1px solid #333;">
            <h3 style="color: #9580e0; font-size: 14px; text-transform: uppercase; letter-spacing: 1px; margin: 0 0 15px 0;">Detalles</h3>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
              <div>
                <p style="color: #aaa; margin: 0; font-size: 11px; text-transform: uppercase; letter-spacing: 1px;">Fecha</p>
                <p style="color: #fff; margin: 5px 0 0 0; font-size: 14px;" id="conf-date"></p>
              </div>
              <div>
                <p style="color: #aaa; margin: 0; font-size: 11px; text-transform: uppercase; letter-spacing: 1px;">Hora</p>
                <p style="color: #fff; margin: 5px 0 0 0; font-size: 14px;" id="conf-time"></p>
              </div>
              <div>
                <p style="color: #aaa; margin: 0; font-size: 11px; text-transform: uppercase; letter-spacing: 1px;">Sala</p>
                <p style="color: #fff; margin: 5px 0 0 0; font-size: 14px;" id="conf-hall"></p>
              </div>
              <div>
                <p style="color: #aaa; margin: 0; font-size: 11px; text-transform: uppercase; letter-spacing: 1px;">Formato</p>
                <p style="color: #fff; margin: 5px 0 0 0; font-size: 14px;" id="conf-format"></p>
              </div>
            </div>
          </div>
          
          <div style="margin-bottom: 30px; padding-bottom: 30px; border-bottom: 1px solid #333;">
            <h3 style="color: #9580e0; font-size: 14px; text-transform: uppercase; letter-spacing: 1px; margin: 0 0 15px 0;">Asientos</h3>
            <div style="display: flex; flex-wrap: wrap; gap: 8px;" id="conf-seats"></div>
          </div>
          
          <div style="margin-bottom: 30px; padding: 20px; background: #0a0a0a; border-radius: 8px;">
            <div style="display: flex; justify-content: space-between; margin-bottom: 12px;">
              <span style="color: #aaa;">Subtotal</span>
              <span style="color: #fff;" id="conf-subtotal"></span>
            </div>
            <div style="display: flex; justify-content: space-between; margin-bottom: 12px;">
              <span style="color: #aaa;">Fee (8%)</span>
              <span style="color: #fff;" id="conf-fee"></span>
            </div>
            <div style="display: flex; justify-content: space-between; border-top: 1px solid #333; padding-top: 12px;">
              <span style="color: #fff; font-weight: bold;">Total</span>
              <span style="color: #00b8d4; font-weight: bold; font-size: 18px;" id="conf-total"></span>
            </div>
          </div>
          
          <div style="display: flex; gap: 12px;">
            <button onclick="closeConfirmationModal()" style="flex: 1; padding: 14px; background: #333; border: 1px solid #444; border-radius: 6px; color: #fff; cursor: pointer; font-size: 14px; font-weight: bold; text-transform: uppercase; letter-spacing: 0.5px;">Cancelar</button>
            <button onclick="proceedToEmailModal()" style="flex: 1; padding: 14px; background: #9580e0; border: none; border-radius: 6px; color: #000; cursor: pointer; font-size: 14px; font-weight: bold; text-transform: uppercase; letter-spacing: 0.5px;">✓ Confirmar</button>
          </div>
        </div>
      </div>
    `;

    document.body.insertAdjacentHTML("beforeend", modalHtml);
    modal = document.getElementById("confirmation-modal");
  }

  // Llenar datos
  function setText(id, val) {
    const el = document.getElementById(id);
    if (el) el.textContent = val;
  }

  setText("conf-movie", movie?.title || "");
  setText("conf-tagline", movie?.tagline || "");
  setText("conf-date", fn?.fecha || "");
  setText("conf-time", fn?.hora || "");
  setText("conf-hall", fn?.sala || "");
  setText("conf-format", fn?.tecnologia || "");
  setText("conf-subtotal", formatPrice(subtotal));
  setText("conf-fee", formatPrice(fee));
  setText("conf-total", formatPrice(total));

  const seatsEl = document.getElementById("conf-seats");
  if (seatsEl) {
    seatsEl.innerHTML = seats
      .map(
        (s) =>
          `<div style="background: #9580e0; color: #000; padding: 6px 12px; border-radius: 4px; font-size: 12px; font-weight: bold;">${s.row}${s.number}</div>`,
      )
      .join("");
  }

  modal.style.display = "flex";
}

function closeConfirmationModal() {
  const modal = document.getElementById("confirmation-modal");
  if (modal) modal.style.display = "none";
}

function proceedToEmailModal() {
  closeConfirmationModal();
  openEmailModal();
}

function openEmailModal() {
  console.log("openEmailModal called");

  // Crear la modal dinámicamente
  let modal = document.getElementById("email-modal");

  if (!modal) {
    const modalHtml = `
      <div id="email-modal" class="email-modal" style="position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.8); display: flex; align-items: center; justify-content: center; z-index: 10000;">
        <div style="background: #1a1a1a; border: 1px solid #333; border-radius: 8px; padding: 30px; max-width: 400px; width: 90%;">
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
            <h2 style="margin: 0; color: #fff; font-size: 20px;">Confirmar Compra</h2>
            <button onclick="closeEmailModal()" style="background: none; border: none; color: #999; font-size: 24px; cursor: pointer; padding: 0;">×</button>
          </div>
          <div style="margin-bottom: 20px;">
            <p style="color: #aaa; margin: 0 0 15px 0;">Ingresa tu correo para recibir tu tiquete:</p>
            <input 
              type="email" 
              id="email-input" 
              placeholder="tu.email@ejemplo.com" 
              style="width: 100%; padding: 12px; box-sizing: border-box; background: #0a0a0a; border: 1px solid #333; border-radius: 4px; color: #fff; font-size: 14px;"
            />
          </div>
          <div style="display: flex; gap: 10px;">
            <button onclick="closeEmailModal()" style="flex: 1; padding: 12px; background: #333; border: 1px solid #444; border-radius: 4px; color: #fff; cursor: pointer; font-size: 14px;">Cancelar</button>
            <button onclick="submitEmail()" style="flex: 1; padding: 12px; background: #9580e0; border: none; border-radius: 4px; color: #000; font-weight: bold; cursor: pointer; font-size: 14px;">Completar Compra</button>
          </div>
        </div>
      </div>
    `;

    document.body.insertAdjacentHTML("beforeend", modalHtml);
    modal = document.getElementById("email-modal");
  }

  const input = document.getElementById("email-input");
  if (input) {
    input.value = "";
    input.focus();
  }

  modal.style.display = "flex";
  console.log("Modal opened");
}

function closeEmailModal() {
  const modal = document.getElementById("email-modal");
  if (modal) {
    modal.style.display = "none";
  }
}

function submitEmail() {
  const email = document.getElementById("email-input").value.trim();

  if (!email || !email.includes("@")) {
    showToast("Por favor ingresa un correo válido", "error");
    return;
  }

  closeEmailModal();
  confirmPurchaseWithEmail(email);
}

async function confirmPurchaseWithEmail(email) {
  const btnMain = document.getElementById("btn-purchase");
  const btnMobile = document.getElementById("btn-purchase-mobile");

  [btnMain, btnMobile].forEach((b) => {
    if (!b) return;
    b.disabled = true;
    b.innerHTML = `<span class="btn-ripple"></span>Procesando compra...`;
  });

  showToast("Procesando tu compra...", "info");

  try {
    const fn = state.selectedFunction;
    const asiento_ids = state.selectedSeats.map((s) => s.id);
    const total = state.selectedSeats.reduce(
      (sum, s) => sum + (parseFloat(s.price) || 0),
      0,
    );

    const response = await fetch("/api/procesar-compra", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        funcion_id: fn.id,
        asiento_ids: asiento_ids,
        email: email,
        ticket_code: state.ticketCode,
        total: total,
      }),
    });

    const data = await response.json();

    console.log("📡 Response from server:", data);

    if (data.success) {
      console.log("✓ Compra exitosa!");
      console.log("   Ticket ID:", data.ticket_id);
      console.log("   Ticket Code:", data.ticket_code);
      console.log("   state.ticketCode antes:", state.ticketCode);

      // Asegurar que el código se mantiene en el estado
      state.ticketCode = data.ticket_code || state.ticketCode;

      console.log("   state.ticketCode después:", state.ticketCode);

      showToast("¡Compra exitosa! Redirigiendo...", "success");

      // Marcar asientos como ocupados en el estado local
      state.selectedSeats.forEach((s) => {
        const seat = state.seatMap.find((sm) => sm.id === s.id);
        if (seat) seat.status = "reserved";
      });

      console.log("💾 Guardando estado...");
      saveState();

      setTimeout(() => {
        console.log("🔄 Navegando a confirm");
        navigate("confirm");
      }, 600);
    } else {
      [btnMain, btnMobile].forEach((b) => {
        if (!b) return;
        b.disabled = false;
        b.innerHTML = `<span class="btn-ripple"></span>COMPRAR ENTRADA`;
      });
      showToast(
        "Error: " + (data.error || "No se pudo procesar la compra"),
        "error",
      );
    }
  } catch (err) {
    console.error("Error processing purchase:", err);
    const btnMain = document.getElementById("btn-purchase");
    const btnMobile = document.getElementById("btn-purchase-mobile");
    [btnMain, btnMobile].forEach((b) => {
      if (!b) return;
      b.disabled = false;
      b.innerHTML = `<span class="btn-ripple"></span>COMPRAR ENTRADA`;
    });
    showToast("Error de conexión: " + err.message, "error");
  }
}

/* ════════════════════════════════════════════════════════════════
   CONFIRM RENDER
════════════════════════════════════════════════════════════════ */
function renderConfirm() {
  const movie = state.selectedMovie;
  const fn = state.selectedFunction;
  const seats = state.selectedSeats;

  console.log("🎟️ renderConfirm() called");
  console.log("   movie:", movie?.title);
  console.log("   function:", fn?.id);
  console.log("   seats:", seats.length);
  console.log("   state.ticketCode:", state.ticketCode);
  console.log("   Full state:", state);

  if (!movie || !fn || !seats.length) {
    console.warn("⚠️ Missing data, navigating to home");
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
  setText("ticket-date", fn.fecha);
  setText("ticket-time", fn.hora);
  setText("ticket-hall", fn.sala);
  setText("ticket-format", fn.tecnologia);
  setText("ticket-price", formatPrice(total));
  setText("ticket-code", state.ticketCode || "TKT-0000-XXX");

  console.log("📄 Texto de código establecido a:", state.ticketCode);

  // Seat chips in ticket
  const seatsEl = document.getElementById("ticket-seats");
  if (seatsEl) {
    seatsEl.innerHTML = seats
      .map((s) => `<div class="ticket-seat-chip">${s.row}${s.number}</div>`)
      .join("");
  }

  // Generate QR Code
  const barcodeEl = document.getElementById("barcode");
  if (barcodeEl) {
    barcodeEl.innerHTML = ""; // Clear previous QR
    const ticketCode = state.ticketCode;

    if (!ticketCode || ticketCode === "TKT-0000-XXX") {
      console.error("✗ ERROR: No hay código de ticket válido para generar QR");
      console.error("   state.ticketCode:", ticketCode);
      barcodeEl.textContent = "❌ Error: Código no disponible";
      showToast(
        "Error: No se pudo generar el QR. Tema ticket no guardado.",
        "error",
      );
      return;
    }

    console.log("🔲 Generando QR con código:", ticketCode);
    try {
      new QRCode(barcodeEl, {
        text: ticketCode,
        width: 120,
        height: 120,
        colorDark: "#f5f2e8",
        colorLight: "#0f0f0e",
        correctLevel: QRCode.CorrectLevel.H,
      });
      console.log("✓ QR generado exitosamente");
    } catch (e) {
      console.error("✗ Error generating QR:", e);
      barcodeEl.textContent = "QR Error";
    }
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
  state.searchQuery = "";
  try {
    localStorage.removeItem("cinevox_state");
  } catch (e) {}
  navigate("home");
}

/* ════════════════════════════════════════════════════════════════
   MIS ENTRADAS (My Tickets)
════════════════════════════════════════════════════════════════ */
function renderMyTickets() {
  const container = document.getElementById("mytickets-container");
  if (!container) return;

  container.innerHTML = `
    <div style="max-width: 600px; margin: 40px auto; padding: 20px;">
      <h2 style="color: #fff; margin-bottom: 20px;">🎫 Mis Entradas</h2>
      <p style="color: #aaa; margin-bottom: 15px;">Ingresa tu correo para ver tus entradas compradas:</p>
      
      <div style="display: flex; gap: 10px; margin-bottom: 30px;">
        <input 
          type="email" 
          id="mytickets-email-input" 
          placeholder="tu.email@ejemplo.com"
          style="flex: 1; padding: 12px; background: #0a0a0a; border: 1px solid #333; border-radius: 4px; color: #fff; font-size: 14px;"
        />
        <button 
          onclick="searchMyTickets()"
          style="padding: 12px 24px; background: #9580e0; border: none; border-radius: 4px; color: #000; font-weight: bold; cursor: pointer; font-size: 14px;"
        >
          Buscar
        </button>
      </div>
      
      <div id="mytickets-results" style="margin-top: 20px;"></div>
    </div>
  `;
}

function searchMyTickets() {
  const email = document.getElementById("mytickets-email-input").value.trim();
  const resultsDiv = document.getElementById("mytickets-results");

  if (!email) {
    showToast("Por favor ingresa un correo válido", "error");
    return;
  }

  resultsDiv.innerHTML = `<p style="color: #aaa; text-align: center;">Buscando tus entradas...</p>`;

  fetch(`/api/mis-tiquetes?email=${encodeURIComponent(email)}`)
    .then((res) => res.json())
    .then((data) => {
      if (data.success && data.tickets && data.tickets.length > 0) {
        resultsDiv.innerHTML = data.tickets
          .map(
            (t) => `
          <div style="background: #1a1a1a; border: 1px solid #333; border-radius: 8px; padding: 20px; margin-bottom: 15px;">
            <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 15px;">
              <div>
                <h3 style="color: #fff; margin: 0 0 5px 0;">${t.pelicula_titulo}</h3>
                <p style="color: #aaa; margin: 0; font-size: 13px;">${t.fecha} · ${t.hora}</p>
              </div>
              <span style="${t.estado === "canjeado" ? "color: #66cc99;" : "color: #9580e0;"} font-weight: bold; font-size: 12px;">
                ${t.estado === "canjeado" ? "✓ CANJEADO" : "● ACTIVO"}
              </span>
            </div>
            
            <div style="padding: 12px; background: #0a0a0a; border-radius: 4px; margin-bottom: 12px;">
              <p style="color: #aaa; margin: 0 0 5px 0; font-size: 12px;">CÓDIGO</p>
              <p style="color: #fff; margin: 0; font-family: monospace; font-size: 16px; font-weight: bold;">${t.codigo}</p>
            </div>
            
            <div style="display: flex; gap: 15px; font-size: 12px;">
              <div>
                <p style="color: #aaa; margin: 0;">Asientos</p>
                <p style="color: #fff; margin: 5px 0 0 0;">${t.asientos.map((a) => a.numero).join(", ")}</p>
              </div>
              <div>
                <p style="color: #aaa; margin: 0;">Sala</p>
                <p style="color: #fff; margin: 5px 0 0 0;">${t.sala}</p>
              </div>
              <div>
                <p style="color: #aaa; margin: 0;">Total</p>
                <p style="color: #fff; margin: 5px 0 0 0;">${formatPrice(t.total)}</p>
              </div>
            </div>
          </div>
        `,
          )
          .join("");
        showToast(
          `✓ ${data.tickets.length} entrada${data.tickets.length !== 1 ? "s" : ""} encontrada${data.tickets.length !== 1 ? "s" : ""}`,
          "success",
        );
      } else {
        resultsDiv.innerHTML = `
          <div style="text-align: center; padding: 40px 20px;">
            <p style="color: #aaa; margin: 0;">No hay entradas registradas para este correo</p>
          </div>
        `;
        showToast("Sin entradas encontradas", "error");
      }
    })
    .catch((err) => {
      console.error("Error:", err);
      resultsDiv.innerHTML = `<p style="color: #ff6b6b; text-align: center;">Error al buscar tus entradas</p>`;
      showToast("Error al buscar", "error");
    });
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
   VALIDATE TICKET
════════════════════════════════════════════════════════════════ */
let currentTicketCode = null;
let currentTicketData = null;
let isAutoRedeeming = false;

// 🎫 Función para buscar, validar y canjear ticket desde QR (automático)
function searchAndAutoRedeem(code) {
  console.log("🎫 Buscando y canjeando automáticamente:", code);
  isAutoRedeeming = true;

  const codeInput = document.getElementById("validate-code-input");
  codeInput.disabled = true;

  // Reset states
  document.getElementById("validate-not-found").style.display = "none";
  document.getElementById("validate-found").style.display = "none";
  document.getElementById("validate-redeemed").style.display = "none";

  showToast("Validando entrada...", "info");

  fetch(`/api/verificar-ticket/${code}`)
    .then((res) => res.json())
    .then((data) => {
      if (data.success && data.ticket) {
        console.log("✓ Ticket encontrado:", data.ticket.estado);
        currentTicketCode = code;
        currentTicketData = data.ticket;

        // Si ya está canjeado, mostrar error
        if (data.ticket.estado === "canjeado") {
          console.warn("⚠️ Ticket ya fue canjeado");
          displayTicketDetails(data.ticket);
          showToast("⚠️ Esta entrada ya fue utilizada", "error");
          isAutoRedeeming = false;
          codeInput.disabled = false;
          return;
        }

        // Canjear automáticamente
        const btn = document.getElementById("btn-redeem");
        btn.disabled = true;
        btn.textContent = "Canjeando...";

        fetch(`/api/canjear-ticket/${code}`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
        })
          .then((res) => res.json())
          .then((redeemData) => {
            if (redeemData.success) {
              console.log("✓ Ticket canjeado exitosamente");
              document.getElementById("validate-found").style.display = "none";
              document.getElementById("validate-redeemed").style.display =
                "block";
              showToast("✓ ¡Entrada validada y canjeada!", "success");
              setTimeout(() => {
                resetValidateForm();
                isAutoRedeeming = false;
              }, 3000);
            } else {
              console.error("✗ Error canjeando:", redeemData.error);
              displayTicketDetails(data.ticket);
              document.getElementById("validate-found").style.display = "block";
              showToast(redeemData.error || "No se pudo canjear", "error");
              btn.disabled = false;
              btn.textContent = "Canjear Entrada";
              isAutoRedeeming = false;
            }
          })
          .catch((err) => {
            console.error("Error canjeando:", err);
            displayTicketDetails(data.ticket);
            document.getElementById("validate-found").style.display = "block";
            showToast("Error al procesar", "error");
            document.getElementById("btn-redeem").disabled = false;
            document.getElementById("btn-redeem").textContent =
              "Canjear Entrada";
            isAutoRedeeming = false;
          });
      } else {
        console.error("✗ Ticket no encontrado:", data.error);
        document.getElementById("validate-not-found").style.display = "block";
        showToast("Entrada no encontrada", "error");
        codeInput.disabled = false;
        isAutoRedeeming = false;
      }
    })
    .catch((err) => {
      console.error("Error buscando:", err);
      document.getElementById("validate-not-found").style.display = "block";
      showToast("Error al buscar", "error");
      codeInput.disabled = false;
      isAutoRedeeming = false;
    });
}

function searchTicket() {
  const codeInput = document.getElementById("validate-code-input");
  let code = codeInput.value.trim().toUpperCase();

  console.log("🔍 Buscando ticket:", code);

  if (!code) {
    console.warn("⚠️ Código vacío");
    showToast("Ingresa un código de ticket", "error");
    return;
  }

  // Formatear el código automáticamente: remover todo excepto alfanuméricos
  let cleaned = code.replace(/[^0-9A-Z]/g, "");

  if (cleaned.length !== 9) {
    console.warn(
      "⚠️ Código incompleto:",
      cleaned.length,
      "caracteres (se esperan 9)",
    );
    showToast("Código incompleto. Ejemplo: 6956ZHD14", "error");
    return;
  }

  // Formatear a TKT-XXXX-XXXXX
  code = "TKT-" + cleaned.slice(0, 4) + "-" + cleaned.slice(4, 9);
  console.log("📝 Código formateado:", code);
  codeInput.value = code;

  // Reset states
  document.getElementById("validate-not-found").style.display = "none";
  document.getElementById("validate-found").style.display = "none";
  document.getElementById("validate-redeemed").style.display = "none";

  // Show loading
  codeInput.disabled = true;
  const searchBtn = document.querySelector(".validate-search-btn");
  searchBtn.disabled = true;
  searchBtn.textContent = "Buscando...";

  // API call
  console.log("📡 Haciendo request a /api/verificar-ticket/" + code);
  fetch(`/api/verificar-ticket/${code}`)
    .then((res) => {
      console.log("📡 Response status:", res.status);
      return res.json();
    })
    .then((data) => {
      console.log("✓ Response data:", data);

      codeInput.disabled = false;
      searchBtn.disabled = false;
      searchBtn.innerHTML =
        '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.35-4.35"/></svg>Buscar';

      if (data.success && data.ticket) {
        console.log("✓ Ticket encontrado:", data.ticket);
        currentTicketCode = code;
        currentTicketData = data.ticket;
        displayTicketDetails(data.ticket);
      } else {
        console.error("✗ Ticket no encontrado o error:", data.error);
        document.getElementById("validate-not-found").style.display = "block";
        showToast("Ticket no encontrado", "error");
      }
    })
    .catch((err) => {
      console.error("Error:", err);
      codeInput.disabled = false;
      searchBtn.disabled = false;
      searchBtn.innerHTML =
        '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.35-4.35"/></svg>Buscar';
      document.getElementById("validate-not-found").style.display = "block";
      showToast("Error al buscar el ticket", "error");
    });
}

function displayTicketDetails(ticket) {
  const found = document.getElementById("validate-found");

  // Fill ticket details
  document.getElementById("validate-movie").textContent =
    ticket.pelicula_titulo || "N/A";
  document.getElementById("validate-datetime").textContent =
    `${ticket.fecha} ${ticket.hora}` || "N/A";
  document.getElementById("validate-sala").textContent = ticket.sala || "N/A";

  // Format seats
  const seatsStr =
    ticket.asientos && Array.isArray(ticket.asientos)
      ? ticket.asientos.map((a) => a.numero || a.id).join(", ")
      : "N/A";
  document.getElementById("validate-seats").textContent = seatsStr;

  // Status badge
  const statusEl = document.getElementById("validate-status");
  if (ticket.estado === "canjeado") {
    statusEl.textContent = "✓ Canjeado";
    statusEl.style.color = "var(--lime)";
    document.getElementById("btn-redeem").disabled = true;
    document.getElementById("btn-redeem").textContent = "✓ Ya fue canjeado";
  } else {
    statusEl.textContent = "● Activo";
    statusEl.style.color = "var(--lime)";
    document.getElementById("btn-redeem").disabled = false;
    document.getElementById("btn-redeem").innerHTML =
      '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="20 6 9 17 4 12"/></svg>Canjear Entrada';
  }

  found.style.display = "block";
}

function redeemTicket() {
  if (!currentTicketCode) {
    showToast("Error: código no válido", "error");
    return;
  }

  const btn = document.getElementById("btn-redeem");
  btn.disabled = true;
  btn.textContent = "Canjeando...";

  fetch(`/api/canjear-ticket/${currentTicketCode}`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
  })
    .then((res) => res.json())
    .then((data) => {
      if (data.success) {
        document.getElementById("validate-found").style.display = "none";
        document.getElementById("validate-redeemed").style.display = "block";
        showToast("¡Entrada canjeada exitosamente!", "success");

        // Reset form after 3 seconds
        setTimeout(() => {
          resetValidateForm();
        }, 3000);
      } else {
        btn.disabled = false;
        btn.innerHTML =
          '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="20 6 9 17 4 12"/></svg>Canjear Entrada';
        showToast(data.error || "No se pudo canjear", "error");
      }
    })
    .catch((err) => {
      console.error("Error:", err);
      btn.disabled = false;
      btn.innerHTML =
        '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="20 6 9 17 4 12"/></svg>Canjear Entrada';
      showToast("Error al procesar", "error");
    });
}

function resetValidateForm() {
  document.getElementById("validate-code-input").value = "";
  document.getElementById("validate-not-found").style.display = "none";
  document.getElementById("validate-found").style.display = "none";
  document.getElementById("validate-redeemed").style.display = "none";
  currentTicketCode = null;
  currentTicketData = null;
  isAutoRedeeming = false;
  const codeInput = document.getElementById("validate-code-input");
  codeInput.disabled = false;
  codeInput.focus();
}

// Autoformato para código de ticket: TKT-XXXX-XXXXX
function formatTicketCode(input) {
  // Paso 1: Extraer SOLO números y letras, sin nada más
  let rawValue = input.value.replace(/[^0-9A-Za-z]/g, "").toUpperCase();

  // Paso 2: Limitar a máximo 13 caracteres
  rawValue = rawValue.slice(0, 13);

  // Paso 3: Reconstruir formato desde cero
  let result = "TKT-";
  if (rawValue.length > 0) {
    result += rawValue.slice(0, 4); // Primeros 4
  }
  if (rawValue.length > 4) {
    result += "-" + rawValue.slice(4); // Resto con guión
  }

  // Paso 4: Asignar solo si cambió
  if (input.value !== result) {
    input.value = result;
  }
}

/* ════════════════════════════════════════════════════════════════
   QR SCANNER
════════════════════════════════════════════════════════════════ */
let qrScannerActive = false;
let qrScannerStream = null;

function toggleQRScanner() {
  const container = document.getElementById("qr-scanner-container");
  const isOpen = container.style.display !== "none";

  if (isOpen) {
    stopQRScanner();
    container.style.display = "none";
  } else {
    container.style.display = "flex";
    startQRScanner();
  }
}

function startQRScanner() {
  const video = document.getElementById("qr-scanner-video");
  qrScannerActive = true;

  console.log("📹 Iniciando escaneo de cámara...");

  navigator.mediaDevices
    .getUserMedia({ video: { facingMode: "environment" } })
    .then((stream) => {
      console.log("✓ Cámara accedida correctamente");
      console.log("📊 Stream info:", stream.getTracks());
      qrScannerStream = stream;
      video.srcObject = stream;
      video.play();
      scanQRFrame();
    })
    .catch((err) => {
      console.error("✗ Error accediendo a cámara:", err);
      showToast("No se pudo acceder a la cámara", "error");
      toggleQRScanner();
    });
}

function stopQRScanner() {
  qrScannerActive = false;
  if (qrScannerStream) {
    qrScannerStream.getTracks().forEach((track) => track.stop());
    qrScannerStream = null;
  }
}

function scanQRFrame() {
  if (!qrScannerActive) return;

  const video = document.getElementById("qr-scanner-video");
  const canvas = document.createElement("canvas");
  const ctx = canvas.getContext("2d");

  canvas.width = video.videoWidth;
  canvas.height = video.videoHeight;

  if (canvas.width > 0 && canvas.height > 0) {
    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
    const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
    const code = jsQR(imageData.data, imageData.width, imageData.height);

    if (code) {
      const qrData = code.data.trim().toUpperCase();
      console.log("✓ QR detectado:", qrData);
      console.log("📊 Datos del QR:", code);

      // Validar que sea un código de ticket (más flexible)
      if (qrData.includes("TKT-")) {
        console.log("✓ Formato válido de ticket");
        stopQRScanner();
        document.getElementById("qr-scanner-container").style.display = "none";
        document.getElementById("validate-code-input").value = qrData;
        console.log(
          "📍 Código QR detectado, validando y canjeando automáticamente:",
          qrData,
        );
        // Buscar, validar y canjear automáticamente
        setTimeout(() => searchAndAutoRedeem(qrData), 500);
      } else {
        console.log("⚠️ QR leído pero no es un ticket:", qrData);
      }
    } else {
      console.log("🔍 Escaneando... (sin QR detectado aún)");
    }
  } else {
    console.log("⚠️ Video no tiene dimensiones:", canvas.width, canvas.height);
  }

  // Continuar escaneando
  requestAnimationFrame(scanQRFrame);
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
      const movie = appData.movies.find((m) => m.id === mId);
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
