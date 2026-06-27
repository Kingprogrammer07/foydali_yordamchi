"""Repository qatlami — har bir jadval uchun alohida sinf (SRP)."""
from bot.database.connection import Database


class UserRepo:
    """obunachilar jadvali."""

    def __init__(self, db: Database):
        self.db = db

    async def add(self, tg_id: int) -> None:
        await self.db.execute("INSERT INTO obunachilar(tg_user) VALUES(?)", (tg_id,))

    async def exists(self, tg_id: int) -> bool:
        return bool(await self.db.fetchone("SELECT 1 FROM obunachilar WHERE tg_user = ?", (tg_id,)))

    async def all_ids(self) -> list[int]:
        rows = await self.db.fetchall("SELECT tg_user FROM obunachilar")
        return [r[0] for r in rows]

    async def count(self) -> int:
        row = await self.db.fetchone("SELECT COUNT(tg_user) FROM obunachilar")
        return row[0] if row else 0


class AdminRepo:
    """owner jadvali."""

    def __init__(self, db: Database):
        self.db = db

    async def add(self, tg_id: int) -> None:
        await self.db.execute("INSERT INTO owner(admin) VALUES(?)", (tg_id,))

    async def exists(self, tg_id: int) -> bool:
        return bool(await self.db.fetchone("SELECT 1 FROM owner WHERE admin = ?", (tg_id,)))

    async def all_ids(self) -> list[int]:
        rows = await self.db.fetchall("SELECT admin FROM owner")
        return [r[0] for r in rows]

    async def paged(self) -> list[tuple]:
        """(id, admin) — boshqaruv ro'yxati uchun (LIMIT 8)."""
        return await self.db.fetchall("SELECT id, admin FROM owner LIMIT 8")

    async def get(self, row_id: int) -> int | None:
        row = await self.db.fetchone("SELECT admin FROM owner WHERE id = ?", (row_id,))
        return row[0] if row else None

    async def delete(self, row_id: int) -> None:
        await self.db.execute("DELETE FROM owner WHERE id = ?", (row_id,))


class ChannelRepo:
    """channels_data jadvali (majburiy obuna kanallari)."""

    def __init__(self, db: Database):
        self.db = db

    async def add(self, channel_id: int) -> None:
        await self.db.execute("INSERT INTO channels_data(channel_id) VALUES(?)", (channel_id,))

    async def exists(self, channel_id: int) -> bool:
        return bool(await self.db.fetchone("SELECT 1 FROM channels_data WHERE channel_id = ?", (channel_id,)))

    async def count(self) -> int:
        row = await self.db.fetchone("SELECT COUNT(channel_id) FROM channels_data")
        return row[0] if row else 0

    async def all_ids(self) -> list[int]:
        rows = await self.db.fetchall("SELECT channel_id FROM channels_data")
        return [r[0] for r in rows]

    async def paged(self) -> list[tuple]:
        """(id, channel_id) — birinchi sahifa (LIMIT 8)."""
        return await self.db.fetchall("SELECT id, channel_id FROM channels_data LIMIT 8")

    async def range(self, lo: int, hi: int) -> list[tuple]:
        return await self.db.fetchall(
            "SELECT id, channel_id FROM channels_data WHERE id BETWEEN ? AND ? ORDER BY id", (lo, hi)
        )

    async def max_id(self) -> int | None:
        row = await self.db.fetchone("SELECT MAX(id) FROM channels_data")
        return row[0] if row else None

    async def get(self, row_id: int) -> int | None:
        row = await self.db.fetchone("SELECT channel_id FROM channels_data WHERE id = ?", (row_id,))
        return row[0] if row else None

    async def delete(self, row_id: int) -> None:
        await self.db.execute("DELETE FROM channels_data WHERE id = ?", (row_id,))


class PostRepo:
    """for_post jadvali (tayyorlanayotgan media postlar)."""

    def __init__(self, db: Database):
        self.db = db

    async def add(self, admin_id: int, file_id: str, caption: str) -> None:
        await self.db.execute(
            "INSERT INTO for_post(admin_id, file_id, caption) VALUES(?, ?, ?)", (admin_id, file_id, caption)
        )

    async def exists(self, admin_id: int) -> bool:
        return bool(await self.db.fetchone("SELECT 1 FROM for_post WHERE admin_id = ?", (admin_id,)))

    async def update(self, file_id: str, caption: str, admin_id: int) -> None:
        await self.db.execute(
            "UPDATE for_post SET file_id = ?, caption = ? WHERE admin_id = ?", (file_id, caption, admin_id)
        )

    async def get(self, admin_id: int) -> list[tuple]:
        """[(file_id, caption), ...]"""
        return await self.db.fetchall("SELECT file_id, caption FROM for_post WHERE admin_id = ?", (admin_id,))


class ElonRepo:
    """for_elon jadvali (tayyorlanayotgan matnli e'lonlar)."""

    def __init__(self, db: Database):
        self.db = db

    async def add(self, chat_id: int, elon: str) -> None:
        await self.db.execute("INSERT INTO for_elon(id_raqami, elon) VALUES(?, ?)", (chat_id, elon))

    async def update(self, chat_id: int, elon: str) -> None:
        # FIX (R10): asl kodda WHERE yo'q edi — hamma qatorni yangilardi.
        await self.db.execute("UPDATE for_elon SET elon = ? WHERE id_raqami = ?", (elon, chat_id))

    async def exists(self, chat_id: int) -> bool:
        return bool(await self.db.fetchone("SELECT 1 FROM for_elon WHERE id_raqami = ?", (chat_id,)))

    async def get(self, chat_id: int) -> str | None:
        row = await self.db.fetchone("SELECT elon FROM for_elon WHERE id_raqami = ?", (chat_id,))
        return row[0] if row else None
