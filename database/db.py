import sqlite3
import os

class Database:
    def __init__(self):
        os.makedirs('database', exist_ok=True)
        self.conn = sqlite3.connect('database/muxdb.sqlite', check_same_thread=False)
        self.setup()

    def setup(self):
        cmd = """CREATE TABLE IF NOT EXISTS muxbot(
            user_id INT PRIMARY KEY,
            vid_name TEXT,
            sub_name TEXT,
            filename TEXT,
            settings TEXT
        );"""
        self.conn.execute(cmd)
        self.conn.commit()

    def put_video(self, user_id, vid_name, filename):
        srch_cmd = f'SELECT * FROM muxbot WHERE user_id={user_id};'
        res = self.conn.execute(srch_cmd).fetchone()
        
        if res:
            up_cmd = f'UPDATE muxbot SET vid_name=?, filename=? WHERE user_id=?;'
            self.conn.execute(up_cmd, (vid_name, filename, user_id))
        else:
            ins_cmd = 'INSERT INTO muxbot (user_id, vid_name, filename) VALUES (?,?,?);'
            self.conn.execute(ins_cmd, (user_id, vid_name, filename))
        self.conn.commit()

    def put_sub(self, user_id, sub_name):
        srch_cmd = f'SELECT * FROM muxbot WHERE user_id={user_id};'
        res = self.conn.execute(srch_cmd).fetchone()
        
        if res:
            up_cmd = f'UPDATE muxbot SET sub_name=? WHERE user_id=?;'
            self.conn.execute(up_cmd, (sub_name, user_id))
        else:
            ins_cmd = 'INSERT INTO muxbot (user_id, sub_name) VALUES (?,?);'
            self.conn.execute(ins_cmd, (user_id, sub_name))
        self.conn.commit()

    def put_settings(self, user_id, settings):
        import json
        srch_cmd = f'SELECT * FROM muxbot WHERE user_id={user_id};'
        res = self.conn.execute(srch_cmd).fetchone()
        
        if res:
            up_cmd = f'UPDATE muxbot SET settings=? WHERE user_id=?;'
            self.conn.execute(up_cmd, (json.dumps(settings), user_id))
        else:
            ins_cmd = 'INSERT INTO muxbot (user_id, settings) VALUES (?,?);'
            self.conn.execute(ins_cmd, (user_id, json.dumps(settings)))
        self.conn.commit()

    def get_settings(self, user_id):
        import json
        cmd = f'SELECT settings FROM muxbot WHERE user_id={user_id};'
        res = self.conn.execute(cmd).fetchone()
        if res and res[0]:
            return json.loads(res[0])
        return None

    def check_sub(self, user_id):
        cmd = f'SELECT sub_name FROM muxbot WHERE user_id={user_id};'
        res = self.conn.execute(cmd).fetchone()
        return bool(res and res[0]) if res else False

    def check_video(self, user_id):
        cmd = f'SELECT vid_name FROM muxbot WHERE user_id={user_id};'
        res = self.conn.execute(cmd).fetchone()
        return bool(res and res[0]) if res else False

    def get_vid_filename(self, user_id):
        cmd = f'SELECT vid_name FROM muxbot WHERE user_id={user_id};'
        res = self.conn.execute(cmd).fetchone()
        return res[0] if res and res[0] else None

    def get_sub_filename(self, user_id):
        cmd = f'SELECT sub_name FROM muxbot WHERE user_id={user_id};'
        res = self.conn.execute(cmd).fetchone()
        return res[0] if res and res[0] else None

    def get_filename(self, user_id):
        cmd = f'SELECT filename FROM muxbot WHERE user_id={user_id};'
        res = self.conn.execute(cmd).fetchone()
        return res[0] if res and res[0] else None

    def erase(self, user_id):
        try:
            erase_cmd = f'DELETE FROM muxbot WHERE user_id={user_id};'
            self.conn.execute(erase_cmd)
            self.conn.commit()
            return True
        except:
            return False

# Initialize database
db = Database()
