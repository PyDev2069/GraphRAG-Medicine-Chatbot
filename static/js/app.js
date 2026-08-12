// ===== State =====
let chatHistory = [];     // [{role: "user"|"assistant", content: "..."}]
let isLoading = false;

// ===== Elements =====
const messagesContainer = document.getElementById('messagesContainer');
const userInput         = document.getElementById('userInput');
const sendBtn           = document.getElementById('sendBtn');
const welcomeScreen     = document.getElementById('welcomeScreen');
const themeToggle       = document.getElementById('themeToggle');
const newChatBtn        = document.getElementById('newChatBtn');
const hamburgerBtn      = document.getElementById('hamburgerBtn');
const sidebar           = document.querySelector('.sidebar');
const overlay           = document.getElementById('sidebarOverlay');

// ===== Theme =====
const savedTheme = localStorage.getItem('theme') || 'light';
document.documentElement.setAttribute('data-theme', savedTheme);

themeToggle.addEventListener('click', () => {
  const current = document.documentElement.getAttribute('data-theme');
  const next = current === 'light' ? 'dark' : 'light';
  document.documentElement.setAttribute('data-theme', next);
  localStorage.setItem('theme', next);
});

// ===== Mobile sidebar =====
hamburgerBtn.addEventListener('click', () => {
  sidebar.classList.toggle('open');
  overlay.classList.toggle('visible');
});
overlay.addEventListener('click', () => {
  sidebar.classList.remove('open');
  overlay.classList.remove('visible');
});

// ===== New chat =====
newChatBtn.addEventListener('click', () => {
  chatHistory = [];
  messagesContainer.innerHTML = '';
  messagesContainer.appendChild(welcomeScreen);
  welcomeScreen.style.display = 'flex';
  userInput.value = '';
  autoResize();
  sidebar.classList.remove('open');
  overlay.classList.remove('visible');
});

// ===== Suggestion chips =====
document.querySelectorAll('.suggestion-chip').forEach(chip => {
  chip.addEventListener('click', () => {
    userInput.value = chip.dataset.prompt;
    autoResize();
    sendMessage();
  });
});

// ===== Auto-resize textarea =====
function autoResize() {
  userInput.style.height = 'auto';
  userInput.style.height = Math.min(userInput.scrollHeight, 160) + 'px';
}
userInput.addEventListener('input', autoResize);

// ===== Send on Enter (Shift+Enter = newline) =====
userInput.addEventListener('keydown', (e) => {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault();
    sendMessage();
  }
});
sendBtn.addEventListener('click', sendMessage);

// ===== Core send =====
async function sendMessage() {
  const text = userInput.value.trim();
  if (!text || isLoading) return;

  // Hide welcome
  if (welcomeScreen.style.display !== 'none') {
    welcomeScreen.style.display = 'none';
  }

  // Append user bubble
  appendMessage('user', text);

  // Clear input
  userInput.value = '';
  autoResize();

  // Build history to send (exclude current message, it's sent separately)
  const historyToSend = [...chatHistory];

  // Add to local history
  chatHistory.push({ role: 'user', content: text });

  // Show typing
  const typingEl = appendTyping();
  isLoading = true;
  sendBtn.disabled = true;

  try {
    const res = await fetch('/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        message: text,
        history: historyToSend,
      }),
    });

    const data = await res.json();

    typingEl.remove();

    if (data.error) {
      appendMessage('bot', `⚠️ ${data.error}`);
    } else {
      // Metadata row
      if (data.detected_symptoms?.length || data.matched_conditions?.length) {
        appendMeta(data.detected_symptoms, data.matched_conditions);
      }
      appendMessage('bot', data.reply, true);
      chatHistory.push({ role: 'assistant', content: data.reply });
    }
  } catch (err) {
    typingEl.remove();
    appendMessage('bot', '⚠️ Could not reach the server. Make sure the backend is running.');
  } finally {
    isLoading = false;
    sendBtn.disabled = false;
    userInput.focus();
  }
}

// ===== Append a message bubble =====
function appendMessage(role, text, isMarkdown = false) {
  const row = document.createElement('div');
  row.className = `message-row ${role}`;

  const bubble = document.createElement('div');
  bubble.className = 'message-bubble';

  if (isMarkdown && role === 'bot') {
    bubble.innerHTML = marked.parse(text);
  } else {
    bubble.textContent = text;
  }

  row.appendChild(bubble);
  messagesContainer.appendChild(row);
  scrollToBottom();
  return row;
}

// ===== Append metadata tags =====
function appendMeta(symptoms, conditions) {
  if (!symptoms?.length && !conditions?.length) return;
  const meta = document.createElement('div');
  meta.className = 'message-meta';

  symptoms?.forEach(s => {
    const tag = document.createElement('span');
    tag.className = 'meta-tag';
    tag.textContent = `🔍 ${s}`;
    meta.appendChild(tag);
  });

  conditions?.forEach(c => {
    const tag = document.createElement('span');
    tag.className = 'meta-tag';
    tag.textContent = `📋 ${c}`;
    meta.appendChild(tag);
  });

  messagesContainer.appendChild(meta);
}

// ===== Typing indicator =====
function appendTyping() {
  const row = document.createElement('div');
  row.className = 'message-row bot typing-indicator';
  const bubble = document.createElement('div');
  bubble.className = 'message-bubble';
  bubble.innerHTML = '<div class="dot"></div><div class="dot"></div><div class="dot"></div>';
  row.appendChild(bubble);
  messagesContainer.appendChild(row);
  scrollToBottom();
  return row;
}

function scrollToBottom() {
  messagesContainer.scrollTop = messagesContainer.scrollHeight;
}