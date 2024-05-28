from app import settings
from app.models.models import Quotes
from app.services.database import DBAdapter


class FirstFillTables:

    @staticmethod
    def fill_data():
        with DBAdapter().get_session() as session:
            with open(settings.BASE_DIR / 'data' / 'main_cites.csv', mode='r', encoding='cp866') as fd:
                for line in fd:
                    split_line = line.split(';')
                    temp_obj = Quotes(quote=split_line[1], owner=split_line[2])
                    session.add(temp_obj)
            session.commit()


    @staticmethod
    def get_quotes_table_row_count():
        with DBAdapter().get_session() as session:
            rows = session.query(Quotes).count()
            return rows


if __name__ == '__main__':
    print(f"Подключите файл как модуль.")
