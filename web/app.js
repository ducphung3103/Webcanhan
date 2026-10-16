/**
 * ICPC & Olympic Tin Học Sinh Viên Progress Tracker & Knowledge Hub
 * Specially tailored for DeruckLoveNewTechnology
 * Handles: 7-Week Training Schedule, A2OJ Ladder 16, 137 Hard Forgotten Problems, and Tricks.
 */

// Application State
const state = {
  data: {
    schedule: [],
    ladder16: [],
    old_hard_problems: [],
    tricks: [],
    exercises: [],
    materials: [],
    roadmap_nodes: [],
    accounts: {},
    projects: [],
    stats: {}
  },
  activeTab: "schedule", // Default to the 7-Week Training Schedule!
  
  // Schedule Filters
  scheduleFilters: {
    week: "ALL",
    type: "ALL"
  },
  completedSchedule: new Set(JSON.parse(localStorage.getItem("cp_completed_schedule") || "[]")),
  completedProblems: new Set(JSON.parse(localStorage.getItem("cp_completed_problems") || "[]")),

  // Ladder 16 Filters
  ladderFilters: {
    status: "ALL", // ALL, REVIEW, UNSOLVED, SOLVED
    diff: "ALL",
    search: ""
  },
  completedLadder: new Set(JSON.parse(localStorage.getItem("cp_completed_ladder") || "[]")),

  // Hard Problems Filters
  hardFilters: {
    topic: "ALL",
    priority: "ALL",
    days: "ALL",
    sortBy: "rating-desc",
    search: ""
  },
  completedHard: new Set(JSON.parse(localStorage.getItem("cp_completed_hard") || "[]")),

  // Exercise Library Filters
  filters: {
    search: "",
    topic: "ALL",
    platform: "ALL",
    difficulty: "ALL",
    sortBy: "rating-desc",
    page: 1,
    pageSize: 30
  },

  // Tricks Filters
  trickFilter: "ALL",
  trickSearch: "",

  expandedTopics: new Set(),
  solvedProblems: new Set(JSON.parse(localStorage.getItem("cp_solved_problems") || "[]")),
  completedRoadmap: new Set(JSON.parse(localStorage.getItem("cp_completed_roadmap") || "[]")),
  dataSource: "checking..."
};

// DOM Elements
const el = {
  syncBadge: document.getElementById("sync-badge"),
  statSolvedCf: document.getElementById("stat-solved-cf"),
  statLadderProgress: document.getElementById("stat-ladder-progress"),
  statHardReview: document.getElementById("stat-hard-review"),
  statScheduleProgress: document.getElementById("stat-schedule-progress"),
  statSchedulePct: document.getElementById("stat-schedule-pct"),
  
  // Containers
  scheduleContainer: document.getElementById("schedule-container"),
  ladder16Container: document.getElementById("ladder16-container"),
  hardContainer: document.getElementById("hard-container"),
  tricksContainer: document.getElementById("tricks-container"),
  roadmapContainer: document.getElementById("roadmap-container"),
  exercisesContainer: document.getElementById("exercises-container"),
  statsContainer: document.getElementById("stats-container"),
  
  // Filters for exercises
  searchInput: document.getElementById("search-input"),
  platformSelect: document.getElementById("platform-select"),
  difficultySelect: document.getElementById("difficulty-select"),
  sortSelect: document.getElementById("sort-select"),
  topicChipsContainer: document.getElementById("topic-chips"),
  paginationContainer: document.getElementById("pagination-container"),
  problemCountText: document.getElementById("problem-count-text")
};

// ==========================================
// DATA INITIALIZATION & DUAL FETCHING
// ==========================================
async function initApp() {
  setupEventListeners();

  try {
    showSyncStatus("syncing", "Đang tải dữ liệu...");
    const cacheBuster = `?_t=${Date.now()}`;
    const res = await fetch(`./data/data.json${cacheBuster}`, {
      cache: "no-store",
      headers: { "Cache-Control": "no-cache", "Pragma": "no-cache" }
    });
    if (!res.ok) throw new Error(`HTTP error ${res.status}`);
    const json = await res.json();

    state.data.schedule = json.schedule || [];
    state.data.ladder16 = json.ladder16 || [];
    state.data.old_hard_problems = json.old_hard_problems || [];
    state.data.tricks = json.tricks || [];
    state.data.exercises = json.exercises || [];
    state.data.materials = json.materials || [];
    state.data.roadmap_nodes = json.roadmap_nodes || [];
    state.data.accounts = json.accounts || {};
    state.data.projects = json.projects || [];
    state.data.stats = json.stats || {};
    state.dataSource = "static";
    showSyncStatus("live", "🟢 Dữ liệu Đã Cập Nhật");

    // Initialize local solved set
    state.data.exercises.forEach(p => {
      if (p.solved) state.solvedProblems.add(p.id || p.url);
    });

    onDataLoaded();
  } catch (err) {
    console.error("[App] Failed to load data snapshot:", err);
    showSyncStatus("error", "⚠️ Không tải được data.json");
  }
}

function onDataLoaded() {
  updateHeroStats();
  renderTabContent();
  renderExercisesFilters();
}

function updateHeroStats() {
  const stats = state.data.stats || {};
  if (el.statSolvedCf) el.statSolvedCf.textContent = stats.total_cf_solved || 614;
  if (el.statLadderProgress) {
    el.statLadderProgress.textContent = `${stats.ladder16_solved || 70} / ${stats.ladder16_total || 100}`;
  }
  if (el.statHardReview) el.statHardReview.textContent = stats.hard_review_count || 137;
  
  // Schedule problem completion (224 problems across 8 weeks)
  const totalScheduleProbs = state.data.schedule.reduce((acc, d) => acc + (d.problems ? d.problems.length : 1), 0) || 224;
  const completedProbsCount = state.completedProblems.size;
  const pct = Math.round((completedProbsCount / totalScheduleProbs) * 100);
  if (el.statScheduleProgress) el.statScheduleProgress.textContent = `${completedProbsCount} / ${totalScheduleProbs}`;
  if (el.statSchedulePct) el.statSchedulePct.textContent = `${pct}% hoàn thành (Target: 4-5 bài/ngày)`;

  // Dynamic countdowns based on today (2026-10-16)
  const today = new Date("2026-10-16T00:00:00");
  const diffDays = (targetStr) => {
    const target = new Date(targetStr);
    const diffTime = target - today;
    return Math.ceil(diffTime / (1000 * 60 * 60 * 24));
  };

  const elSouth = document.getElementById("countdown-south");
  if (elSouth) {
    const d = diffDays("2026-10-17T00:00:00");
    elSouth.textContent = d <= 0 ? "Hôm nay!" : (d === 1 ? "Ngày mai!" : `${d} Ngày`);
  }

  const elNat = document.getElementById("countdown-national");
  if (elNat) {
    const d = diffDays("2026-11-08T00:00:00");
    elNat.textContent = `${d} Ngày`;
  }

  const elOlp = document.getElementById("countdown-olp");
  if (elOlp) {
    const d = diffDays("2026-12-09T00:00:00");
    elOlp.textContent = `${d} Ngày`;
  }

  const elIcpc = document.getElementById("countdown-icpc");
  if (elIcpc) {
    const d = diffDays("2026-12-11T00:00:00");
    elIcpc.textContent = `${d} Ngày`;
  }
}

