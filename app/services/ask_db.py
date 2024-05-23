import random

from app.models.models import Quotes
from app.services.database import DBAdapter


class AskDB:
    def random_quote(self) -> str:
        with DBAdapter().get_session() as session:
            rand = random.randrange(0, session.query(Quotes).count())
            rand_row: Quotes = session.query(Quotes)[rand]
            return f"{rand_row.quote}\n---------------------------\n{rand_row.owner}"
