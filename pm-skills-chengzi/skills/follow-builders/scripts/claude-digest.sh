#!/bin/zsh
# Claude-powered digest using the actual skill prompts
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
PROMPTS_DIR="$SKILL_DIR/prompts"
USER_PROMPTS_DIR="${FOLLOW_BUILDERS_HOME:-$HOME/.follow-builders}/prompts"
TMP_JSON="/tmp/fb-prepared.json"
TMP_PROMPT="/tmp/fb-prompt.txt"
TMP_DIGEST="/tmp/fb-claude-digest.md"
LOG="/tmp/fb-digest.log"

echo "[$(date)] Starting Claude digest..." >> "$LOG"
cd "$SCRIPT_DIR"

# Step 1: Fetch content
node prepare-digest.js > "$TMP_JSON" 2>>"$LOG"
echo "[$(date)] prepare done, $(wc -c < $TMP_JSON) bytes" >> "$LOG"

# Step 2: Build full prompt — read prompt files inside Node to avoid shell escaping issues
node -e "
const fs = require('fs');
const path = require('path');

const promptsDir = '$PROMPTS_DIR';
const userPromptsDir = '$USER_PROMPTS_DIR';

function loadPrompt(name) {
  const userFile = path.join(userPromptsDir, name + '.md');
  const defaultFile = path.join(promptsDir, name + '.md');
  if (fs.existsSync(userFile)) return fs.readFileSync(userFile, 'utf8');
  if (fs.existsSync(defaultFile)) return fs.readFileSync(defaultFile, 'utf8');
  return '';
}

const d = JSON.parse(fs.readFileSync('$TMP_JSON', 'utf8'));
const podcasts = d.podcasts || [];
const builders = d.x || [];
const lang = (d.config && d.config.language) || 'zh';

const parts = [];
parts.push('=== YOUR ROLE ===');
parts.push(loadPrompt('digest-intro'));
parts.push('');
parts.push('=== TWEET SUMMARIZATION RULES ===');
parts.push(loadPrompt('summarize-tweets'));
parts.push('');
parts.push('=== PODCAST SUMMARIZATION RULES ===');
parts.push(loadPrompt('summarize-podcast'));
parts.push('');

if (lang === 'zh' || lang === 'bilingual') {
  const translatePrompt = loadPrompt('translate');
  parts.push('=== LANGUAGE ===');
  parts.push('Output language: Chinese (zh).');
  if (translatePrompt) parts.push(translatePrompt);
  parts.push('');
}

parts.push('=== CONTENT TO PROCESS ===');
parts.push('');
parts.push('--- PODCASTS ---');
for (const p of podcasts) {
  parts.push('Name: ' + p.name);
  parts.push('Title: ' + p.title);
  parts.push('URL: ' + p.url);
  parts.push('Transcript:');
  parts.push((p.transcript || '').slice(0, 8000));
  parts.push('');
}

parts.push('--- X / TWITTER ---');
for (const b of builders) {
  const tweets = (b.tweets || []).filter(t => t.url);
  if (!tweets.length) continue;
  parts.push('Handle: ' + b.handle);
  parts.push('Bio: ' + (b.bio || '').slice(0, 150));
  for (const t of tweets) {
    parts.push('Tweet: ' + (t.text || '').slice(0, 400));
    parts.push('URL: ' + t.url);
  }
  parts.push('');
}

parts.push('Now generate the complete digest following all the rules above.');

const out = parts.join('\n');
fs.writeFileSync('$TMP_PROMPT', out);
process.stderr.write('prompt: ' + out.length + ' chars\n');
" 2>>"$LOG"

echo "[$(date)] prompt built, $(wc -c < $TMP_PROMPT) bytes" >> "$LOG"

# Step 3: Claude remixes
/opt/homebrew/bin/claude --print --output-format text < "$TMP_PROMPT" > "$TMP_DIGEST" 2>>"$LOG"
echo "[$(date)] Claude remix done, $(wc -c < $TMP_DIGEST) bytes" >> "$LOG"

# Step 4: Deliver
node deliver.js --file "$TMP_DIGEST" >> "$LOG" 2>&1
echo "[$(date)] Delivered." >> "$LOG"
