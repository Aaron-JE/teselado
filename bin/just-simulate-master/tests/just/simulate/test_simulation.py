import random
from datetime import date, timedelta as td, timedelta

from just.simulate.agent import Courier, Customer, Restaurant
from just.simulate.component.assigner import RandomAssigner
from just.simulate.component.assigner.mip_assigner import MipAssigner
from just.simulate.helper import je_load_agents, skip_load_agents
from just.simulate.metric import DeliveryTime
from just.simulate.session import Session
from just.simulate.simulation import Simulation
from just.simulate.time_dist import TimeDist


def test_simulation_new():

    simulation = Simulation(
        restaurants=[
            Restaurant('The British Museum', 51.5194, -0.1270),
            Restaurant('Tate Modern', 51.5076, -0.0994)
        ],
        customers=[
            Customer('Brockwell Lido', 51.4531, -0.1064),
            Customer('Parliament Hill Lido', 51.5562, -0.1511),
            Customer('London Fields Lido', 51.5423, 0.0615)
        ],
        sessions=[
            Session('Brockwell Lido', 'The British Museum', td(hours=14)),
            Session('Parliament Hill Lido', 'Tate Modern', td(hours=15)),
            Session('London Fields Lido', 'Tate Modern', td(hours=16)),
        ],
        couriers=[
            Courier('Kenny Acheson', 51.5080, -0.1281),
            Courier('Cliff Allison', 51.5080, -0.1281)
        ],
        assigner=RandomAssigner(),
        metrics=[DeliveryTime()]
    )

    simulation.run(verbose=0)
    simulation.reporting.get_results()
    assert True


def test_simulation_helper_je_load_agents():

    restaurants, customers, sessions, __ = je_load_agents(
        date(2020, 4, 29), '74905', '80029', '91525', '5996',
        '6528', '91568', '99972', '76444', '82638', '82625')

    couriers = [
        Courier(f'Courier-{i}', restaurant.lat, restaurant.lng)
        for i, restaurant in enumerate(random.choices(restaurants, k=20))]

    simulation = Simulation(
        restaurants=restaurants,
        customers=customers,
        sessions=sessions,
        couriers=couriers,
        assigner=RandomAssigner(),
        metrics=[DeliveryTime()]
    )

    simulation.run(verbose=0)
    simulation.reporting.get_results()
    assert True


def test_simulation_helper_skip_load_agents():

    restaurants, customers, sessions, couriers = skip_load_agents(
        date(2020, 4, 29), 'Winnipeg - NW')

    for restaurant in restaurants:
        restaurant.wait = TimeDist('norm', 5, 2)

    simulation = Simulation(
        restaurants=restaurants,
        customers=customers,
        sessions=sessions,
        couriers=couriers,
        assigner=MipAssigner(),
        metrics=[DeliveryTime()]
    )

    simulation.run(verbose=0, until=timedelta(2))
    simulation.reporting.get_results()
    assert True
