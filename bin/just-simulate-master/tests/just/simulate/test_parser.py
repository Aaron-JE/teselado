from just.simulate.parser import SimulationSchema


def test_parser():

    config = {
        "restaurants": [
            {
                "id": "Tate Modern",
                "lat": 51.5076,
                "lng": -0.0994,
                "start_time": "00:00:00",
                "end_time": "23:59:59"
            },
            {
                "id": "The British Museum",
                "lat": 51.5194,
                "lng": -0.1270,
                "start_time": "00:00:00",
                "end_time": "23:59:59"
            }
        ],
        "customers": [
            {
                "id": "Brockwell Lido",
                "lat": 51.4531,
                "lng": -0.1064
            },
            {
                "id": "Parliament Hill Lido",
                "lat": 51.5562,
                "lng": -0.1511
            },
            {
                "id": "London Fields Lido",
                "lat": 51.5423,
                "lng": 0.0615
            }
        ],
        "couriers": [
            {
                "id": "Kenny Acheson",
                "lat": 51.5080,
                "lng": -0.1281,
                "start_time": "00:00:00",
                "end_time": "23:59:59"
            },
            {
                "id": "Cliff Allison",
                "lat": 51.5080,
                "lng": -0.1281,
                "start_time": "00:00:00",
                "end_time": "23:59:59"
            }
        ]
    }

    schema = SimulationSchema()
    assert schema.validate(config) == {}