function showSyncStatus(type, label) {
  if (!el.syncBadge) return;
  const colors = {
    syncing: "bg-amber-500/10 text-amber-400 border-amber-500/20",
    live: "bg-emerald-500/10 text-emerald-400 border-emerald-500/20",
    static: "bg-indigo-500/10 text-indigo-400 border-indigo-500/20",
    error: "bg-rose-500/10 text-rose-400 border-rose-500/20"
  };
  el.syncBadge.className = `hidden sm:inline-flex items-center px-3 py-1 rounded-full text-xs font-mono border ${colors[type] || colors.static}`;
  el.syncBadge.innerHTML = `<span class="w-2 h-2 mr-2 rounded-full ${type === 'error' ? 'bg-rose-400' : 'bg-emerald-400'} animate-pulse"></span> ${label}`;
}

window.resetCache = async function() {
  try {
    showSyncStatus("syncing", "Làm mới dữ liệu...");
    await initApp();
    showToast("✅ Đã tải dữ liệu mới nhất thành công!");
  } catch (e) {
    console.error("Error during resetCache:", e);
    showToast("⚠️ Có lỗi khi làm mới dữ liệu.", "error");
  }
};

function showToast(message, type = "success") {
  const existing = document.getElementById("app-toast");
  if (existing) existing.remove();

  const toast = document.createElement("div");
  toast.id = "app-toast";
  toast.className = `fixed bottom-6 right-6 z-50 px-4 py-3 rounded-2xl text-xs font-semibold text-white shadow-2xl backdrop-blur-xl border transition-all duration-300 transform translate-y-0 ${
    type === "error" ? "bg-rose-900/90 border-rose-500/50" : "bg-emerald-900/90 border-emerald-500/50"
  }`;
  toast.innerHTML = `<div class="flex items-center gap-2 font-mono"><span>${message}</span></div>`;
  document.body.appendChild(toast);

  setTimeout(() => {
    toast.style.opacity = "0";
    toast.style.transform = "translateY(10px)";
    setTimeout(() => toast.remove(), 300);
  }, 3500);
}

// ==========================================
// EVENT LISTENERS & TAB MANAGEMENT
// ==========================================
function setupEventListeners() {
  document.querySelectorAll(".tab-btn").forEach(btn => {
    btn.addEventListener("click", () => {
      document.querySelectorAll(".tab-btn").forEach(b => {
        b.classList.remove("active", "text-white");
        b.classList.add("text-slate-400");
      });
      btn.classList.add("active", "text-white");
      btn.classList.remove("text-slate-400");

      state.activeTab = btn.getAttribute("data-tab");
      renderTabContent();
    });
  });

  if (el.searchInput) {
    el.searchInput.addEventListener("input", (e) => {
      state.filters.search = e.target.value.toLowerCase().trim();
      state.filters.page = 1;
      renderExercises();
    });
  }

  if (el.platformSelect) {
    el.platformSelect.addEventListener("change", (e) => {
      state.filters.platform = e.target.value;
      state.filters.page = 1;
      renderExercises();
    });
  }

  if (el.difficultySelect) {
    el.difficultySelect.addEventListener("change", (e) => {
      state.filters.difficulty = e.target.value;
      state.filters.page = 1;
      renderExercises();
    });
  }

  if (el.sortSelect) {
    el.sortSelect.addEventListener("change", (e) => {
      state.filters.sortBy = e.target.value;
      renderExercises();
    });
  }
}

function renderTabContent() {
  const tabs = ["schedule", "ladder16", "hard", "tricks", "roadmap", "exercises", "stats"];
  tabs.forEach(t => {
    const pane = document.getElementById(`tab-pane-${t}`);
    if (pane) {
      pane.style.display = (state.activeTab === t) ? "block" : "none";
    }
  });

  if (state.activeTab === "schedule") renderSchedule();
  else if (state.activeTab === "ladder16") renderLadder16();
  else if (state.activeTab === "hard") renderHardProblems();
  else if (state.activeTab === "tricks") renderTricks();
  else if (state.activeTab === "roadmap") renderRoadmap();
  else if (state.activeTab === "exercises") renderExercises();
  else if (state.activeTab === "stats") renderStats();
}

