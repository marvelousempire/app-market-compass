from market_compass.technical import enrich, fibonacci, memory_and_route_layers, price_memory, trend_layer


def test_price_memory_is_symmetric(sample_data):
    x = enrich(sample_data.bars)
    supports, resistances = price_memory(x)
    assert supports and resistances
    assert all("touches" in z and "strength" in z and "erosion" in z for z in supports + resistances)


def test_bus_stop_route(sample_data):
    x = enrich(sample_data.bars)
    t = trend_layer(x)
    _, _, route = memory_and_route_layers(x, t.score)
    assert route.direction in {"up", "down"}
    assert isinstance(route.fibonacci, dict)
    assert fibonacci(x)[0] in {"up", "down"}
