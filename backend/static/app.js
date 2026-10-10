/**
 * Universal Media Streaming Platform - Client Application
 */

const API_BASE = window.location.origin;
let currentToken = localStorage.getItem("streamflow_token") || null;
let currentUser = null;
let currentMedia = null;
let isAudio = false;

// DOM Elements
const browseView = document.getElementById("browseView");
const historyView = document.getElementById("historyView");
const hostView = document.getElementById("hostView");
const mediaGrid = document.getElementById("mediaGrid");
const resultsCount = document.getElementById("resultsCount");
const categoryPills = document.getElementById("categoryPills");
const searchInput = document.getElementById("searchInput");

// Host Elements
const hostIpDisplay = document.getElementById("hostIpDisplay");
const serverStatusText = document.getElementById("serverStatusText");
const mediaCountDisplay = document.getElementById("mediaCountDisplay");
const lanUrlBox = document.getElementById("lanUrlBox");
const scanFolderInput = document.getElementById("scanFolderInput");
const startScanBtn = document.getElementById("startScanBtn");
const scanResultBox = document.getElementById("scanResultBox");

// Player Elements
const mainAudioPlayer = document.getElementById("mainAudioPlayer");
const mainVideoPlayer = document.getElementById("mainVideoPlayer");
const videoModal = document.getElementById("videoModal");
const closeVideoModal = document.getElementById("closeVideoModal");
const videoModalToggle = document.getElementById("videoModalToggle");
const modalVideoTitle = document.getElementById("modalVideoTitle");

const nowPlayingTitle = document.getElementById("nowPlayingTitle");
const nowPlayingMeta = document.getElementById("nowPlayingMeta");
const nowPlayingIcon = document.getElementById("nowPlayingIcon");
const playPauseBtn = document.getElementById("playPauseBtn");
const rewindBtn = document.getElementById("rewindBtn");
const forwardBtn = document.getElementById("forwardBtn");
const progressBar = document.getElementById("progressBar");
const currentTimeLabel = document.getElementById("currentTime");
const totalDurationLabel = document.getElementById("totalDuration");
const volumeSlider = document.getElementById("volumeSlider");

// Auth Elements
const authBtn = document.getElementById("authBtn");
const authModal = document.getElementById("authModal");
const closeAuthModal = document.getElementById("closeAuthModal");
const tabLogin = document.getElementById("tabLogin");
const tabRegister = document.getElementById("tabRegister");
const emailGroup = document.getElementById("emailGroup");
const authForm = document.getElementById("authForm");
const authModalTitle = document.getElementById("authModalTitle");
const authSubmitBtn = document.getElementById("authSubmitBtn");
const authErrorMsg = document.getElementById("authErrorMsg");
const userNameDisplay = document.getElementById("userNameDisplay");
const userAvatar = document.getElementById("userAvatar");

let isRegisterMode = false;
let selectedType = "";
let selectedCategory = "";

// ----------------- Initialization -----------------
document.addEventListener("DOMContentLoaded", () => {
  initNavigation();
  fetchHostStatus();
  fetchCategories();
  fetchMedia();
  initPlayerEvents();
  initAuth();
  if (currentToken) {
    checkCurrentUser();
  }
});

// ----------------- Navigation -----------------
function initNavigation() {
  document.querySelectorAll(".nav-item").forEach(btn => {
    btn.addEventListener("click", () => {
      document.querySelectorAll(".nav-item").forEach(b => b.classList.remove("active"));
      document.querySelectorAll(".content-view").forEach(v => v.classList.remove("active"));

      btn.classList.add("active");
      const targetView = btn.getAttribute("data-view");
      if (targetView === "browse") browseView.classList.add("active");
      if (targetView === "history") {
        historyView.classList.add("active");
        fetchHistory();
      }
      if (targetView === "host") hostView.classList.add("active");
    });
  });
}

// ----------------- Host Status & Scanner -----------------
async function fetchHostStatus() {
  try {
    const res = await fetch(`${API_BASE}/api/host/status`);
    if (!res.ok) throw new Error("Server error");
    const data = await res.json();
    serverStatusText.textContent = "Online";
    hostIpDisplay.textContent = `IP: ${data.host_ip}:${data.port}`;
    mediaCountDisplay.textContent = `${data.total_media_count} media files`;
    lanUrlBox.textContent = `http://${data.host_ip}:${data.port}`;
  } catch (err) {
    serverStatusText.textContent = "Disconnected";
    hostIpDisplay.textContent = "IP: 127.0.0.1:8000";
  }
}