// ==========================================
// 📅 TAB 1: LỊCH HUẤN LUYỆN 7 TUẦN (SCHEDULE)
// ==========================================
function renderSchedule() {
  if (!el.scheduleContainer) return;
  const items = state.data.schedule || [];
  if (!items.length) {
    el.scheduleContainer.innerHTML = `<div class="text-center py-12 text-slate-500 font-mono">Đang tải lịch trình huấn luyện...</div>`;
    return;
  }

  // Filter items
  let filtered = items.filter(item => {
    if (state.scheduleFilters.week !== "ALL" && String(item.week_num) !== String(state.scheduleFilters.week)) return false;
    if (state.scheduleFilters.type === "mock" && !item.session_type.includes("MOCK")) return false;
    if (state.scheduleFilters.type === "olp" && !item.session_type.includes("OLP") && !item.session_type.includes("Mini")) return false;
    if (state.scheduleFilters.type === "resolve" && !item.session_type.includes("Re-solve")) return false;
    return true;
  });

  // Calculate overall & week problem progress
  const totalProblems = items.reduce((acc, d) => acc + (d.problems ? d.problems.length : 1), 0);
  const completedProblemsCount = state.completedProblems.size;
  const pct = Math.round((completedProblemsCount / totalProblems) * 100);

  // Group by week
  const weeks = {};
  filtered.forEach(it => {
    if (!weeks[it.week_num]) weeks[it.week_num] = { theme: it.week_theme, days: [] };
    weeks[it.week_num].days.push(it);
  });

  let html = `
    <!-- Top Filter Controls -->
    <div class="glass-card rounded-2xl p-5 mb-6 border border-slate-800">
      <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h2 class="text-lg font-bold text-white flex items-center gap-2">
            📅 Kế Hoạch 8 Tuần Huấn Luyện Cường Độ Cao (Master 2107)
            <span class="text-xs px-2.5 py-0.5 rounded-full bg-indigo-500/20 text-indigo-300 font-mono">17/10 - 11/12/2026 (Chung kết OLP & ICPC)</span>
          </h2>
          <p class="text-xs text-slate-400 mt-1">
            Mỗi ngày được thiết kế <strong>4 phiên bài tập có mục tiêu rõ ràng</strong> (Speed Warm-up, Core ICPC, OLP Decisive, Mastery Re-solve). Bạn có thể tích checkbox từng bài hoặc tích cả ngày.
          </p>
        </div>
        <div class="flex items-center gap-2">
          <span class="text-xs font-mono text-slate-300">Tiến độ bài tập: <strong class="text-emerald-400 font-bold">${completedProblemsCount}/${totalProblems}</strong> (${pct}%)</span>
        </div>
      </div>

      <!-- Overall Progress Bar -->
      <div class="w-full bg-slate-950 rounded-full h-3 mt-4 border border-slate-800/80 overflow-hidden">
        <div class="bg-gradient-to-r from-indigo-500 via-emerald-500 to-amber-500 h-3 rounded-full transition-all duration-500" style="width: ${pct}%"></div>
      </div>

      <!-- Filter Buttons Row -->
      <div class="flex items-center gap-2 mt-4 overflow-x-auto pb-1 scrollbar-none flex-wrap">
        <span class="text-xs text-slate-500 font-mono mr-1">Lọc Tuần:</span>
        <button onclick="setScheduleWeek('ALL')" class="px-3 py-1 rounded-lg text-xs font-medium transition-colors ${state.scheduleFilters.week === 'ALL' ? 'bg-indigo-600 text-white font-semibold' : 'bg-slate-900 text-slate-400 hover:text-white border border-slate-800'}">Tất cả</button>
        ${[1,2,3,4,5,6,7,8].map(w => `
          <button onclick="setScheduleWeek('${w}')" class="px-3 py-1 rounded-lg text-xs font-medium transition-colors ${state.scheduleFilters.week === String(w) ? 'bg-indigo-600 text-white font-semibold' : 'bg-slate-900 text-slate-400 hover:text-white border border-slate-800'}">Tuần ${w}</button>
        `).join('')}

        <span class="text-xs text-slate-500 font-mono ml-3 mr-1">Loại hình:</span>
        <button onclick="setScheduleType('ALL')" class="px-3 py-1 rounded-lg text-xs font-medium transition-colors ${state.scheduleFilters.type === 'ALL' ? 'bg-amber-600 text-white font-semibold' : 'bg-slate-900 text-slate-400 hover:text-white border border-slate-800'}">Tất cả</button>
        <button onclick="setScheduleType('mock')" class="px-3 py-1 rounded-lg text-xs font-medium transition-colors ${state.scheduleFilters.type === 'mock' ? 'bg-rose-600 text-white font-semibold' : 'bg-slate-900 text-slate-400 hover:text-white border border-slate-800'}">🔥 Mock Test 5h</button>
        <button onclick="setScheduleType('olp')" class="px-3 py-1 rounded-lg text-xs font-medium transition-colors ${state.scheduleFilters.type === 'olp' ? 'bg-violet-600 text-white font-semibold' : 'bg-slate-900 text-slate-400 hover:text-white border border-slate-800'}">🏆 OLP Mock</button>
        <button onclick="setScheduleType('resolve')" class="px-3 py-1 rounded-lg text-xs font-medium transition-colors ${state.scheduleFilters.type === 'resolve' ? 'bg-emerald-600 text-white font-semibold' : 'bg-slate-900 text-slate-400 hover:text-white border border-slate-800'}">🧠 Re-solve Bài Cũ</button>
      </div>
    </div>

    <!-- Weeks Timeline Cards -->
    <div class="space-y-6">
  `;

  Object.keys(weeks).forEach(wNum => {
    const w = weeks[wNum];
    const wTotalProbs = w.days.reduce((acc, d) => acc + (d.problems ? d.problems.length : 1), 0);
    const wDoneProbs = w.days.reduce((acc, d) => acc + (d.problems ? d.problems.filter(p => state.completedProblems.has(p.id)).length : 0), 0);
    const wPct = Math.round((wDoneProbs / wTotalProbs) * 100);

    html += `
      <div class="glass-card rounded-2xl p-5 border border-slate-800">
        <!-- Week Header -->
        <div class="flex flex-col sm:flex-row sm:items-center justify-between pb-4 mb-4 border-b border-slate-800/80 gap-2">
          <div>
            <span class="text-xs px-2.5 py-0.5 rounded-full bg-indigo-500/20 text-indigo-300 font-mono font-medium">Tuần ${wNum}</span>
            <h3 class="text-base font-bold text-white mt-1">${w.theme}</h3>
          </div>
          <div class="flex items-center gap-3">
            <span class="text-xs font-mono text-slate-400">${wDoneProbs}/${wTotalProbs} bài AC (${wPct}%)</span>
            <div class="w-24 bg-slate-950 rounded-full h-2 border border-slate-800 overflow-hidden">
              <div class="bg-emerald-500 h-2 rounded-full" style="width: ${wPct}%"></div>
            </div>
          </div>
        </div>

        <!-- Days Grid -->
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-3 2xl:grid-cols-4 gap-4">
    `;

    w.days.forEach(d => {
      const itemKey = `${d.date}_${d.day_name}`;
      const dayProbs = d.problems || [];
      const dayDoneCount = dayProbs.filter(p => state.completedProblems.has(p.id)).length;
      const isDayDone = (dayProbs.length > 0 && dayDoneCount === dayProbs.length) || state.completedSchedule.has(itemKey);
      const isContestDay = d.session_type.includes("CONTEST") || d.session_type.includes("MOCK");
      const isResolveDay = d.session_type.includes("Re-solve") || d.session_type.includes("UPSOLV");

      let cardBorder = isDayDone ? "border-emerald-500/50 bg-emerald-950/15" : 
        (isContestDay ? "border-rose-500/40 bg-rose-950/10" : 
        (isResolveDay ? "border-amber-500/30 bg-slate-900/80" : "border-slate-800 bg-slate-900/60"));

      html += `
        <div class="rounded-xl border ${cardBorder} p-4 flex flex-col justify-between hover:border-slate-700 transition-all relative">
          <div>
            <!-- Date & Badges -->
            <div class="flex items-center justify-between mb-2">
              <span class="text-xs font-mono text-slate-300 font-bold">${d.date} (${d.day_name})</span>
              <div class="flex items-center gap-1">
                <span class="text-[10px] font-mono px-2 py-0.5 rounded-full ${
                  isContestDay ? 'bg-rose-500/20 text-rose-300 border border-rose-500/30' : 
                  (isResolveDay ? 'bg-amber-500/20 text-amber-300 border border-amber-500/30' : 'bg-slate-800 text-slate-300')
                }">${d.session_type}</span>
                <span class="text-[10px] font-mono px-1.5 py-0.5 rounded-full bg-indigo-500/20 text-indigo-300 font-bold">🎯 ${dayProbs.length} bài</span>
              </div>
            </div>

            <!-- Activity Description -->
            <p class="text-xs text-slate-300 mb-3 leading-relaxed font-medium">${d.activity}</p>

            <!-- 4-Problem Interactive List -->
            <div class="space-y-2 mb-3">
              ${dayProbs.map((p, pIdx) => {
                const pKey = p.id || `${itemKey}_p${pIdx}`;
                const isProbDone = state.completedProblems.has(pKey) || isDayDone;
                const slotStr = String(p.slot || "");
                const isContestProb = slotStr.includes("CONTEST") || slotStr.includes("MOCK");
                const isMasteryProb = slotStr.includes("Mastery") || slotStr.includes("Re-solve") || String(p.tag || "").includes("Re-solve");
                const isSpeedProb = slotStr.includes("Speed") || slotStr.includes("Warm-up");

                let badgeColor = isContestProb ? 'bg-rose-500/20 text-rose-300 border-rose-500/30' :
                  (isMasteryProb ? 'bg-amber-500/20 text-amber-300 border-amber-500/30' :
                  (isSpeedProb ? 'bg-sky-500/20 text-sky-300 border-sky-500/30' : 'bg-indigo-500/20 text-indigo-300 border-indigo-500/30'));

                const slotTag = slotStr.split(':')[0] || "Bài tập";

                return `
                  <div class="p-2.5 rounded-lg border ${isProbDone ? 'border-emerald-500/40 bg-emerald-950/25' : 'border-slate-800/90 bg-slate-950/70'} flex items-start justify-between gap-2 transition-all">
                    <div class="flex-1 min-w-0">
                      <div class="flex items-center gap-1.5 flex-wrap mb-1">
                        <span class="text-[9px] font-mono px-1.5 py-0.2 rounded border ${badgeColor} font-semibold">${slotTag}</span>
                        ${p.rating ? `<span class="text-[9px] font-mono px-1.5 py-0.2 rounded bg-slate-800 text-amber-400 font-bold">${p.rating}</span>` : ''}
                        ${p.time_est && p.time_est !== '0m' ? `<span class="text-[9px] font-mono text-slate-400">⏱ ${p.time_est}</span>` : ''}
                      </div>
                      <a href="${p.url}" target="_blank" rel="noopener noreferrer" class="text-xs font-semibold ${isProbDone ? 'text-emerald-400 line-through' : 'text-slate-200 hover:text-indigo-400'} underline line-clamp-1 transition-colors block">
                        🔗 ${p.name}
                      </a>
                      ${p.tag ? `<span class="text-[10px] text-slate-400 mt-0.5 line-clamp-1 block italic">${p.tag}</span>` : ''}
                    </div>
                    <input type="checkbox" onchange="toggleScheduleProblem('${pKey}', '${itemKey}')" ${isProbDone ? 'checked' : ''} class="w-4 h-4 mt-1 rounded border-slate-700 bg-slate-900 text-emerald-500 focus:ring-0 cursor-pointer" title="Đánh dấu đã AC bài này">
                  </div>
                `;
              }).join("")}
            </div>
          </div>

          <!-- Bottom Checkbox Toggle -->
          <div class="pt-2 border-t border-slate-800/60 flex items-center justify-between">
            <span class="text-[11px] ${isDayDone ? 'text-emerald-400 font-semibold' : 'text-slate-400'} font-mono">
              ${isDayDone ? '✅ Đã hoàn thành ngày' : `⏳ Đã giải ${dayDoneCount}/${dayProbs.length} bài`}
            </span>
            <label class="cursor-pointer inline-flex items-center gap-1.5 text-xs text-slate-400 hover:text-white">
              <input type="checkbox" onchange="toggleScheduleItem('${itemKey}')" ${isDayDone ? 'checked' : ''} class="w-4 h-4 rounded border-slate-700 bg-slate-800 text-indigo-600 focus:ring-0 cursor-pointer">
              <span>Cả ngày</span>
            </label>
          </div>
        </div>
      `;
    });

    html += `
        </div>
      </div>
    `;
  });

  html += `</div>`;
  el.scheduleContainer.innerHTML = html;
}

