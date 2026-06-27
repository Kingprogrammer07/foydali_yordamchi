# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

A Telegram bot ("Foydali yordamchi [PC Mexanics]") built on **aiogram 2.22.2** (Python 3.11.9). It distributes school textbooks and PC software (links to Telegram channel posts), downloads video/media from YouTube/Instagram/TikTok, and gives admins a post-broadcasting + user-management panel. All user-facing text and most comments are in **Uzbek** — match that language when editing strings.

## Commands

```bash
pip install -r requirements.txt   # requirements.txt is UTF-16 encoded; pip handles it, editors may show a BOM
python app.py                     # run the bot (long-polling; no webhook)
python purifier.py                # recursively delete all __pycache__ dirs
```

There are **no tests, linter, or build step**. `runtime.txt` (`python-3.11.9`) targets a Heroku/Railway-style deploy.

## Architecture

**Registration is by import side-effect.** `app.py` does `import middlewares, filters, handlers` — importing each package runs its `__init__.py`, which imports submodules, which run the `@dp.*_handler` decorators that register everything on the shared `dp`. Nothing is wired up explicitly. Consequences:

- **`loader.py` is the single source of `bot`, `dp`, and `storage`** (`MemoryStorage`, HTML parse mode). Every module imports from it. FSM state is in-memory only — a restart drops all in-progress flows.
- **Handler order = match priority.** `handlers/__init__.py` and `handlers/users/__init__.py` control the order handlers are registered. Two near-catch-all handlers exist and order between them is load-bearing: `handlers/users/owner/creator.py` registers `@dp.message_handler(content_types=ContentType.TEXT)` (the giant `elif text == "..."` main-menu router for every reply-keyboard button), and `handlers/users/aks_holda/echo.py` is the final fallback — `echo` is imported **last** in `users/__init__.py` so it only catches unmatched text. Adding a new menu button means adding both a `KeyboardButton` in `keyboards/keyboard/all_button.py` and an `elif` branch in `creator.py`.
- **Middlewares/filters use an unusual guard.** `middlewares/__init__.py` and `filters/__init__.py` only run their setup inside `if __name__ == "middlewares":` / `if __name__ == "filters":`. This works *only because* they are imported as top-level packages named exactly that. Don't relocate or rename these packages, and don't expect the setup to run if imported under another path.

**Force-subscription gate.** `middlewares/checksub.py` (`BigBrother`, `on_pre_process_update`) blocks every update except `/start`, `/help`, and the `check_subs` callback until the user is subscribed to all `CHANNELS`; non-subscribers get invite buttons and the handler is cancelled via `CancelHandler()`. `ThrottlingMiddleware` (`middlewares/throttling.py`) is the standard aiogram anti-flood.

**Data layer.** `data/post_data.py` defines a hand-rolled `Database` wrapper over `sqlite3` and exports a module-level singleton `db` (DB file: `data/database.sqlite3`, resolved relative to that file). Tables:
- `obunachilar` — subscribers (`tg_user`)
- `owner` — admins (`admin`)
- `channels_data` — required-subscription channels (`channel_id`, negative Telegram IDs)
- `for_post` — staged media posts (`admin_id`, `file_id`, `caption`)
- `for_elon` — staged text announcements (`id_raqami`, `elon`)

**Config is read from the DB at import time.** `data/config.py` sets `BOT_TOKEN` (hardcoded) and computes `ADMINS`/`CHANNELS` via `list(*zip(*db.admin_view()))` / `db.channel_view()` when the module is first imported. So `ADMINS`/`CHANNELS` are **snapshots** — admin/channel rows added at runtime are written to the DB but won't appear in these lists until the process restarts. Code that needs live admin checks uses `db.is_admin(...)` directly instead.

**Media downloads.** `handlers/users/yt_insta_tiktok/download.py` routes a pasted URL by prefix to functions in `all_request.py`, which call **RapidAPI** endpoints (Instagram/TikTok/YouTube) with a hardcoded `X-RapidAPI-Key`. `pytube` is used only to normalize a YouTube URL into a `videoId`. Each branch is wrapped in `try/except` that replies with a generic failure message.

## Gotchas

- **Secrets are committed in source**: `BOT_TOKEN` in `data/config.py` and the `X-RapidAPI-Key` in `handlers/users/yt_insta_tiktok/all_request.py`. Treat them as live; don't paste them elsewhere.
- **The new-post flow uses module-level mutable dicts** (`user_entity`, `analiz`, `btn_text`, `tugmalar`) in `handlers/users/yangi_pst/newpost.py` as cross-handler scratch state. These are **global, not per-user** — concurrent admins building posts simultaneously will clobber each other. Per-message data goes through aiogram's `state.proxy()`/`update_data`; this global dict is the post-construction working set.
- **`newpost.py` and `creator.py` swallow exceptions broadly** and DM the admins a hardcoded `[ Line: NN ]` marker on failure; those line numbers are stale and don't track edits.
- The bot only responds in `private` chats for most handlers (`if message.chat.type == "private"`); group/channel updates are largely ignored.