startScanBtn.addEventListener("click", async () => {
  const dirPath = scanFolderInput.value.trim();
  if (!dirPath) {
    alert("Please enter a folder path on the host machine.");
    return;
  }
  startScanBtn.disabled = true;
  startScanBtn.textContent = "Scanning...";
  scanResultBox.classList.remove("hidden");
  scanResultBox.textContent = "Scanning directory for media files...";

  try {
    const res = await fetch(`${API_BASE}/api/host/scan`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ directory_path: dirPath })
    });
    const result = await res.json();
    if (result.status === "completed") {
      scanResultBox.textContent = `Scan complete: Found ${result.files_found} files, added ${result.files_added} new items, ${result.already_indexed} already indexed.`;
      fetchHostStatus();
      fetchMedia();
    } else {
      scanResultBox.textContent = `Scan error: ${result.errors.join(", ")}`;
    }
  } catch (err) {
    scanResultBox.textContent = `Request failed: ${err.message}`;
  } finally {
    startScanBtn.disabled = false;
    startScanBtn.textContent = "Scan Folder";
  }
});

// ----------------- Categories & Filter -----------------
async function fetchCategories() {
  try {
    const res = await fetch(`${API_BASE}/api/categories`);
    const categories = await res.json();
    categories.forEach(cat => {
      const btn = document.createElement("button");
      btn.className = "pill";
      btn.textContent = `${cat.category_name} (${cat.media_count})`;
      btn.setAttribute("data-cat-id", cat.category_id);
      btn.addEventListener("click", () => {
        document.querySelectorAll(".pill").forEach(p => p.classList.remove("active"));
        btn.classList.add("active");
        selectedCategory = cat.category_id;
        selectedType = "";
        fetchMedia();
      });
      categoryPills.appendChild(btn);
    });
  } catch (err) {
    console.error("Failed to fetch categories", err);
  }
}

// Category Pills click handlers
categoryPills.querySelectorAll(".pill").forEach(pill => {
  pill.addEventListener("click", () => {
    document.querySelectorAll(".pill").forEach(p => p.classList.remove("active"));
    pill.classList.add("active");
    selectedCategory = "";
    selectedType = pill.getAttribute("data-type") || "";
    fetchMedia();
  });
});

let searchTimeout = null;
searchInput.addEventListener("input", () => {
  clearTimeout(searchTimeout);
  searchTimeout = setTimeout(() => {
    fetchMedia();
  }, 300);
});

// ----------------- Fetch & Render Media -----------------
async function fetchMedia() {
  mediaGrid.innerHTML = `<div class="empty-state">Loading library...</div>`;
  const params = new URLSearchParams();
  if (selectedType) params.append("media_type", selectedType);
  if (selectedCategory) params.append("category_id", selectedCategory);
  if (searchInput.value.trim()) params.append("search", searchInput.value.trim());

  try {
    const res = await fetch(`${API_BASE}/api/media?${params.toString()}`);
    const data = await res.json();
    resultsCount.textContent = `${data.total} items`;

    if (data.items.length === 0) {
      mediaGrid.innerHTML = `<div class="empty-state">No media found. Go to 'Host & Scan' to index files from your disk.</div>`;
      return;
    }

    mediaGrid.innerHTML = "";
    data.items.forEach(item => {
      const card = document.createElement("div");
      card.className = "media-card";
      const icon = item.media_type === "video" ? "🎬" : "🎵";
      const formattedDuration = formatSeconds(item.duration);
      const formattedSize = (item.file_size / (1024 * 1024)).toFixed(1) + " MB";

      card.innerHTML = `
        <div class="media-thumbnail">
          <span>${icon}</span>
          <span class="media-type-badge">${item.media_type}</span>
        </div>
        <div class="media-info">
          <h4 class="media-title" title="${item.title}">${item.title}</h4>
          <div class="media-meta">
            <span>${item.category_name || 'General'}</span>
            <span>${formattedDuration}</span>
          </div>
          <div class="media-meta">
            <small style="color:var(--text-muted)">${formattedSize}</small>
          </div>
        </div>
      `;
      card.addEventListener("click", () => playMedia(item));
      mediaGrid.appendChild(card);
    });
  } catch (err) {
    mediaGrid.innerHTML = `<div class="empty-state">Failed to load media files.</div>`;
  }
}

