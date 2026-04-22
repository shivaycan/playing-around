# ⚔️ TARS — Terminal AI Friend

```
                                                                    .  <>  .  <>  .
         . <> . <> . <> .                                        . <>  .  <>  .  <> .
  .-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~--.
  |~[<>]~[<>]~[<>]~[<>]~[<>]~[<>]~[||]==================================---------->|
  `-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~--'
         . <> . <> . <> .                                        . <>  .  <>  .  <> .
                                                                    .  <>  .  <>  .

  ┌───────────────────────────────────────────┐
  │  T A R S  //  tactical AI  //  stay sharp.│
  │      humor: 65%  |  honesty: 95%  |  v2.0 │
  └───────────────────────────────────────────┘
```

> *"You are not talking to a chatbot. You are talking to a co-pilot."*

---

## What is this?

A personal AI assistant that lives inside your terminal. Type `ai` anywhere and instantly talk to an intelligent, no-nonsense AI modeled after **TARS from Interstellar** — precise, dry, loyal, and occasionally funny.

Built in one night by **Shivay** as an experiment in understanding how AI apps actually work under the hood.

Powered by **Google Gemini 2.5 Flash** — completely free.

---

## What I learned building this

This started as a simple question: *"can my computer have memory and talk to me?"*

Turns out — yes. And it's simpler than you'd think.

### How AI apps actually work
Every AI app in the world — ChatGPT, Claude, Gemini — is doing exactly this under the hood:
1. Take user message
2. Add conversation history
3. Send everything to an AI model via API
4. Get reply back
5. Save to memory
6. Repeat

That's it. The "magic" is just an API call.

### How terminal commands work
When you type `ai` in the terminal, here's what actually happens:
```
you type "ai"
  → terminal searches PATH folders (/usr/local/bin, /usr/bin, etc.)
    → finds /usr/local/bin/ai
      → reads the shebang line: #!/usr/bin/env python3
        → runs the file with Python
          → TARS boots up ⚔️
```

The `chmod +x` command gives the file permission to be executed. The shebang line tells the terminal which program to use to run it. Copy any script into `/usr/local/bin/` with a name and it becomes a command.

### How memory works
Every conversation is saved to `~/.ai_friend_memory.json` — a simple JSON file on your computer. Each message is stored as a `role` + `content` pair:
```json
{
  "messages": [
    { "role": "user", "content": "hello" },
    { "role": "assistant", "content": "Hello. What do you need?" }
  ]
}
```
On every new message, the script loads this file, appends the new exchange, and saves it back. The AI receives the full history as context — that's how it "remembers" you.

### The security rabbit hole
Halfway through building this, I realized — the same mechanism that makes this work (`PATH` + `shebang` + `chmod +x`) is exactly how malware achieves **persistence** on a system. A malicious script named `git` or `sudo` dropped into an early PATH folder would run silently every time you use those commands.

Security is just understanding the same tools from a different angle.

---

## Setup

**Requirements:**
- Mac or Linux
- Python 3
- A free Google AI Studio account

**Install:**
```bash
# 1. Install the Google Gemini library
pip3 install google-genai --break-system-packages

# 2. Get a free API key at https://aistudio.google.com/apikey
#    Add to ~/.zshrc:
export GEMINI_API_KEY="your-key-here"
source ~/.zshrc

# 3. Install as a global command
chmod +x ai_friend.py
sudo cp ai_friend.py /usr/local/bin/ai
```

**Done. Now just type:**
```bash
ai
```

---

## Usage

```bash
ai                    # start a conversation
ai "quick question"   # one-shot answer, no interactive mode
ai --history          # see past conversations
ai --clear            # wipe memory, fresh start
```

**Inside the chat:**
```
bye       → disconnect
clear     → wipe memory
history   → show mission log
```

---

## The AI's personality

TARS doesn't flatter. TARS doesn't say *"Great question!"*. TARS tells you what you need to know, nothing more.

- **Humor setting: 65%** — deployed only when the moment earns it
- **Honesty setting: 95%** — will tell you when it doesn't know
- Dry wit. Precise answers. Zero filler.

Inspired by TARS from *Interstellar* — the only AI in fiction that feels like a real co-pilot.

---

## Files

| File | What it does |
|------|-------------|
| `ai_friend.py` | The entire AI friend — ~150 lines of Python |
| `~/.ai_friend_memory.json` | Your conversation history (on your Mac, not in this repo) |

---

## Cost

**Free.** Google Gemini 2.5 Flash has a free tier that's more than enough for personal terminal use.

No subscriptions. No credit card. No bills.

---

*Built at 2am by Shivay. Started by asking a simple question, ended up learning how AI, terminals, PATH, memory, and security all connect.*

*"Stay sharp." ⚔️*