window.setScheduleWeek = function(w) {
  state.scheduleFilters.week = w;
  renderSchedule();
};

window.setScheduleType = function(t) {
  state.scheduleFilters.type = t;
  renderSchedule();
};

window.toggleScheduleProblem = function(pKey, dayKey) {
  if (state.completedProblems.has(pKey)) {
    state.completedProblems.delete(pKey);
    state.completedSchedule.delete(dayKey);
  } else {
    state.completedProblems.add(pKey);
    const dayItem = state.data.schedule.find(d => `${d.date}_${d.day_name}` === dayKey);
    if (dayItem && dayItem.problems) {
      const allDone = dayItem.problems.every(p => state.completedProblems.has(p.id));
      if (allDone) state.completedSchedule.add(dayKey);
    }
  }
  localStorage.setItem("cp_completed_problems", JSON.stringify([...state.completedProblems]));
  localStorage.setItem("cp_completed_schedule", JSON.stringify([...state.completedSchedule]));
  updateHeroStats();
  renderSchedule();
};

window.toggleScheduleItem = function(key) {
  const dayItem = state.data.schedule.find(d => `${d.date}_${d.day_name}` === key);
  if (state.completedSchedule.has(key)) {
    state.completedSchedule.delete(key);
    if (dayItem && dayItem.problems) {
      dayItem.problems.forEach(p => state.completedProblems.delete(p.id));
    }
  } else {
    state.completedSchedule.add(key);
    if (dayItem && dayItem.problems) {
      dayItem.problems.forEach(p => state.completedProblems.add(p.id));
    }
  }
  localStorage.setItem("cp_completed_schedule", JSON.stringify([...state.completedSchedule]));
  localStorage.setItem("cp_completed_problems", JSON.stringify([...state.completedProblems]));
  updateHeroStats();
  renderSchedule();
};

