from app.main import app


def test_hospitals_routes_registered():
    paths = [route.path for route in app.routes]
    assert any(p.startswith("/hospitals") for p in paths), "hospitals routes not registered"
