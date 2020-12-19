import pytest
from faker import Faker
import pytz

from moviebase.settings import TIME_ZONE
from showtimes.models import Cinema, Screening
from movielist.models import Movie
from .utils import fake_cinema_data


faker = Faker("pl_PL")

TZ = pytz.timezone(TIME_ZONE)

# Testing create cinema option
@pytest.mark.django_db
def test_add_cinema(client, set_up):
    cinemas_before = Cinema.objects.count()
    new_cinema = fake_cinema_data()
    new_cinema["movies"] = []
    response = client.post("/cinemas/", new_cinema, format='json')
    assert response.status_code == 201
    assert Cinema.objects.count() == cinemas_before + 1
    for key, value in new_cinema.items():
        assert key in response.data
        if isinstance(value, list):
            assert len(response.data[key]) == len(value)
        else:
            assert response.data[key] == value


@pytest.mark.django_db
def test_get_cinema_list(client, set_up):
    response = client.get("/cinemas/", {}, format="json")

    assert response.status_code == 200
    assert Cinema.objects.count() == len(response.data)


@pytest.mark.django_db
def test_get_cinema_detail(client, set_up):
    cinema = Cinema.objects.first()
    response = client.get(f"/cinemas/{cinema.pk}/", {}, format="json")

    assert response.status_code == 200
    for field in ("name", "city", "movies"):
        assert field in response.data


@pytest.mark.django_db
def test_delete_cinema(client, set_up):
    cinema = Cinema.objects.first()
    response = client.delete(f"/cinemas/{cinema.pk}/", {}, format="json")
    assert response.status_code == 204
    cinema_ids = [cinema.pk for cinema in Cinema.objects.all()]
    assert cinema.pk not in cinema_ids


@pytest.mark.django_db
def test_update_cinema(client, set_up):
    cinema = Cinema.objects.first()
    response = client.get(f"/cinemas/{cinema.pk}/", {}, format="json")
    cinema_data = response.data
    new_name = "Kino Romantica"
    cinema_data["name"] = new_name
    cinema_data["movies"] = []
    response = client.patch(f"/cinemas/{cinema.pk}/", cinema_data, format='json')
    assert response.status_code == 200
    cinema_obj = Cinema.objects.get(id=cinema.id)
    assert cinema_obj.name == new_name