// ==========================================
// 🧗 TAB 2: LADDER 16 TRACKER (1700 - 1799)
// ==========================================
function renderLadder16() {
  if (!el.ladder16Container) return;
  const problems = state.data.ladder16 || [];
  if (!problems.length) {
    el.ladder16Container.innerHTML = `<div class="text-center py-12 text-slate-500 font-mono">Đang tải Ladder 16...</div>`;
    return;
  }

  // Filter problems
  let filtered = problems.filter(p => {
    if (state.ladderFilters.status === "REVIEW" && !p.review_needed) return false;
    if (state.ladderFilters.status === "UNSOLVED" && p.solved) return false;
    if (state.ladderFilters.status === "SOLVED" && !p.solved) return false;
    if (state.ladderFilters.diff !== "ALL" && String(p.diff_level) !== String(state.ladderFilters.diff)) return false;
    if (state.ladderFilters.search) {
      const q = state.ladderFilters.search.toLowerCase();
      const matchName = (p.name || "").toLowerCase().includes(q);
      const matchKey = (p.key || "").toLowerCase().includes(q);
      const matchTags = (p.tags || []).join(" ").toLowerCase().includes(q);
      if (!matchName && !matchKey && !matchTags) return false;
    }
    return true;
  });

  const total = problems.length;
  const solvedCount = problems.filter(p => p.solved).length;
  const reviewCount = problems.filter(p => p.review_needed).length;
  const unsolvedCount = total - solvedCount;
  const pct = Math.round((solvedCount / total) * 100);

  let html = `
    <!-- Top Stats & Alert Box -->
    <div class="glass-card rounded-2xl p-5 mb-6 border border-slate-800">
      <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h2 class="text-lg font-bold text-white flex items-center gap-2">
            🧗 A2OJ Ladder 16 (1700 &le; Rating &le; 1799)
            <span class="text-xs px-2.5 py-0.5 rounded-full bg-amber-500/20 text-amber-300 font-mono">Handle: DeruckLoveNewTechnology</span>
          </h2>
          <p class="text-xs text-slate-400 mt-1">
            Đã giải <strong>${solvedCount}/${total}</strong> bài (${pct}%). Còn <strong>${unsolvedCount}</strong> bài chưa làm.
          </p>
        </div>
        <div class="text-right">
          <span class="text-xs font-mono text-amber-400 font-bold">⚠️ ${reviewCount} bài giải từ &ge; 2 tháng trước cần Re-solve</span>
        </div>
      </div>

      <!-- Progress Bar -->
      <div class="w-full bg-slate-950 rounded-full h-3 mt-4 border border-slate-800 overflow-hidden">
        <div class="bg-gradient-to-r from-amber-500 to-emerald-500 h-3 rounded-full" style="width: ${pct}%"></div>
      </div>

      <!-- Critical 8-Problem Alert Banner -->
      <div class="mt-4 p-4 rounded-xl bg-amber-950/30 border border-amber-500/40 text-amber-200 text-xs leading-relaxed flex items-start gap-3">
        <span class="text-lg">⚠️</span>
        <div>
          <strong class="font-bold text-amber-300">Lưu ý then chốt từ hệ thống phân tích:</strong>
          Có <strong>${reviewCount} bài quan trọng</strong> trong Ladder 16 bạn đã giải từ rất lâu (2023 - giữa 2024) như 
          <em>Greg and Graph (1700), Password (1700), Lucky Common Subsequence (2000), The Child and Sequence (2300), Tree Requests (2200)</em>.
          Hãy lọc mục <strong>"Cần Ôn Lại"</strong> và giải lại độc lập để phục hồi phản xạ code!
        </div>
      </div>

      <!-- Filters & Search Toolbar -->
      <div class="grid grid-cols-1 sm:grid-cols-12 gap-3 mt-5">
        <div class="sm:col-span-5 relative">
          <input type="text" id="ladder-search-input" value="${state.ladderFilters.search}" placeholder="Tìm theo tên bài, ID (e.g. 295B), tag..." 
                 oninput="setLadderSearch(this.value)"
                 class="w-full pl-9 pr-3 py-2 rounded-xl bg-slate-900 border border-slate-800 text-xs text-white placeholder-slate-500 focus:outline-none focus:border-amber-500">
          <span class="absolute left-3 top-2.5 text-slate-500 text-xs">🔍</span>
        </div>

        <div class="sm:col-span-7 flex items-center gap-2 overflow-x-auto pb-1 scrollbar-none flex-wrap">
          <button onclick="setLadderStatus('ALL')" class="px-3 py-1.5 rounded-lg text-xs font-medium ${state.ladderFilters.status === 'ALL' ? 'bg-amber-600 text-white font-semibold' : 'bg-slate-900 text-slate-400 border border-slate-800'}">Tất cả (${total})</button>
          <button onclick="setLadderStatus('REVIEW')" class="px-3 py-1.5 rounded-lg text-xs font-bold ${state.ladderFilters.status === 'REVIEW' ? 'bg-rose-600 text-white' : 'bg-rose-950/50 text-rose-300 border border-rose-500/30'}">⚠️ Cần Ôn Lại (${reviewCount})</button>
          <button onclick="setLadderStatus('UNSOLVED')" class="px-3 py-1.5 rounded-lg text-xs font-medium ${state.ladderFilters.status === 'UNSOLVED' ? 'bg-slate-700 text-white' : 'bg-slate-900 text-slate-400 border border-slate-800'}">⏳ Chưa làm (${unsolvedCount})</button>
          <button onclick="setLadderStatus('SOLVED')" class="px-3 py-1.5 rounded-lg text-xs font-medium ${state.ladderFilters.status === 'SOLVED' ? 'bg-emerald-600 text-white' : 'bg-slate-900 text-slate-400 border border-slate-800'}">✅ Đã làm (${solvedCount})</button>
        </div>
      </div>
    </div>

    <!-- Problems Grid / Table -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
  `;

  filtered.forEach(p => {
    const isDone = p.solved;
    const isReview = p.review_needed;
    const isLocalChecked = state.completedLadder.has(String(p.ladder_idx));

    let cardBorder = isReview ? "border-amber-500/50 bg-amber-950/15" : (isDone ? "border-emerald-500/40 bg-emerald-950/10" : "border-slate-800 bg-slate-900/60");

    html += `
      <div class="rounded-xl border ${cardBorder} p-4 flex flex-col justify-between hover:border-slate-600 transition-all">
        <div>
          <!-- Header ID & Diff -->
          <div class="flex items-center justify-between mb-2">
            <span class="text-xs font-mono font-bold text-slate-400">#${p.ladder_idx} [${p.key || 'CF'}]</span>
            <div class="flex items-center gap-1.5">
              <span class="text-[10px] font-mono px-2 py-0.5 rounded bg-slate-800 text-slate-300">Mức ${p.diff_level}</span>
              ${p.rating ? `<span class="text-[10px] font-mono px-2 py-0.5 rounded bg-amber-500/20 text-amber-300 font-bold">${p.rating}</span>` : ''}
            </div>
          </div>

          <!-- Problem Name & Link -->
          <h4 class="text-sm font-bold text-white mb-1.5 line-clamp-1">
            <a href="${p.url}" target="_blank" rel="noopener noreferrer" class="hover:text-amber-400 transition-colors flex items-center gap-1">
              <span>${p.name}</span>
              <span class="text-xs text-slate-500">↗</span>
            </a>
          </h4>

          <!-- Tags -->
          <div class="flex flex-wrap gap-1 mb-3">
            ${(p.tags || []).slice(0, 3).map(t => `<span class="text-[10px] px-1.5 py-0.5 rounded bg-slate-800/80 text-slate-400">${t}</span>`).join('')}
          </div>
        </div>

        <!-- Status & Re-solve Indicator -->
        <div class="pt-3 border-t border-slate-800/80 flex items-center justify-between">
          <div class="flex flex-col">
            ${isReview ? `
              <span class="text-[11px] font-bold text-amber-400 font-mono">⚠️ Cần Ôn Lại</span>
              <span class="text-[10px] text-slate-500">Làm từ: ${p.last_sub ? p.last_sub.split(' ')[0] : 'N/A'}</span>
            ` : (isDone ? `
              <span class="text-[11px] font-semibold text-emerald-400 font-mono">✅ Đã giải</span>
              <span class="text-[10px] text-slate-500">Gần đây</span>
            ` : `
              <span class="text-[11px] font-medium text-slate-500 font-mono">⏳ Chưa làm</span>
            `)}
          </div>

          <label class="cursor-pointer inline-flex items-center gap-1.5 text-xs text-slate-400 hover:text-white">
            <input type="checkbox" onchange="toggleLadderItem('${p.ladder_idx}')" ${isLocalChecked ? 'checked' : ''} class="w-4 h-4 rounded border-slate-700 bg-slate-800 text-amber-600 focus:ring-0 cursor-pointer">
            <span class="text-[11px]">Re-solve</span>
          </label>
        </div>
      </div>
    `;
  });

  html += `</div>`;
  el.ladder16Container.innerHTML = html;
}

window.setLadderStatus = function(s) {
  state.ladderFilters.status = s;
  renderLadder16();
};

window.setLadderSearch = function(val) {
  state.ladderFilters.search = val.trim();
  renderLadder16();
};

window.toggleLadderItem = function(idx) {
  if (state.completedLadder.has(idx)) {
    state.completedLadder.delete(idx);
  } else {
    state.completedLadder.add(idx);
  }
  localStorage.setItem("cp_completed_ladder", JSON.stringify([...state.completedLadder]));
  renderLadder16();
};

