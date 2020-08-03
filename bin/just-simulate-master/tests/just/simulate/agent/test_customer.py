from datetime import timedelta

from just.simulate.agent.customer import Customer
from just.simulate.env import Env
from just.simulate.time_dist import TimeDist


def test_customer_customer_session_started():

    env = Env()

    customer = Customer(
        'test_customer_id', 0, 0,
        TimeDist('fixed', 10))

    env.register(customer)

    input_data = {
        'restaurant_id': 'test_restaurant_id',
        'customer_id': 'test_customer_id'
    }

    env.publish('customer_session_started', input_data)
    for topic, output_data in env.run():
        if topic == 'order_placed':
            assert env.now == timedelta(minutes=0)
            assert input_data == output_data
            return

    assert False


def test_customer_courier_at_customer():

    env = Env()

    customer = Customer(
        'test_customer_id', 0, 0,
        TimeDist('fixed', 10))

    env.register(customer)

    input_data = {
        'order_id': 'test_order_id',
        'restaurant_id': 'test_restaurant_id',
        'customer_id': 'test_customer_id',
        'courier_id': 'test_courier_id'
    }

    env.publish('courier_at_customer', input_data)
    for topic, output_data in env.run():
        if topic == 'customer_order_collected':
            assert env.now == timedelta(minutes=10)
            assert input_data == output_data
            return

    assert False
