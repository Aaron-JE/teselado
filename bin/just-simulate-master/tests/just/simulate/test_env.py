from just.simulate.env import Env
from just.simulate.registrable import Registrable


def test_env():

    class MockClass(Registrable):
        pass

    env = Env()
    mock_object = MockClass()
    env.register(mock_object)
    mock_object.env.publish('test_topic', {})
    topic, data = next(env.run())
    assert topic == 'test_topic'
    assert data == {}