// ==========================================
// 🧠 TAB 3: 137 BÀI KHÓ ĐÃ QUÊN (HARD REVIEW)
// ==========================================
function renderHardProblems() {
  if (!el.hardContainer) return;
  const problems = state.data.old_hard_problems || [];
  if (!problems.length) {
    el.hardContainer.innerHTML = `<div class="text-center py-12 text-slate-500 font-mono">Đang tải danh sách bài khó...</div>`;
    return;
  }

  // Filter
  let filtered = problems.filter(p => {
    if (state.hardFilters.topic !== "ALL" && p.topic !== state.hardFilters.topic) return false;
    if (state.hardFilters.priority !== "ALL" && !p.priority.includes(state.hardFilters.priority)) return false;
    if (state.hardFilters.days === "180" && p.days_ago < 180) return false;
    if (state.hardFilters.days === "365" && p.days_ago < 365) return false;
    if (state.hardFilters.days === "700" && p.days_ago < 700) return false;
    if (state.hardFilters.search) {
      const q = state.hardFilters.search.toLowerCase();
      const matchName = (p.name || "").toLowerCase().includes(q);
      const matchKey = (p.key || "").toLowerCase().includes(q);
      const matchTags = (p.tags || []).join(" ").toLowerCase().includes(q);
      if (!matchName && !matchKey && !matchTags) return false;
    }
    return true;
  });

  // Sort
  if (state.hardFilters.sortBy === "rating-desc") {
    filtered.sort((a, b) => b.rating - a.rating);
  } else if (state.hardFilters.sortBy === "rating-asc") {
    filtered.sort((a, b) => a.rating - b.rating);
  } else if (state.hardFilters.sortBy === "days-desc") {
    filtered.sort((a, b) => b.days_ago - a.days_ago);
  }

  const total = problems.length;
  const reSolvedCount = state.completedHard.size;
  const pct = Math.round((reSolvedCount / total) * 100);

  // Topics set
  const topics = ["ALL", "Tree", "Graph Theory", "Dynamic Programming", "Data Structures", "Mathematics", "Geometry & Sweepline", "Strings", "Game Theory & Adhoc"];

  let html = `
    <!-- Top Header & Filter Controls -->
    <div class="glass-card rounded-2xl p-5 mb-6 border border-slate-800">
      <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h2 class="text-lg font-bold text-white flex items-center gap-2">
            🧠 137 Bài Khó Đã Giải &ge; 2 Tháng Trước Cần Phục Hồi Kiến Thức
            <span class="text-xs px-2.5 py-0.5 rounded-full bg-rose-500/20 text-rose-300 font-mono">Rating 1600 - 2800</span>
          </h2>
          <p class="text-xs text-slate-400 mt-1">
            Các bài tập bạn đã từng giải thành công nhưng chưa từng đụng lại trong hơn 60 ngày. Đây là mỏ vàng để kích hoạt lại tư duy thuật toán trước ngày thi.
          </p>
        </div>
        <div class="text-right">
          <span class="text-xs font-mono text-emerald-400 font-bold">Tiến độ Re-solve: ${reSolvedCount}/${total} bài (${pct}%)</span>
        </div>
      </div>

      <!-- Progress Bar -->
      <div class="w-full bg-slate-950 rounded-full h-3 mt-4 border border-slate-800 overflow-hidden">
        <div class="bg-gradient-to-r from-rose-500 via-amber-500 to-emerald-500 h-3 rounded-full" style="width: ${pct}%"></div>
      </div>

      <!-- Filters Row -->
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-12 gap-3 mt-5">
        <!-- Search Input -->
        <div class="lg:col-span-4 relative">
          <input type="text" value="${state.hardFilters.search}" placeholder="Tìm mã bài (e.g. 986E), tên bài, tags..." 
                 oninput="setHardSearch(this.value)"
                 class="w-full pl-9 pr-3 py-2 rounded-xl bg-slate-900 border border-slate-800 text-xs text-white placeholder-slate-500 focus:outline-none focus:border-indigo-500">
          <span class="absolute left-3 top-2.5 text-slate-500 text-xs">🔍</span>
        </div>

        <!-- Topic Select -->
        <div class="lg:col-span-3">
          <select onchange="setHardTopic(this.value)" class="w-full px-3 py-2 rounded-xl bg-slate-900 border border-slate-800 text-xs text-slate-300 focus:outline-none focus:border-indigo-500">
            ${topics.map(t => `<option value="${t}" ${state.hardFilters.topic === t ? 'selected' : ''}>${t === 'ALL' ? 'Tất cả Chủ đề' : t}</option>`).join('')}
          </select>
        </div>

        <!-- Priority Select -->
        <div class="lg:col-span-3">
          <select onchange="setHardPriority(this.value)" class="w-full px-3 py-2 rounded-xl bg-slate-900 border border-slate-800 text-xs text-slate-300 focus:outline-none focus:border-indigo-500">
            <option value="ALL">Tất cả Mức ưu tiên</option>
            <option value="P1" ${state.hardFilters.priority === 'P1' ? 'selected' : ''}>P1 - Trọng tâm ICPC/OLP (1800-2300)</option>
            <option value="P2" ${state.hardFilters.priority === 'P2' ? 'selected' : ''}>P2 - Master/TST (2400-2800)</option>
            <option value="P3" ${state.hardFilters.priority === 'P3' ? 'selected' : ''}>P3 - Luyện phản xạ (1600-1700)</option>
          </select>
        </div>

        <!-- Sort Select -->
        <div class="lg:col-span-2">
          <select onchange="setHardSort(this.value)" class="w-full px-3 py-2 rounded-xl bg-slate-900 border border-slate-800 text-xs text-slate-300 focus:outline-none focus:border-indigo-500">
            <option value="rating-desc" ${state.hardFilters.sortBy === 'rating-desc' ? 'selected' : ''}>Rating: Cao &rarr; Thấp</option>
            <option value="rating-asc" ${state.hardFilters.sortBy === 'rating-asc' ? 'selected' : ''}>Rating: Thấp &rarr; Cao</option>
            <option value="days-desc" ${state.hardFilters.sortBy === 'days-desc' ? 'selected' : ''}>Ngày chưa làm: Lâu nhất</option>
          </select>
        </div>
      </div>
      
      <div class="text-xs text-slate-400 font-mono mt-3">
        Hiển thị <strong>${filtered.length}</strong> / ${total} bài phù hợp.
      </div>
    </div>

    <!-- Cards Grid -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
  `;

  filtered.forEach(p => {
    const isDone = state.completedHard.has(p.key);
    
    // Rating color
    let rColor = "bg-blue-500/20 text-blue-300 border-blue-500/30";
    if (p.rating >= 2400) rColor = "bg-rose-500/25 text-rose-300 border-rose-500/40 font-black";
    else if (p.rating >= 2100) rColor = "bg-amber-500/20 text-amber-300 border-amber-500/40 font-bold";
    else if (p.rating >= 1900) rColor = "bg-purple-500/20 text-purple-300 border-purple-500/30 font-bold";

    html += `
      <div class="rounded-xl border ${isDone ? 'border-emerald-500/40 bg-emerald-950/10' : 'border-slate-800 bg-slate-900/60'} p-4 flex flex-col justify-between hover:border-slate-700 transition-all">
        <div>
          <!-- Header -->
          <div class="flex items-center justify-between mb-2">
            <span class="text-xs font-mono font-bold text-slate-400">CF-${p.key}</span>
            <span class="text-xs font-mono px-2 py-0.5 rounded-full border ${rColor}">
              Rating: ${p.rating}
            </span>
          </div>

          <!-- Title -->
          <h4 class="text-sm font-bold text-white mb-2 line-clamp-1">
            <a href="${p.url}" target="_blank" rel="noopener noreferrer" class="hover:text-indigo-400 transition-colors flex items-center gap-1">
              <span>${p.name}</span>
              <span class="text-xs text-slate-500">↗</span>
            </a>
          </h4>

          <!-- Topic & Priority -->
          <div class="flex items-center gap-1.5 mb-2 flex-wrap">
            <span class="text-[10px] font-mono px-2 py-0.5 rounded bg-indigo-500/15 text-indigo-300 border border-indigo-500/20">${p.topic}</span>
            <span class="text-[10px] font-mono px-2 py-0.5 rounded bg-slate-800 text-slate-400">${p.priority.split(' - ')[0]}</span>
          </div>

          <!-- Tags -->
          <div class="flex flex-wrap gap-1 mb-3">
            ${(p.tags || []).slice(0, 4).map(t => `<span class="text-[10px] px-1.5 py-0.5 rounded bg-slate-800/80 text-slate-400">${t}</span>`).join('')}
          </div>
        </div>

        <!-- Days & Checkbox -->
        <div class="pt-3 border-t border-slate-800/80 flex items-center justify-between">
          <div class="flex flex-col">
            <span class="text-[11px] font-mono text-amber-400/90 font-medium">⏳ Chưa đụng: ${p.days_ago} ngày</span>
            <span class="text-[10px] text-slate-500">Lần cuối: ${p.last_sub ? p.last_sub.split(' ')[0] : 'N/A'}</span>
          </div>

          <label class="cursor-pointer inline-flex items-center gap-1.5 text-xs text-slate-400 hover:text-white">
            <input type="checkbox" onchange="toggleHardItem('${p.key}')" ${isDone ? 'checked' : ''} class="w-4 h-4 rounded border-slate-700 bg-slate-800 text-emerald-600 focus:ring-0 cursor-pointer">
            <span class="text-[11px] ${isDone ? 'text-emerald-400 font-semibold' : ''}">${isDone ? 'Đã Re-solve' : 'Cần giải'}</span>
          </label>
        </div>
      </div>
    `;
  });

  html += `</div>`;
  el.hardContainer.innerHTML = html;
}

