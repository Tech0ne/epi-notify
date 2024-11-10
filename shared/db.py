from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import time
import os

def get_engine():
    engine = create_engine(os.getenv("DB_URL"), echo=False)
    delay = 3

    while 1:
        try:
            with engine.connect():
                pass
            return engine
        except:
            time.sleep(delay)

engine = get_engine()

session = sessionmaker(autocommit=False, autoflush=False, bind=engine)()