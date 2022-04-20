try:
    from utils.tmp_db_data import default_infos
except Exception:
    default_infos = {}
from app.db_connector import *  # noqa
from app.sqlalchemy_h import Base, engine, SessionContext
from app import backapp, backpair, backpays
import argparse
import datetime as dt
import json
import os
from pathlib import Path
from rich import print
from rich.console import Console
from rich.table import Table  # type: ignore

checkyes = False
console = Console()


def rinput(*args):
    print(*args, end='', flush=True)
    return input()


def unix2ctime(t: str):
    return dt.datetime.fromtimestamp(int(t)).ctime()


class DotEnvParser:
    def __init__(self, env_path) -> None:
        if not isinstance(env_path, Path):
            env_path = Path(env_path)
        self.env_path = env_path
        self.parse()

    def parse(self):
        self.envs = os.environ
        with self.env_path.open(mode='r') as f:
            for line in f.read().split('\n'):
                key, *values = line.split('=')
                self.envs[key] = '='.join(values)


def db_init(auto_yes=False):
    if auto_yes or input('Going to delete all data in DB. Are you sure what you are doing? [y/N] ') == 'y':
        print('initializing DB')
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)
        for i, user in enumerate(default_infos['user']):
            token = backapp.signup(**user)
            if token is None:
                token = backapp.userid2token(i + 1)
            user['token'] = token
        backpair.addnewpair(2, 1)
        for i, pay in enumerate(default_infos['payments']):
            pay['pairhash'] = backpair.generatePairHash(1, 2)
            token = backpays.addpayment(**pay)
            print(f'{i=}', f'{pay=}', f'{token=}')
    else:
        print('Not initializing the DB.')
    db_show()


def show_all_data(name: str, columns, data):
    table = Table(title=name.upper())
    for c in columns:
        table.add_column(c)
    for d in data:
        table.add_row(*[str(d[c]) for c in columns])
    console.print(table, justify='center')


def find_tables():
    tables = []
    g = globals()
    names = set(Base.metadata.tables.keys())
    for t in g:
        if t.lower() in names:
            tables.append(g[t])
    return tables


def db_show():
    with SessionContext() as session:
        for t in find_tables():
            show_all_data(t.__name__, t.__table__.c.keys(), [
                          s.get_dict() for s in session.query(t).all()])


class VueI18nDict:
    def __init__(self, lang_dir='./src/lang', json_name='dictionary.json') -> None:
        if not isinstance(lang_dir, Path):
            lang_dir = Path(lang_dir)
        self.lang_dir = lang_dir
        self.json_name = json_name
        self.json_path = self.lang_dir / self.json_name
        self.dictionary = {}
        if self.json_path.exists():
            with self.json_path.open('r') as f:
                self.dictionary = json.loads(f.read())
        self.availableLocales = list(self.dictionary.keys())

    def from_csv(self):
        for p in self.lang_dir.glob('*.csv'):
            with p.open(mode='r') as f:
                contents = f.read().split('\n')
                languages = contents[0].split(',')[1:]
                for lang in languages:
                    self.dictionary.setdefault(lang, {})
                for line in contents[1:]:
                    keys = line.split(',')
                    if len(keys) < len(languages) + 1:
                        continue
                    for i, lang in enumerate(languages):
                        self.dictionary[lang].setdefault(p.stem.capitalize(), {})
                        self.dictionary[lang][p.stem.capitalize()][keys[0]] = keys[i + 1].replace('~', ',')

    def reset(self):
        self.dictionary = {}

    def save(self):
        with self.json_path.open(mode='w') as f:
            f.write(json.dumps(self.dictionary, indent=4, sort_keys=True))

    def print(self):
        print(self.dictionary)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='upload .md to your webpage')
    parser.add_argument('-y', '--yes', action='store_true', help='pass yes to all verifications')
    parser.add_argument('--lang', action='store_true', help='language json')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-d', '--db', type=str, help='delete all data in DB')

    args = parser.parse_args()

    if args.yes:
        checkyes = True

    if args.db:
        if args.db == 'init':
            db_init(checkyes)
        elif args.db == 'show':
            db_show()
        else:
            print('Couldn\'t find a corresponding command')
            print('init\tclear all data in DB')
            print('show\tshow all data in DB')

    if args.lang:
        lang = VueI18nDict('src/lang', json_name='dictionary.json')
        lang.reset()
        lang.from_csv()
        lang.save()
        lang.print()
