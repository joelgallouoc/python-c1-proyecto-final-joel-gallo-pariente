from sqlalchemy import text

from app.extensions import db


def check_database():

    try:

        db.session.execute(
            text("SELECT 1")
        )

        return True

    except Exception:

        return False