window.setHardSearch = function(val) {
  state.hardFilters.search = val.trim();
  renderHardProblems();
};

window.setHardTopic = function(val) {
  state.hardFilters.topic = val;
  renderHardProblems();
};

window.setHardPriority = function(val) {
  state.hardFilters.priority = val;
  renderHardProblems();
};

window.setHardSort = function(val) {
  state.hardFilters.sortBy = val;
  renderHardProblems();
};

window.toggleHardItem = function(key) {
  if (state.completedHard.has(key)) {
    state.completedHard.delete(key);
  } else {
    state.completedHard.add(key);
  }
  localStorage.setItem("cp_completed_hard", JSON.stringify([...state.completedHard]));
  renderHardProblems();
};

// ==========================================
// ⚡ TAB 4: TRICK LỎ & TEMPLATE NOTE
// ==========================================
function renderTricks() {
  if (!el.tricksContainer) return;
  const tricks = state.data.tricks || [];
  if (!tricks.length) {
    el.tricksContainer.innerHTML = `<div class="text-center py-12 text-slate-500 font-mono">Đang tải trick lỏ...</div>`;
    return;
  }

  let html = `
    <div class="glass-card rounded-2xl p-5 mb-6 border border-slate-800">
      <h2 class="text-lg font-bold text-white flex items-center gap-2">
        ⚡ Tổng Hợp Trick Lỏ, Mẹo Cài Đặt & Chiến Thuật Phòng Thi ICPC
        <span class="text-xs px-2.5 py-0.5 rounded-full bg-amber-500/20 text-amber-300 font-mono">ICPC & OLP Survival Kit</span>
      </h2>
      <p class="text-xs text-slate-400 mt-1">
        Các mẹo giảm độ phức tạp, bẫy tràn số thường gặp, và cách phối hợp 3 người 1 máy để đạt hiệu suất tối đa.
      </p>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
  `;

  tricks.forEach((t, idx) => {
    html += `
      <div class="glass-card rounded-xl p-4 border border-slate-800 hover:border-slate-700 transition-all flex flex-col justify-between">
        <div>
          <div class="flex items-center justify-between mb-2">
            <span class="text-xs font-mono px-2 py-0.5 rounded bg-indigo-500/15 text-indigo-300 border border-indigo-500/20 font-bold">${t.category}</span>
            <span class="text-[10px] font-mono px-2 py-0.5 rounded ${t.priority.includes('Bắt buộc') || t.priority.includes('Cực kỳ') ? 'bg-rose-500/20 text-rose-300 font-bold' : 'bg-slate-800 text-slate-400'}">${t.priority}</span>
          </div>

          <h4 class="text-sm font-bold text-white mb-2 leading-snug">${t.trick}</h4>
          
          <div class="p-2.5 rounded-lg bg-slate-950/80 border border-slate-800/80 mb-3 text-xs font-mono text-amber-300/90 leading-relaxed">
            <span class="text-slate-500 block text-[10px] uppercase font-bold mb-0.5">⚠️ Bẫy cài đặt / Lưu ý:</span>
            ${t.edge_case}
          </div>
        </div>

        ${t.link ? `
          <div class="pt-2 border-t border-slate-800/60 text-right">
            <a href="${t.link}" target="_blank" rel="noopener noreferrer" class="text-xs font-medium text-indigo-400 hover:text-indigo-300 underline transition-colors">
              Xem bài tập ví dụ ↗
            </a>
          </div>
        ` : ''}
      </div>
    `;
  });

  html += `</div>`;
  el.tricksContainer.innerHTML = html;
}

// ==========================================
// 🗺️ TAB 5: ROADMAP (EXISTING)
// ==========================================
function renderRoadmap() {
  if (!el.roadmapContainer) return;
  const nodes = state.data.roadmap_nodes || [];
  if (!nodes.length) {
    el.roadmapContainer.innerHTML = `<div class="text-center py-12 text-slate-500 font-mono">Đang tải Curriculum Roadmap...</div>`;
    return;
  }

  let html = `
    <div class="glass-card rounded-2xl p-5 mb-6 border border-slate-800">
      <h2 class="text-lg font-bold text-white flex items-center gap-2">
        🗺️ Khung Kiến Thức Chuẩn 4 Cấp Độ (VOI / ICPC Curriculum)
        <span class="text-xs px-2.5 py-0.5 rounded-full bg-violet-500/20 text-violet-300 font-mono">Từ New Roadmap.docx</span>
      </h2>
      <p class="text-xs text-slate-400 mt-1">Phân cấp từ BASIC, INTERMEDIATE đến HARD và INSANE.</p>
    </div>
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
  `;

  ["BASIC", "INTERMEDIATE", "HARD", "INSANE"].forEach(tier => {
    const tierNodes = nodes.filter(n => n.tier === tier);
    html += `
      <div class="glass-card rounded-xl p-4 border border-slate-800">
        <h3 class="text-sm font-bold text-white pb-2 mb-3 border-b border-slate-800 flex items-center justify-between">
          <span>Tier [${tier}]</span>
          <span class="text-xs text-slate-400 font-mono">${tierNodes.length} Topics</span>
        </h3>
        <div class="space-y-2 max-h-[600px] overflow-y-auto pr-1">
          ${tierNodes.map(n => `
            <div class="p-2.5 rounded-lg bg-slate-900 border border-slate-800/80 text-xs">
              <strong class="text-slate-200 block mb-1">${n.title}</strong>
              <span class="text-[10px] text-slate-500 font-mono">${n.category}</span>
            </div>
          `).join('')}
        </div>
      </div>
    `;
  });

  html += `</div>`;
  el.roadmapContainer.innerHTML = html;
}

