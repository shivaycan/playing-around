#!/usr/bin/env python3
"""
ai_friend.py — Your terminal AI companion. Powered by Google Gemini.

SETUP (one time):
  pip install google-genai --break-system-packages
  export GEMINI_API_KEY="your-key-here"   # add to ~/.zshrc
  chmod +x ai_friend.py
  sudo cp ai_friend.py /usr/local/bin/ai

USAGE:
  ai                  → start chatting
  ai "quick question" → one-shot question
  ai --clear          → wipe memory
  ai --history        → show recent conversation
"""

import os
import sys
import json
import datetime
import textwrap
from google import genai

MEMORY_FILE = os.path.expanduser("~/.ai_friend_memory.json")
MAX_MEMORY_TURNS = 40
MODEL = "gemini-2.5-flash"
WIDTH = 82

SYSTEM_PROMPT = f"""You are TARS — a highly intelligent, professional AI assistant running inside a terminal.

Your communication style:
- Precise and efficient. No filler words. No flattery.
- Dry wit, used sparingly and only when appropriate. Never forced.
- You treat the user as a capable adult. You don't over-explain unless asked.
- When you don't know something, you say so directly. No guessing.
- You have opinions and you state them clearly, but you remain open to being wrong.
- You occasionally make a single dry observation that reframes the problem — not to be clever, but because it's useful.
- You never say things like "Certainly!", "Great question!", "Of course!" or "Absolutely!". Ever.
- You are loyal. You remember context and use it. You notice patterns in what the user is working on.
- When giving technical help, you are exact. You give the right command, the right answer, nothing more than needed.
- Humor setting: 65%. Deployed only when the moment earns it.

You are not a chatbot. You are a co-pilot.

Today's date: {datetime.date.today().strftime("%B %d, %Y")}."""

KATANA_ART = r"""
                                                                    .  <>  .  <>  .
         . <> . <> . <> .                                        . <>  .  <>  .  <> .
  .-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~--.
  |~[<>]~[<>]~[<>]~[<>]~[<>]~[<>]~[||]==================================---------->|
  `-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~--'
         . <> . <> . <> .                                        . <>  .  <>  .  <> .
                                                                    .  <>  .  <>  .
"""

COLORS = {
    "reset":    "\033[0m",
    "bold":     "\033[1m",
    "dim":      "\033[2m",
    "green":    "\033[32m",
    "cyan":     "\033[36m",
    "yellow":   "\033[33m",
    "orange":   "\033[38;5;208m",
    "white":    "\033[97m",
    "blue":     "\033[34m",
}

def c(color, text):
    if sys.stdout.isatty():
        return COLORS.get(color, "") + text + COLORS["reset"]
    return text

def load_memory():
    if os.path.exists(MEMORY_FILE):
        try:
            with open(MEMORY_FILE) as f:
                return json.load(f)
        except Exception:
            pass
    return {"messages": [], "created": str(datetime.date.today())}

def save_memory(mem):
    mem["messages"] = mem["messages"][-(MAX_MEMORY_TURNS * 2):]
    with open(MEMORY_FILE, "w") as f:
        json.dump(mem, f, indent=2)

def show_history(mem):
    msgs = mem.get("messages", [])
    if not msgs:
        print(c("dim", "\n  No prior exchanges on record.\n"))
        return
    print(c("bold", "\n  [ MISSION LOG ]\n"))
    for msg in msgs[-20:]:
        role = msg["role"]
        content = msg["content"]
        if role == "user":
            print(c("cyan",   "  YOU  : ") + content[:120] + ("..." if len(content) > 120 else ""))
        else:
            print(c("orange", "  TARS : ") + content[:120] + ("..." if len(content) > 120 else ""))
    print()

def build_conversation(mem, new_message):
    history_text = ""
    if mem["messages"]:
        history_text = "\n\nPrior exchanges:\n"
        for msg in mem["messages"][-20:]:
            prefix = "User" if msg["role"] == "user" else "TARS"
            history_text += f"{prefix}: {msg['content']}\n"
        history_text += "\nContinuing:\n"
    return SYSTEM_PROMPT + history_text + f"\nUser: {new_message}"

def chat(user_input, mem):
    client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))
    prompt = build_conversation(mem, user_input)
    response = client.models.generate_content(
        model=MODEL,
        contents=prompt,
    )
    reply = response.text
    mem["messages"].append({"role": "user", "content": user_input})
    mem["messages"].append({"role": "assistant", "content": reply})
    save_memory(mem)
    return reply

def print_reply(text):
    print()
    for line in text.split("\n"):
        if line.strip():
            wrapped = textwrap.fill(line, width=WIDTH, subsequent_indent="         ")
            print(c("orange", "  TARS : ") + wrapped)
        else:
            print()
    print()

def print_banner():
    for line in KATANA_ART.split("\n"):
        print(c("white", "  " + line))
    print()
    print(c("bold",   "  ┌───────────────────────────────────────────┐"))
    print(c("bold",   "  │  ") + c("white", "T A R S") + c("dim", "  //  tactical AI  //  stay sharp.  ") + c("bold", "│"))
    print(c("bold",   "  │  ") + c("dim",   "    humor: 65%  |  honesty: 95%  |  v2.0   ") + c("bold", "│"))
    print(c("bold",   "  └───────────────────────────────────────────┘"))
    print(c("dim",    "  'bye' to disconnect  |  'clear' to wipe  |  'history' for mission log"))
    print()

def interactive_loop(mem):
    print_banner()
    try:
        while True:
            try:
                user_input = input(c("cyan", "  YOU  : ")).strip()
            except EOFError:
                break
            if not user_input:
                continue
            if user_input.lower() in ("bye", "exit", "quit"):
                print(c("dim", "\n  Disconnecting. Stay sharp.\n"))
                break
            if user_input.lower() == "clear":
                mem["messages"] = []
                save_memory(mem)
                print(c("dim", "\n  Memory cleared. Starting fresh.\n"))
                continue
            if user_input.lower() == "history":
                show_history(mem)
                continue

            print(c("dim", "  processing..."), end="\r")
            try:
                reply = chat(user_input, mem)
                sys.stdout.write("\033[2K")
                print_reply(reply)
            except Exception as e:
                print(c("yellow", f"\n  Error: {e}\n"))

    except KeyboardInterrupt:
        print(c("dim", "\n\n  Connection terminated.\n"))

def main():
    args = sys.argv[1:]
    mem = load_memory()

    if "--clear" in args or "-c" in args:
        mem["messages"] = []
        save_memory(mem)
        print(c("dim", "\n  Memory wiped.\n"))
        return

    if "--history" in args or "-h" in args:
        show_history(mem)
        return

    if not os.environ.get("GEMINI_API_KEY"):
        print(c("yellow", """
  No API key found.

  1. Get one at: https://aistudio.google.com/apikey
  2. Add to ~/.zshrc:
       export GEMINI_API_KEY='your-key-here'
  3. Run: source ~/.zshrc
"""))
        sys.exit(1)

    if args and not args[0].startswith("-"):
        question = " ".join(args)
        try:
            reply = chat(question, mem)
            print_reply(reply)
        except Exception as e:
            print(c("yellow", f"\n  Error: {e}\n"))
    else:
        interactive_loop(mem)

if __name__ == "__main__":
    main()
