import sqlite3

from pathlib import Path

DATABASE_NAME = "database.sqlite3"



class Database():
    """"
    'db_name' Data base-ning nomi. masalan:db.sqlite3
    'path_db' bu 'db_name'-ni qayerda joylashganini dasturga ko'rsatish uchun kerak ( berilmasa avtomatik tarzda o'zi shu PATH oladi ).
    """
    base_dir = Path(__file__).resolve()
    def __init__(self,db_name,path_db=None):
        PATH = path_db or self.base_dir.parent
        self.datebase = PATH / db_name 
        
        # fle = Path(self.datebase) 
        # fle.touch(exist_ok=True) # auto creator file
    

    def connection(self):                                                           #Basa bilan bog'lanish
        self.connect =  sqlite3.connect(self.datebase)
        self.cur = self.connect.cursor()
    
    def close(self):                                                                #Basa-ni yopish ( Basa bilan aloqalikni uzish )
        self.connect.close()

    
    def execute(self,code,items:tuple=()):                                          #Basa-ga o'zartirish kiritish uchun (Basa-ga yozish qismi)
        self.connection()
        self.cur.execute(code,items)
        self.connect.commit()
        return self


    def fetchall(self):                                                             # execute -> commit -> fetchall ( SELECT-dan qaytgan ma'lumotlarni olish )
        return self.cur.fetchall() 

    def fetchone(self):                                                             # execute -> commit -> fetchone ( SELECT-dan qaytgan ma'lumotlarni olish )
        return self.cur.fetchone() 

    def fetchmany(self):                                                            # execute -> commit -> fetchmany ( SELECT-dan qaytgan ma'lumotlarni olish )
        return self.cur.fetchmany() 




    ########################################### qo'shim def yoziz mumkin bo'lgan hudud ###########################################################
    def create_tables(self):                                                        # Jadvallarni yaratish (idempotent — mavjud ma'lumotga tegmaydi)
        self.execute("CREATE TABLE IF NOT EXISTS obunachilar (id INTEGER PRIMARY KEY, tg_user INTEGER NOT NULL)")
        self.execute("CREATE TABLE IF NOT EXISTS owner (id INTEGER PRIMARY KEY, admin INTEGER NOT NULL)")
        self.execute("CREATE TABLE IF NOT EXISTS channels_data (id INTEGER PRIMARY KEY, channel_id INTEGER NOT NULL)")
        self.execute("CREATE TABLE IF NOT EXISTS for_post (id INTEGER PRIMARY KEY, admin_id INTEGER NOT NULL, file_id TEXT NOT NULL, caption TEXT NOT NULL)")
        self.execute("CREATE TABLE IF NOT EXISTS for_elon (id INTEGER PRIMARY KEY, id_raqami INTEGER NOT NULL, elon TEXT NOT NULL)")

                                                    # for user
    def user_plus(self,chat_id):
        self.execute("""
        INSERT INTO obunachilar(tg_user) VALUES(?)
        """, (chat_id,))

    def is_user(self,chat_id):
        result = self.execute("""
        SELECT tg_user FROM obunachilar WHERE tg_user = ?
        """, (chat_id,)).fetchall()
        return bool(len(result))

    def user_view(self):
        return self.execute("SELECT tg_user FROM obunachilar").fetchall()

    def user_count(self):
        return self.execute("""
        SELECT COUNT(tg_user) FROM obunachilar
        """).fetchone()[0]

                                                    ## for admin
    def admin_plus(self,chat_id):
        self.execute("""
        INSERT INTO owner(admin) VALUES(?)
        """, (chat_id,))

    def is_admin(self,chat_id):
        result = self.execute("""
        SELECT admin FROM owner WHERE admin = ?
        """, (chat_id,)).fetchall()
        return bool(len(result))

    def admin_view(self):
        return self.execute("""
        SELECT admin FROM owner
        """).fetchall()
                                                ## channel malumotlar

    def channel_plus(self,channel_id):
        self.execute("""
        INSERT INTO channels_data(channel_id) VALUES(?) 
        """, (channel_id,))

    def is_channel(self,channel_id):
        result = self.execute("""
        SELECT channel_id FROM channels_data WHERE channel_id = ?
        """, (channel_id,)).fetchall()
        return bool(len(result))

    def chanel_count(self):
        return self.execute("""
        SELECT COUNT(channel_id) FROM channels_data
        """).fetchone()[0]

    def channel_view(self):
        return self.execute("""
        SELECT channel_id FROM channels_data
        """).fetchall()


                                                        ## malumot yozish va ko`rish
    def for_post(self,admin_id,file_id,caption):
        self.execute("""
            INSERT INTO for_post(admin_id,file_id,caption) VALUES(?,?,?)
        """, (admin_id,file_id,caption,))

    def is_in_post(self,chat_id):
        result = self.execute("""
        SELECT admin_id FROM for_post WHERE admin_id = ?
        """, (chat_id,)).fetchall()
        return bool(len(result))
    
    def is_in_elon(self,chat_id):
        result = self.execute("""
        SELECT id_raqami FROM for_elon WHERE id_raqami = ?
        """, (chat_id,)).fetchall()
        return bool(len(result))

    def post_update(self,file_id,caption,chat_id):
        self.execute("""
        UPDATE for_post SET file_id = ?,caption = ? WHERE admin_id = ?
        """, (file_id,caption,chat_id,))

    def for_elon(self,chat_id,elon):
        self.execute("""
        INSERT INTO for_elon(id_raqami,elon) VALUES(?,?)
        """, (chat_id,elon,))

    def for_elon_update(self,chat_id,elon):
        self.execute("""
        UPDATE for_elon SET id_raqami = ?,elon = ?
        """, (chat_id,elon,))

    def for_elon_is_id(self,chat_id):
        result = self.execute("""
        SELECT id_raqami FROM for_elon WHERE id_raqami = ?
        """, (chat_id,)).fetchall()
        return bool(len(result))

    def for_elon_view(self,chat_id):
        d = self.execute("""
        SELECT elon FROM for_elon WHERE id_raqami = ?
        """, (chat_id,)).fetchone()[0]
        return d

    def for_post_view(self,chat_id):
        return self.execute("""
        SELECT file_id,caption FROM for_post WHERE admin_id = ?
        """, (chat_id,)).fetchall()


                                                                ## vkm stilida


    def vkm_stili(self):
        return self.execute("""
        SELECT id,channel_id FROM channels_data LIMIT 8
        """).fetchall()

    def is_max(self):
        return self.execute("""
        SELECT MAX(id) FROM channels_data
        """).fetchone()[0]

    def view(self, kichik_id, katta_id):
        return self.execute("""SELECT id,channel_id FROM channels_data
                        WHERE id BETWEEN ? AND ?
                        ORDER BY id;
""", (kichik_id,katta_id,)).fetchall()

    def get_malumot(self,id):
        return self.execute("""
            SELECT channel_id FROM channels_data WHERE id = ?
            """, (id,)).fetchone()[0]

    def get_malumot_del(self,id):
        return self.execute("""
        DELETE FROM channels_data WHERE id = ?
        """, (id,))

    def vkm_stili_admin(self):
        return self.execute("""
        SELECT id, admin FROM owner LIMIT 8
        """).fetchall()

    def del_admin(self,id):
        self.execute("""
        DELETE FROM owner WHERE id = ?
        """, (id,))

    def get_admin(self,id):
        return self.execute("""
        SELECT admin FROM owner WHERE id = ?
        """, (id,)).fetchone()[0]

    # def tests(self):
    #     self.execute("""
    #     ALTER TABLE for_post DROP COLUMN type
    #     """)


db = Database(db_name=DATABASE_NAME,path_db=Path(__file__).resolve().parent)        # 'path_db' berilmasa, dastur shu yerda o'zi kerakli file-ni ochib oladi
db.create_tables()                                                                  # jadvallar yo'q bo'lsa yaratadi (bo'sh DB'da ishlashi uchun)
    # print("oxirgi kiritilgan ma'lumot id-si: ",db.cur.lastrowid)

# if __name__ == "__main__":
#     db.tests()
