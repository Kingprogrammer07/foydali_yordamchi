"""aiosqlite asosidagi async DB ulanish. Bitta umumiy connection."""
import aiosqlite

from bot.config import DB_PATH


class Database:
    """Yagona aiosqlite ulanishni boshqaradi va past darajadagi so'rovlarni beradi."""

    def __init__(self, path=DB_PATH):
        self.path = path
        self._conn: aiosqlite.Connection | None = None

    async def connect(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)  # data/ yo'q bo'lsa yaratadi
        self._conn = await aiosqlite.connect(self.path)
        await self.create_tables()

    async def close(self) -> None:
        if self._conn is not None:
            await self._conn.close()
            self._conn = None

    async def execute(self, sql: str, params: tuple = ()) -> None:
        await self._conn.execute(sql, params)
        await self._conn.commit()

    async def fetchone(self, sql: str, params: tuple = ()):
        async with self._conn.execute(sql, params) as cur:
            return await cur.fetchone()

    async def fetchall(self, sql: str, params: tuple = ()) -> list:
        async with self._conn.execute(sql, params) as cur:
            return await cur.fetchall()

    async def create_tables(self) -> None:
        """Jadvallar yo'q bo'lsa yaratadi (idempotent — mavjud ma'lumotga tegmaydi)."""
        await self.execute("CREATE TABLE IF NOT EXISTS obunachilar (id INTEGER PRIMARY KEY, tg_user INTEGER NOT NULL)")
        await self.execute("CREATE TABLE IF NOT EXISTS owner (id INTEGER PRIMARY KEY, admin INTEGER NOT NULL)")
        await self.execute("CREATE TABLE IF NOT EXISTS channels_data (id INTEGER PRIMARY KEY, channel_id INTEGER NOT NULL)")
        await self.execute("CREATE TABLE IF NOT EXISTS for_post (id INTEGER PRIMARY KEY, admin_id INTEGER NOT NULL, file_id TEXT NOT NULL, caption TEXT NOT NULL)")
        await self.execute("CREATE TABLE IF NOT EXISTS for_elon (id INTEGER PRIMARY KEY, id_raqami INTEGER NOT NULL, elon TEXT NOT NULL)")
