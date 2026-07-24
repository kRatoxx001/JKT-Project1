const form = document.querySelector("#moodForm");
const input = document.querySelector("#feelingInput");
const trackList = document.querySelector("#trackList");
const emotionDisc = document.querySelector("#emotionDisc");
const emotionLabel = document.querySelector("#emotionLabel");
const emotionSummary = document.querySelector("#emotionSummary");
const confidenceValue = document.querySelector("#confidenceValue");
const confidenceMeter = document.querySelector("#confidenceMeter");
const playlistTitle = document.querySelector("#playlistTitle");
const savePlaylist = document.querySelector("#savePlaylist");
const connectSpotify = document.querySelector("#connectSpotify");
const generateButton = document.querySelector(".generate-button");
let currentPlaylist = null;

const fallbackPlaylists = {
  joy: {
    summary: "Upbeat, bright tracks with high valence and enough momentum to keep the good mood moving.",
    tracks: [
      ["Golden Hour Drive", "NOVA Lane", "happy pop", 94],
      ["Skyline Lift", "The North Signal", "dance pop", 89],
      ["Good News Static", "Mira Vale", "indie pop", 84],
    ],
  },
  sadness: {
    summary: "Soft acoustic and warm low-tempo tracks for comfort without making the room heavier.",
    tracks: [
      ["Late Bloom", "Aster Theory", "acoustic", 91],
      ["Window Weather", "Mira Vale", "soft indie", 86],
      ["Quiet Return", "NOVA Lane", "piano calm", 81],
    ],
  },
  anger: {
    summary: "High-energy rock and focused beats to let pressure move without losing control.",
    tracks: [
      ["Static Run", "The North Signal", "alt rock", 92],
      ["Redline Reset", "Aster Theory", "rock", 88],
      ["Fuse Break", "NOVA Lane", "workout rock", 83],
    ],
  },
  fear: {
    summary: "Calm, grounded tracks with lower tempo and smoother textures to help regulate the moment.",
    tracks: [
      ["Steady Lights", "Mira Vale", "calm", 93],
      ["Soft Landing", "Aster Theory", "ambient pop", 87],
      ["Small Horizon", "NOVA Lane", "chill", 82],
    ],
  },
  love: {
    summary: "Warm romantic tracks with gentle rhythm and intimate vocals.",
    tracks: [
      ["Soft Static", "Mira Vale", "romantic", 93],
      ["Close Enough", "Aster Theory", "r&b", 87],
      ["Bloom Signal", "The North Signal", "warm pop", 82],
    ],
  },
  surprise: {
    summary: "Playful, varied tracks with a little bounce and unexpected movement.",
    tracks: [
      ["Bright Detour", "NOVA Lane", "party", 91],
      ["Turn the Corner", "The North Signal", "funk pop", 86],
      ["Lift Off", "Aster Theory", "electropop", 82],
    ],
  },
  neutral: {
    summary: "Balanced recommendations that can work while studying, commuting, or resetting.",
    tracks: [
      ["Middle Distance", "Mira Vale", "chill pop", 86],
      ["Clean Slate", "NOVA Lane", "focus", 82],
      ["Low Sun", "Aster Theory", "indie", 78],
    ],
  },
};

const emotionColors = {
  joy: ["#1ed760", "#f5b84b"],
  sadness: ["#69a7ff", "#d7c8a7"],
  anger: ["#ff796c", "#f5b84b"],
  fear: ["#78f0b2", "#69a7ff"],
  love: ["#ff796c", "#d7c8a7"],
  surprise: ["#f5b84b", "#78f0b2"],
  neutral: ["#a9adb7", "#78f0b2"],
};

const keywordEmotion = [
  ["anger", ["angry", "frustrated", "annoyed", "irritated", "mad", "rage"]],
  ["sadness", ["sad", "lonely", "low", "down", "depressed", "heartbroken", "tired"]],
  ["fear", ["anxious", "afraid", "scared", "worried", "nervous", "panic"]],
  ["joy", ["happy", "excited", "great", "good", "energetic", "joy"]],
  ["love", ["love", "romantic", "grateful", "warm", "close"]],
  ["surprise", ["surprised", "shocked", "amazed", "curious"]],
];

