# OpenClaw Skill Ideas

## Future Skills & Automations

### 1. Pontic Greek Lyrics & Language Learning
**Status:** Idea - not started

**Description:**
- Input: Spotify playlist with Pontic Greek songs + website with lyrics/translations
- Process: 
  - Extract all songs from playlist
  - Look up each song on the provided lyrics website
  - Extract original Pontic Greek text and any available translations (Greek/partial English)
  - Use AI to decode/translate the Pontic Greek dialect
- Output: Structured learning reports with:
  - Original line in Pontic Greek
  - English translation below each line
  - Word-by-word breakdowns where available

**Related Ideas:**
- Quiz generation for language learning
- Transcription practice exercises
- Interactive teaching/tutoring for Pontic Greek
- Flashcard generation from lyrics

### 2. General Language Learning Tools
**Status:** Idea - not started

**Description:**
- Quizzes based on vocabulary from songs/texts
- Spaced repetition system for new words
- Listening comprehension exercises
- Cultural context notes for songs

### 3. Main Session as Sub-Agent Manager
**Status:** Idea - not started

**Description:**
Work through HEARTBEAT.md, identity files (AGENTS.md, SOUL.md), skills, and scripts to ensure the main session properly delegates to sub-agents and acts as an effective manager.

**Key Behaviors to Enforce:**
- Main session delegates work instead of doing everything itself
- Regular check-ins on sub-agent progress
- Hard enforcement - demand results, no excuses
- Kill and respawn failed/stuck sub-agents immediately
- Track sub-agent tasks in Mission Control
- Main session as intermediary between user (Anthony) and sub-agents
- Teach sub-agents proper work habits through strict oversight

**Files to Review/Update:**
- `HEARTBEAT.md` - sub-agent supervision rules
- `AGENTS.md` - sub-agent spawning and naming rules  
- `SOUL.md` - manager mindset and accountability
- Mission Control scripts - task tracking integration

---

*Last updated: 2026-02-03*