// ----------------- Player Core -----------------
function playMedia(item, startOffset = 0) {
  currentMedia = item;
  isAudio = item.media_type === "audio";
  const streamUrl = `${API_BASE}/api/media/${item.media_id}/stream`;

  nowPlayingTitle.textContent = item.title;
  nowPlayingMeta.textContent = `${item.media_type.toUpperCase()} • ${item.category_name || "General"}`;
  nowPlayingIcon.textContent = isAudio ? "🎵" : "🎬";

  if (isAudio) {
    mainVideoPlayer.pause();
    videoModal.classList.add("hidden");
    mainAudioPlayer.src = streamUrl;
    if (startOffset > 0) mainAudioPlayer.currentTime = startOffset;
    mainAudioPlayer.play();
  } else {
    mainAudioPlayer.pause();
    mainVideoPlayer.src = streamUrl;
    modalVideoTitle.textContent = item.title;
    if (startOffset > 0) mainVideoPlayer.currentTime = startOffset;
    videoModal.classList.remove("hidden");
    mainVideoPlayer.play();
  }
  playPauseBtn.textContent = "⏸";

  // Record initial history if logged in
  if (currentUser) {
    savePlaybackProgress(item.media_id, startOffset);
  }
}

function getActivePlayer() {
  return isAudio ? mainAudioPlayer : mainVideoPlayer;
}

function initPlayerEvents() {
  [mainAudioPlayer, mainVideoPlayer].forEach(player => {
    player.addEventListener("timeupdate", () => {
      const cur = player.currentTime;
      const dur = player.duration || (currentMedia ? currentMedia.duration : 0);
      currentTimeLabel.textContent = formatSeconds(cur);
      totalDurationLabel.textContent = formatSeconds(dur);
      if (dur > 0) {
        progressBar.value = (cur / dur) * 100;
      }
    });

    player.addEventListener("ended", () => {
      playPauseBtn.textContent = "▶";
      if (currentUser && currentMedia) {
        savePlaybackProgress(currentMedia.media_id, Math.floor(player.duration));
      }
    });

    player.addEventListener("play", () => playPauseBtn.textContent = "⏸");
    player.addEventListener("pause", () => playPauseBtn.textContent = "▶");
  });

  playPauseBtn.addEventListener("click", () => {
    const player = getActivePlayer();
    if (!player.src) return;
    if (player.paused) {
      player.play();
    } else {
      player.pause();
    }
  });

  rewindBtn.addEventListener("click", () => {
    const player = getActivePlayer();
    player.currentTime = Math.max(0, player.currentTime - 10);
  });

  forwardBtn.addEventListener("click", () => {
    const player = getActivePlayer();
    player.currentTime = Math.min(player.duration, player.currentTime + 10);
  });

  progressBar.addEventListener("input", () => {
    const player = getActivePlayer();
    if (player.duration) {
      player.currentTime = (progressBar.value / 100) * player.duration;
    }
  });

  volumeSlider.addEventListener("input", () => {
    const vol = parseFloat(volumeSlider.value);
    mainAudioPlayer.volume = vol;
    mainVideoPlayer.volume = vol;
  });

  videoModalToggle.addEventListener("click", () => {
    if (currentMedia && currentMedia.media_type === "video") {
      videoModal.classList.toggle("hidden");
    }
  });

  closeVideoModal.addEventListener("click", () => {
    videoModal.classList.add("hidden");
  });

  // Periodically sync playback progress every 10s
  setInterval(() => {
    if (currentUser && currentMedia) {
      const player = getActivePlayer();
      if (!player.paused && player.currentTime > 0) {
        savePlaybackProgress(currentMedia.media_id, Math.floor(player.currentTime));
      }
    }
  }, 10000);
}

