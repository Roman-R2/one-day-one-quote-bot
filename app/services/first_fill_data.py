from app import settings
from app.models.models import Quotes
from app.services.database import DBAdapter

if __name__ == '__main__':

    with DBAdapter().get_session() as session:
        with open(settings.BASE_DIR / 'data' / 'main_cites.csv', mode='r', encoding='cp866') as fd:
            print(fd.readline())
            for line in fd:
                split_line = line.split(';')
                temp_obj = Quotes(quote=split_line[1], owner=split_line[2])
                session.add(temp_obj)
        session.commit()
