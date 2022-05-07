import sqlite3
from typing import Optional


class UserDao:
    def __init__(self):
        self.db_path = 'data/youth_study.db'
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        self.cursor.execute(
            'create table if not exists study_user(user_id text primary key, push integer default 0)')
        self.cursor.execute(
            'create table if not exists friend_req(user_id text primary key,flag text)')
        self.conn.commit()
        self.conn.close()

    def set_or_update_push(self, user_id: str, push: int):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('insert or ignore into study_user(user_id, push) values(?, ?)', (user_id, push))
        cursor.execute('update study_user set push = ? where user_id = ?', (push, user_id))
        conn.commit()
        conn.close()

    def get_push_user(self) -> list:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('select user_id from study_user where push = 1')
        user_list = cursor.fetchall()
        conn.close()
        data = []
        for user in user_list:
            data.append(user[0])
        return data

    def set_or_update_friend_req(self, user_id: str, flag: str):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('insert or ignore into friend_req(user_id, flag) values(?, ?)', (user_id, flag))
        cursor.execute('update friend_req set flag = ? where user_id = ?', (flag, user_id))
        conn.commit()
        conn.close()

    def get_friend_req(self, user_id: Optional[str] = None) -> list:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        if user_id:
            cursor.execute('select user_id,flag from friend_req where user_id = ?', (user_id,))
        else:
            cursor.execute('select user_id,flag from friend_req')
        user_list = cursor.fetchall()
        conn.close()
        data = []
        for user in user_list:
            data.append({
                'user_id': user[0],
                'flag': user[1]
            })
        return data
