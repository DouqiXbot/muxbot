import sqlite3

def init_db():
    conn = sqlite3.connect("user_data.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_settings (
            user_id TEXT PRIMARY KEY,
            crf TEXT,
            codec TEXT,
            preset TEXT,
            resolution TEXT,
            fontsize TEXT
        )
    ''')
    conn.commit()
    conn.close()

def save_user_settings(user_id, settings):
    conn = sqlite3.connect("user_data.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT OR REPLACE INTO user_settings (user_id, crf, codec, preset, resolution, fontsize)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (user_id, settings["crf"], settings["codec"], settings["preset"], settings["resolution"], settings["fontsize"]))
    conn.commit()
    conn.close()

def get_user_settings(user_id):
    conn = sqlite3.connect("user_data.db")
    cursor = conn.cursor()
    cursor.execute("SELECT crf, codec, preset, resolution, fontsize FROM user_settings WHERE user_id=?", (user_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return dict(zip(["crf", "codec", "preset", "resolution", "fontsize"], row))
    return None
