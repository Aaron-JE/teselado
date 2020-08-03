from datetime import timedelta

from just.simulate.bus import Bus


def test_bus_run():

    bus = Bus()
    bus.publish('test_topic_0', {})
    bus.publish('test_topic_1', {}, delay=timedelta(seconds=1))
    bus.publish('test_topic_2', {}, delay=timedelta(seconds=2))
    for i, (topic, data) in enumerate(bus.run()):
        assert topic == f'test_topic_{i}'
        assert bus.now == timedelta(seconds=i)


def test_bus_subscription():

    class MockClass:

        def __init__(self) -> None:
            self.ack = False

        def mock_handler(self, __: dict, **kwargs) -> None:
            self.ack = True

    bus = Bus()
    mock_object = MockClass()
    bus.add_subscription(
        'test_topic', mock_object.mock_handler)
    bus.publish('test_topic', {})

    assert mock_object.ack is False

    topic, data = bus.scan()

    assert topic == 'test_topic'
    assert data == {}
    assert mock_object.ack is True


def test_bus_subscription_yield():

    class MockYieldClass:

        def __init__(self) -> None:
            self.ack = None

        def mock_handler(self, __: dict, **kwargs) -> None:
            self.ack = False
            yield timedelta(seconds=1)
            self.ack = True

    bus = Bus()
    mock_object = MockYieldClass()
    bus.add_subscription(
        'test_topic', mock_object.mock_handler)
    bus.publish('test_topic', {})

    assert mock_object.ack is None

    topic, data = bus.scan()

    assert topic == 'test_topic'
    assert data == {}
    assert mock_object.ack is False
    assert bus.now == timedelta(seconds=0)

    topic, data = bus.scan()

    assert topic is None
    assert data is None
    assert mock_object.ack is True
    assert bus.now == timedelta(seconds=1)
