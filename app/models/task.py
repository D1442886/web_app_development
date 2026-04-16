import sqlite3
import os

DB_PATH = 'instance/database.db'

def get_db_connection():
    """
    建立並回傳一個 SQLite 的連線物件。
    如果 instance 資料夾或 database.db 不存在，會自動建立。
    在首次連線時將自動執行 schema.sql 以確保資料表存在。
    """
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    
    conn = sqlite3.connect(DB_PATH)
    # 設定 row_factory 可以讓結果以字典形式取用 (例如 row['title'])
    conn.row_factory = sqlite3.Row
    
    # 確保資料表結構已建立
    schema_path = 'database/schema.sql'
    if os.path.exists(schema_path):
        with open(schema_path, 'r', encoding='utf-8') as f:
            conn.executescript(f.read())
            
    return conn

class TaskModel:
    """任務模型類別，提供與 tasks 資料表互動的 CRUD 方法。"""

    @staticmethod
    def get_all(status_filter=None):
        """
        取得任務清單。
        status_filter 可傳入 'completed', 'uncompleted' 或是 None (全部)
        """
        conn = get_db_connection()
        query = 'SELECT * FROM tasks'
        params = ()
        
        if status_filter == 'completed':
            query += ' WHERE is_completed = 1'
        elif status_filter == 'uncompleted':
            query += ' WHERE is_completed = 0'
            
        query += ' ORDER BY created_at DESC'
        
        tasks = conn.execute(query, params).fetchall()
        conn.close()
        return tasks

    @staticmethod
    def create(title):
        """新增一筆任務，預設為未完成"""
        if not title or not title.strip():
            return False
            
        conn = get_db_connection()
        conn.execute('INSERT INTO tasks (title, is_completed) VALUES (?, 0)', (title.strip(),))
        conn.commit()
        conn.close()
        return True

    @staticmethod
    def delete(task_id):
        """根據 ID 刪除一筆任務"""
        conn = get_db_connection()
        conn.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
        conn.commit()
        conn.close()

    @staticmethod
    def toggle_status(task_id):
        """根據 ID 切換任務的完成狀態（0 變 1，1 變 0）"""
        conn = get_db_connection()
        current_task = conn.execute('SELECT is_completed FROM tasks WHERE id = ?', (task_id,)).fetchone()
        
        if current_task is not None:
            new_status = 0 if current_task['is_completed'] else 1
            conn.execute('UPDATE tasks SET is_completed = ? WHERE id = ?', (new_status, task_id))
            conn.commit()
            
        conn.close()
