import pytest

from just.simulate.agent.base_agent import BaseAgent
from just.simulate.env import Env


class MockAgent(BaseAgent):

    def _self_register(self) -> None:
        pass

    def handler(self, data: dict) -> None:
        pass


@pytest.fixture
def mock_agent():
    return MockAgent(Env())


def test_mock_agent_subscribe(mock_agent):
    mock_agent.add_subscription(
        'test_topic', mock_agent._handler)
    assert mock_agent.subscriptions == [
        ('test_topic', mock_agent._handler, mock_agent.filtering)]


def test_mock_agent_subscribe_filtering(mock_agent):
    def test_filtering(data: dict) -> bool:
        return True
    mock_agent.add_subscription(
        'test_topic', mock_agent._handler, test_filtering)
    assert mock_agent.subscriptions == [
        ('test_topic', mock_agent._handler, test_filtering)]


class MockMagicAgent(BaseAgent):

    def _self_register(self) -> None:
        pass

    def magic_topic_handler(self, data: dict, **kwargs) -> None:
        pass


@pytest.fixture
def mock_magic_agent():
    return MockMagicAgent(Env())


def test_mock_magic_agent_auto_subscribe(mock_magic_agent):
    assert mock_magic_agent.subscriptions == [(
        'magic_topic',
        mock_magic_agent.magic_topic_handler,
        mock_magic_agent.filtering)]
