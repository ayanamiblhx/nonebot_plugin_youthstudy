import sqlite3


class GroupDao:
    def __init__(self):
        self.db_path = 'data/youth_study.db'
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        self.cursor.execute(
            'create table if not exists study_group(group_id text primary key,push integer default 0)')
        self.conn.commit()
        self.conn.close()

    def set_or_update_push(self, group_id: str, push: int = 1):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('insert or ignore into study_group(group_id,push) values(?,?)',
                       (group_id, push))
        cursor.execute('update study_group set push=? where group_id=?', (push, group_id))
        conn.commit()
        conn.close()

    def get_push_group(self) -> list:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('select group_id from study_group where push=1')
        group_list = cursor.fetchall()
        conn.close()
        data = []
        for group in group_list:
            data.append(group[0])
        return data