// ==========================================
// 🎯 TAB 6: EXERCISES LIBRARY (EXISTING)
// ==========================================
function renderExercisesFilters() {
  const exercises = state.data.exercises || [];
  if (!el.platformSelect || !exercises.length) return;

  const platforms = new Set();
  const topics = new Set();

  exercises.forEach(ex => {
    if (ex.platform) platforms.add(ex.platform);
    if (ex.tags) {
      ex.tags.forEach(t => topics.add(t));
    }
  });

  el.platformSelect.innerHTML = `<option value="ALL">Tất cả Nền tảng</option>` + 
    Array.from(platforms).sort().map(p => `<option value="${p}">${p}</option>`).join("");

  if (el.topicChipsContainer) {
    el.topicChipsContainer.innerHTML = `<button class="px-3 py-1 rounded-full text-xs font-mono font-medium transition-all ${state.filters.topic === 'ALL' ? 'bg-indigo-600 text-white' : 'bg-slate-900 text-slate-400 hover:text-white border border-slate-800'}" onclick="setExerciseTopic('ALL')">All</button>` +
      Array.from(topics).slice(0, 15).map(t => `
        <button class="px-3 py-1 rounded-full text-xs font-mono font-medium whitespace-nowrap transition-all ${state.filters.topic === t ? 'bg-indigo-600 text-white' : 'bg-slate-900 text-slate-400 hover:text-white border border-slate-800'}" onclick="setExerciseTopic('${t}')">${t}</button>
      `).join("");
  }
}

window.setExerciseTopic = function(t) {
  state.filters.topic = t;
  state.filters.page = 1;
  renderExercisesFilters();
  renderExercises();
};

function renderExercises() {
  if (!el.exercisesContainer) return;
  const exercises = state.data.exercises || [];
  if (!exercises.length) {
    el.exercisesContainer.innerHTML = `<div class="text-center py-12 text-slate-500 font-mono col-span-full">Đang tải danh sách bài tập...</div>`;
    return;
  }

  let filtered = exercises.filter(ex => {
    if (state.filters.platform !== "ALL" && ex.platform !== state.filters.platform) return false;
    if (state.filters.difficulty !== "ALL" && ex.difficulty !== state.filters.difficulty) return false;
    if (state.filters.topic !== "ALL" && !(ex.tags || []).includes(state.filters.topic)) return false;
    if (state.filters.search) {
      const q = state.filters.search.toLowerCase();
      const matchTitle = (ex.title || "").toLowerCase().includes(q);
      const matchId = (ex.id || "").toLowerCase().includes(q);
      const matchNotes = (ex.notes || "").toLowerCase().includes(q);
      if (!matchTitle && !matchId && !matchNotes) return false;
    }
    return true;
  });

  if (el.problemCountText) {
    el.problemCountText.textContent = `Hiển thị ${filtered.length} / ${exercises.length} bài tập.`;
  }

  const start = (state.filters.page - 1) * state.filters.pageSize;
  const pageItems = filtered.slice(start, start + state.filters.pageSize);

  el.exercisesContainer.innerHTML = pageItems.map(p => `
    <div class="glass-card rounded-xl p-4 border border-slate-800 hover:border-slate-700 transition-all flex flex-col justify-between">
      <div>
        <div class="flex items-center justify-between mb-2">
          <span class="text-xs font-mono font-bold text-slate-400">${p.id || 'EX'}</span>
          <span class="text-[10px] font-mono px-2 py-0.5 rounded bg-slate-800 text-slate-300">${p.platform || 'CP'}</span>
        </div>
        <h4 class="text-sm font-bold text-white mb-2 line-clamp-1">
          <a href="${p.url}" target="_blank" rel="noopener noreferrer" class="hover:text-indigo-400 transition-colors">${p.title || p.url}</a>
        </h4>
        <div class="flex flex-wrap gap-1 mb-3">
          ${(p.tags || []).slice(0, 3).map(t => `<span class="text-[10px] px-1.5 py-0.5 rounded bg-slate-800/80 text-slate-400">${t}</span>`).join('')}
        </div>
      </div>
      <div class="pt-2 border-t border-slate-800/80 flex items-center justify-between text-xs">
        <span class="text-amber-400 font-mono font-medium">${p.rating ? `Rating: ${p.rating}` : (p.difficulty || 'Normal')}</span>
        ${p.solved ? '<span class="text-emerald-400 font-semibold">✅ Solved</span>' : '<span class="text-slate-500">Unsolved</span>'}
      </div>
    </div>
  `).join('');
}

// ==========================================
// 📊 TAB 7: STATS (EXISTING)
// ==========================================
function renderStats() {
  if (!el.statsContainer) return;
  const stats = state.data.stats || {};
  el.statsContainer.innerHTML = `
    <div class="grid grid-cols-1 md:grid-cols-3 gap-5">
      <div class="glass-card rounded-2xl p-5 border border-slate-800">
        <h3 class="text-sm font-bold text-white mb-3">Codeforces Submissions</h3>
        <div class="text-3xl font-black font-mono text-emerald-400">${stats.total_cf_solved || 614}</div>
        <p class="text-xs text-slate-400 mt-1">Bài đã AC trên tổng số ${stats.total_cf_submissions || 1553} lượt nộp</p>
      </div>
      <div class="glass-card rounded-2xl p-5 border border-slate-800">
        <h3 class="text-sm font-bold text-white mb-3">Ladder 16 Completion</h3>
        <div class="text-3xl font-black font-mono text-amber-400">${stats.ladder16_solved || 69} / 100</div>
        <p class="text-xs text-slate-400 mt-1">Đạt 69% tiến độ Ladder 16 Codeforces</p>
      </div>
      <div class="glass-card rounded-2xl p-5 border border-slate-800">
        <h3 class="text-sm font-bold text-white mb-3">Hard Problems Needing Review</h3>
        <div class="text-3xl font-black font-mono text-rose-400">${stats.hard_review_count || 137}</div>
        <p class="text-xs text-slate-400 mt-1">Rating 1600 - 2800 giải &ge; 2 tháng trước</p>
      </div>
    </div>
  `;
}

// Start application
document.addEventListener("DOMContentLoaded", initApp);
