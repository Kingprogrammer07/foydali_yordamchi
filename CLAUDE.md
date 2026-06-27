# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

A Telegram bot ("Foydali yordamchi [PC Mexanics]") on **aiogram 3.29** (Python 3.11). It distributes school textbooks and PC software (links to Telegram channel posts), downloads video/media from YouTube/Instagram/TikTok, and gives admins a post-broadcast + user/channel/admin management panel. All user-facing text and most comments are in **Uzbek** — match that language when editing strings.

> Migrated from aiogram 2.22.2 to a clean layered architecture. The old flat tree (`app.py`, `loader.py`, `handlers/`, `keyboards/`, `data/post_data.py`, …) is gone; everything lives under `bot/`.

## Commands

```bash
pip install -r requirements.txt   # aiogram 3.29, aiosqlite, python-dotenv, requests
python -m bot                     # run the bot (long-polling)
python purifier.py                # dev tool: recursively delete __pycache__
```

No tests/linter/build step. `runtime.txt` (`python-3.11.9`) targets a simple deploy. Secrets come from **`.env`** (`.env.example` is the template): `BOT_TOKEN`, `RAPIDAPI_KEY` + 3 `RAPIDAPI_*_HOST`.

## Architecture (`bot/`)

Explicit wiring — no import-side-effect magic. `bot/__main__.py` is the single composition root:

- Builds `Bot(default=DefaultBotProperties(parse_mode=HTML))` + `Dispatcher(MemoryStorage)`.
- **Dependency injection via workflow data**: repositories are set as `dp["users"]`, `dp["admins"]`, `dp["channels"]`, `dp["posts"]`, `dp["elons"]`. Handlers/filters/middlewares receive them by parameter name (e.g. `async def h(message, admins: AdminRepo)`). `bot` is auto-injected by aiogram.
- Registers middlewares, then `dp.include_router(setup_routers())`.

**Data layer** (`bot/database/`): `connection.py` holds one shared `aiosqlite` connection (`Database`) with `create_tables()` (idempotent, runs on startup). `repositories.py` is one class per table (`UserRepo`, `AdminRepo`, `ChannelRepo`, `PostRepo`, `ElonRepo`) — all DB access goes through these. **Schema and data file (`data/database.sqlite3`) are unchanged from the old version**; tables: `obunachilar`, `owner`, `channels_data`, `for_post`, `for_elon`.

**Router order is load-bearing** (`bot/handlers/__init__.py` `setup_routers()`): `errors.router` is used as the **root** (errors bubble up to it, so its `@router.errors` handlers catch everything), feature routers are included into it, and `menu.router` is **last** because it contains the catch-all `echo`. Anything that must beat `echo` (catalog sends, admin buttons, broadcast) is included before it.

**aiogram-3 conventions used throughout:**
- `@router.message(F.text == "...")`, `Command(...)`, `CommandStart()`; state via `StateFilter(...)` or passing the `State` positionally.
- **Every non-state handler carries `StateFilter(None)`** — in v3 a handler without it fires in *all* states and would steal input mid-FSM. Keep this when adding handlers.
- `CallbackData` subclasses in `bot/keyboards/callbacks.py` (`PostCB`, `AdminPostCB`, `ChannelCB`, `DeleteCB`, `TaklifCB`, `BotPostCB`); filter with `X.filter(F.action == ...)`, build with `X(...).pack()`.
- Keyboards: reply menus in `keyboards/reply.py` (explicit `ReplyKeyboardMarkup`), inline in `keyboards/inline.py` (`InlineKeyboardBuilder` for dynamic ones).
- `IsAdmin` filter (`bot/filters/is_admin.py`) queries the DB **live** every time — there is no `ADMINS`/`CHANNELS` snapshot, so runtime admin/channel changes take effect without restart.

**Middlewares** (`bot/middlewares/`): `subscription.py` is a typed `outer_middleware` on `dp.update` — the force-subscription gate; it lets `/start`, `/help`, and the `check_subs` callback through, otherwise requires membership in all `channels_data` (only in private chats). `throttling.py` is a per-user TTL anti-flood on `dp.message`.

**Content catalog** (`bot/content/catalog.py`): the ~70 "button → document/photo(s)" entries are pure data (`BOOKS`, `SOFTWARE` dicts of `Item`). `handlers/user/books.py` and `software.py` are thin — one dict lookup replaces the old 950-line elif chain. Adding a download = add a `catalog.py` entry (and a `reply.py` button if it needs one); no handler code.

**Broadcast** (`bot/handlers/admin/broadcast.py`): post-building state lives entirely in **FSM** (`state.update_data`), not module globals — concurrent admins don't clash. Publishing uses **`bot.copy_message` / `message.copy_to`** (single message, with optional `reply_markup`) or **`bot.copy_messages`** (album), which preserve the original formatting — so there is no per-content-type branching and no manual entity handling. Supports text / photo / video / document / voice and **albums** (media groups). Targets are resolved by `_targets()` from the FSM `sort` (`first_chanel` / `in_bot` / `all_chanel` / specific `channel_id`). **Album limitations**: inline buttons can't attach to an album (Telegram), and album *user-suggestions* (Taklif) are rejected (only single-message suggestions go through the admin-approval flow).

**Albums** (`bot/middlewares/album.py`): Telegram delivers a media group as separate messages; `AlbumMiddleware` (outer, on `dp.message`) debounces them by `media_group_id` and hands the full list to the handler as `album: list[Message]`. `ThrottlingMiddleware` skips `media_group_id` messages so album bursts aren't dropped.

## Conventions & gotchas

- **Secrets were exposed before the `.env` migration and were committed in git history** — the `BOT_TOKEN` and `RAPIDAPI_KEY` should be rotated (BotFather `/revoke`; RapidAPI regenerate). `.env` and `data/database.sqlite3` are gitignored.
- Navigation reply-button texts (`Asosiy Bo`lim⬅️`, `Asosiy bo`lim💡`, `🔙Orqaga⬅️`, `Orqaga🔧`, …) are intentionally distinct — they encode position in the menu tree (each returns to a *specific* parent), so they're not collapsed to one "back". `menu.py` `NAV` maps each to its target keyboard.
- Reply-button texts must stay byte-identical across `reply.py`, `content/catalog.py` keys, and the `F.text == ...` / `NAV` handlers — a mismatch silently routes to `echo`.
- `RAPIDAPI` calls use blocking `requests` wrapped in `asyncio.to_thread` (`handlers/user/download.py`); YouTube `videoId` is parsed by regex (pytube was dropped).
- Error handlers are registered on the **root** router; per-leaf-router error handlers would only catch their own router's errors.