function detectEmotionLocally(text) {
  const normalized = text.toLowerCase();
  const match = keywordEmotion.find(([, words]) => words.some((word) => normalized.includes(word)));
  const emotion = match?.[0] ?? "neutral";
  return {
    emotion,
    confidence: emotion === "neutral" ? 0.62 : 0.86,
    source: "local preview",
  };
}

async function generatePlaylist(text) {
  try {
    const response = await fetch("http://localhost:8000/api/music/generate-playlist", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text }),
    });

    if (!response.ok) {
      throw new Error("Backend unavailable");
    }

    return response.json();
  } catch {
    const detected = detectEmotionLocally(text);
    const playlist = fallbackPlaylists[detected.emotion] ?? fallbackPlaylists.neutral;
    return {
      ...detected,
      playlist_name: `${capitalize(detected.emotion)} Reset Mix`,
      summary: playlist.summary,
      tracks: playlist.tracks.map(([title, artist, mood, match]) => ({ title, artist, mood, match })),
    };
  }
}

function renderPlaylist(result) {
  const emotion = result.emotion?.toLowerCase() ?? "neutral";
  const colors = emotionColors[emotion] ?? emotionColors.neutral;
  const confidence = Math.round((result.confidence ?? 0.7) * 100);

  emotionDisc.textContent = emotion.slice(0, 1).toUpperCase();
  emotionDisc.style.background = `linear-gradient(135deg, ${colors[0]}, ${colors[1]})`;
  emotionLabel.textContent = capitalize(emotion);
  emotionSummary.textContent = result.summary;
  confidenceValue.textContent = `${confidence}%`;
  confidenceMeter.style.width = `${confidence}%`;
  confidenceMeter.style.background = `linear-gradient(90deg, ${colors[0]}, ${colors[1]})`;
  playlistTitle.textContent = result.playlist_name;
  savePlaylist.disabled = false;
  savePlaylist.textContent = result.spotify_enabled ? "Save to Spotify" : "Connect Spotify first";
  currentPlaylist = result;

  trackList.innerHTML = "";
  result.tracks.forEach((track, index) => {
    const row = document.createElement("article");
    row.className = "track-row";
    row.innerHTML = `
      <div class="track-art" style="background: linear-gradient(135deg, ${colors[0]}, ${colors[1]});">
        <span>${index + 1}</span>
      </div>
      <div>
        <strong>${track.title}</strong>
        <span>${track.artist} · ${track.mood}</span>
      </div>
      <em>${track.match}%</em>
    `;
    trackList.append(row);
  });
}

function capitalize(value) {
  return `${value.charAt(0).toUpperCase()}${value.slice(1)}`;
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  const text = input.value.trim();

  if (!text) {
    input.focus();
    return;
  }

  generateButton.disabled = true;
  generateButton.textContent = "Detecting emotion...";

  const result = await generatePlaylist(text);
  renderPlaylist(result);

  generateButton.disabled = false;
  generateButton.textContent = "Generate playlist";
});

document.querySelectorAll(".quick-prompts button").forEach((button) => {
  button.addEventListener("click", () => {
    input.value = button.textContent;
    input.focus();
  });
});

savePlaylist.addEventListener("click", async () => {
  if (!currentPlaylist) return;

  const trackUris = currentPlaylist.tracks
    .map(track => track.spotify_uri)
    .filter(Boolean);

  console.log("Track URIs:", trackUris);

  if (!trackUris.length) {
    alert("No Spotify tracks found.");
    return;
  }

  savePlaylist.disabled = true;
  savePlaylist.textContent = "Saving...";

  try {
    const response = await fetch(
      "http://127.0.0.1:8000/api/music/save-playlist",
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          name: currentPlaylist.playlist_name,
          description: currentPlaylist.summary,
          track_uris: trackUris,
        }),
      }
    );

    const payload = await response.json();

    console.log(payload);

    if (!response.ok) {
      throw new Error(payload.detail || "Failed to save playlist");
    }

    savePlaylist.textContent = "Saved to Spotify";

    if (payload.external_url) {
      window.open(payload.external_url, "_blank");
    }

  } catch (err) {
    console.error(err);
    alert(err.message);

    savePlaylist.textContent = "Save to Spotify";
  } finally {
    savePlaylist.disabled = false;
  }
});