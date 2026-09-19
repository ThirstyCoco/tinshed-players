from datetime import date, time

import pytest

from app import create_app
from app.models import CrewCall, Performance, Production, Volunteer, db


@pytest.fixture()
def app(tmp_path):
    app = create_app(
        {
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": f"sqlite:///{tmp_path / 'test.db'}",
        }
    )
    with app.app_context():
        db.create_all()
    yield app
    with app.app_context():
        db.session.remove()
        db.drop_all()


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def seed(app):
    with app.app_context():
        volunteer = Volunteer(name="Marion D'Souza", phone="0400 000 000")
        production = Production(title="The Weather House")
        performance = Performance(date=date(2026, 9, 4), start_time=time(19, 30))
        performance.crew_calls.append(CrewCall(role="Box Office", count=1))
        production.performances.append(performance)
        db.session.add_all([volunteer, production])
        db.session.commit()
    return {"volunteer": volunteer, "production": production, "performance": performance}
