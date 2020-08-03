from datetime import timedelta

from just.simulate.agent.restaurant import Restaurant
from just.simulate.env import Env
from just.simulate.time_dist import TimeDist


def test_mock_restaurant():

    env = Env()

    restaurant = Restaurant(
        'test_id', 0, 0, timedelta(0), timedelta(1),
        TimeDist('fixed', 10, unit='minutes'))

    env.register(restaurant)

    input_data = {
        'order_id': '1',
        'restaurant_id': restaurant.id,
        'customer_id': '3',
        'courier_id': '4'
    }

    env.publish('courier_at_restaurant', input_data)
    for topic, output_data in env.run():
        if topic == 'restaurant_order_ready':
            assert env.now == timedelta(minutes=10)
            assert input_data == output_data
            return

    assert False