async function savePlaybackProgress(mediaId, position) {
  if (!currentToken) return;
  try {
    await fetch(`${API_BASE}/api/history`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${currentToken}`
      },
      body: JSON.stringify({ media_id: mediaId, last_position: position })
    });
  } catch (err) {
    console.error("Progress save failed", err);
  }
}

// ----------------- History View -----------------
async function fetchHistory() {
  const historyList = document.getElementById("historyList");
  if (!currentToken) {
    historyList.innerHTML = `<div class="empty-state">Please sign in to view and resume playback history.</div>`;
    return;
  }
  historyList.innerHTML = `<div class="empty-state">Loading history...</div>`;

  try {
    const res = await fetch(`${API_BASE}/api/history`, {
      headers: { "Authorization": `Bearer ${currentToken}` }
    });
    if (!res.ok) throw new Error("Auth error");
    const history = await res.json();

    if (history.length === 0) {
      historyList.innerHTML = `<div class="empty-state">No playback history recorded yet.</div>`;
      return;
    }

    historyList.innerHTML = "";
    history.forEach(item => {
      const el = document.createElement("div");
      el.className = "history-item";
      el.innerHTML = `
        <div>
          <h4>${item.title}</h4>
          <small style="color:var(--text-muted)">Resumed at ${formatSeconds(item.last_position)} • ${new Date(item.played_at).toLocaleString()}</small>
        </div>
        <button class="btn" style="padding: 6px 14px; font-size: 12px;">Resume ▶</button>
      `;
      el.addEventListener("click", () => {
        // Fetch full media item details
        fetch(`${API_BASE}/api/media/${item.media_id}`)
          .then(r => r.json())
          .then(media => playMedia(media, item.last_position));
      });
      historyList.appendChild(el);
    });
  } catch (err) {
    historyList.innerHTML = `<div class="empty-state">Failed to load history.</div>`;
  }
}

// ----------------- Authentication -----------------
function initAuth() {
  authBtn.addEventListener("click", () => {
    if (currentUser) {
      // Logout
      localStorage.removeItem("streamflow_token");
      currentToken = null;
      currentUser = null;
      userNameDisplay.textContent = "Guest User";
      userAvatar.textContent = "U";
      authBtn.textContent = "Sign In";
      return;
    }
    authModal.classList.remove("hidden");
  });

  closeAuthModal.addEventListener("click", () => authModal.classList.add("hidden"));

  tabLogin.addEventListener("click", () => {
    isRegisterMode = false;
    tabLogin.classList.add("active");
    tabRegister.classList.remove("active");
    emailGroup.classList.add("hidden");
    authModalTitle.textContent = "Sign In";
    authSubmitBtn.textContent = "Sign In";
    authErrorMsg.classList.add("hidden");
  });

  tabRegister.addEventListener("click", () => {
    isRegisterMode = true;
    tabRegister.classList.add("active");
    tabLogin.classList.remove("active");
    emailGroup.classList.remove("hidden");
    authModalTitle.textContent = "Register Account";
    authSubmitBtn.textContent = "Create Account";
    authErrorMsg.classList.add("hidden");
  });

  authForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    authErrorMsg.classList.add("hidden");
    const username = document.getElementById("authUsername").value.trim();
    const password = document.getElementById("authPassword").value.trim();
    const email = document.getElementById("authEmail").value.trim();

    const endpoint = isRegisterMode ? `${API_BASE}/api/auth/register` : `${API_BASE}/api/auth/login`;
    const payload = isRegisterMode ? { username, email, password } : { username, password };

    try {
      const res = await fetch(endpoint, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      });
      const data = await res.json();
      if (!res.ok) {
        authErrorMsg.textContent = data.detail || "Authentication error";
        authErrorMsg.classList.remove("hidden");
        return;
      }
      currentToken = data.access_token;
      localStorage.setItem("streamflow_token", currentToken);
      currentUser = data.user;
      userNameDisplay.textContent = currentUser.username;
      userAvatar.textContent = currentUser.username.charAt(0).toUpperCase();
      authBtn.textContent = "Logout";
      authModal.classList.add("hidden");
    } catch (err) {
      authErrorMsg.textContent = err.message;
      authErrorMsg.classList.remove("hidden");
    }
  });
}

async function checkCurrentUser() {
  try {
    const res = await fetch(`${API_BASE}/api/auth/me`, {
      headers: { "Authorization": `Bearer ${currentToken}` }
    });
    if (res.ok) {
      currentUser = await res.json();
      userNameDisplay.textContent = currentUser.username;
      userAvatar.textContent = currentUser.username.charAt(0).toUpperCase();
      authBtn.textContent = "Logout";
    } else {
      localStorage.removeItem("streamflow_token");
      currentToken = null;
    }
  } catch (err) {
    console.error("User validation failed", err);
  }
}

function formatSeconds(sec) {
  if (isNaN(sec) || sec < 0) return "00:00";
  const m = Math.floor(sec / 60);
  const s = Math.floor(sec % 60);
  return `${m.toString().padStart(2, "0")}:${s.toString().padStart(2, "0")}`;
}
