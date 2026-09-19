def test_create_production(client):
    response = client.post(
        "/productions/new",
        data={"title": "Salt on the Wind"},
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"Salt on the Wind" in response.data


def test_create_performance_with_crew_call(client, seed):
    response = client.post(
        f"/productions/{seed['production'].id}/performances/new",
        data={
            "date": "2026-09-05",
            "start_time": "14:00",
            "role": ["Lighting Op", "Usher"],
            "count": ["1", "2"],
        },
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"Lighting Op" in response.data
    assert b"Usher x2" in response.data


def test_performances_listed_in_order(client, app, seed):
    from datetime import date, time

    from app.models import Performance, db

    with app.app_context():
        later = Performance(
            production=seed["production"],
            date=date(2026, 9, 12),
            start_time=time(19, 30),
        )
        db.session.add(later)
        db.session.commit()
    response = client.get(f"/productions/{seed['production'].id}")
    assert response.status_code == 200
    assert response.data.index(b"04 Sep") < response.data.index(b"12 Sep")
