import json
import os
import pathlib
import sqlite3

study_config = {
    'SUPER_USERS': [""]
}


class FileTool:
    def __init__(self):
        self.create_file()
        with open('data/study_config.json', 'r', encoding='utf-8') as f:
            self.study_config = json.load(f)
        self.super_users = self.study_config['SUPER_USERS']

    @staticmethod
    def create_file():
        pathlib.Path('data').mkdir(parents=True, exist_ok=True)
        if not os.path.exists('data/youth_study.db'):
            conn = sqlite3.connect('data/youth_study.db')
            conn.close()
        if not os.path.exists('data/study_config.json'):
            with open('data/study_config.json', 'w', encoding='utf-8') as f:
                json.dump(study_config, f, ensure_ascii=False, indent=4)
