import datetime
from datetime import timedelta
from typing import List, Tuple

from just.simulate.agent import Courier, Customer, Restaurant
from just.simulate.session import Session
from just.simulate.utils import read_gbq


def je_load_agents(date: datetime.date, *args: str) -> Tuple[
        List[Restaurant], List[Customer], List[Session], List[Courier]]:
    """Load agents."""

    _comma_separated = ','.join([f'"{arg}"' for arg in args])

    rows = read_gbq(f"""
        SELECT
          CAST(RestaurantId AS STRING) AS restaurant_id,
          OrderContainer.CustomerInfo.GeoPosition.Latitude AS restaurant_lat,
          OrderContainer.CustomerInfo.GeoPosition.Longitude AS restaurant_lng,
          GENERATE_UUID() AS customer_id,
          OrderContainer.RestaurantInfo.Latitude AS customer_lat,
          OrderContainer.RestaurantInfo.Longitude AS customer_lng,
          EXTRACT(TIME FROM Timestamp) AS `timestamp`
        FROM
          `just-data.production_je_justsaying.orderresolvedandacceptedv2_uk_*`
        WHERE
          DATE(_PARTITIONTIME) >= DATE("{date}")
          AND TIME(Timestamp) >= TIME(6, 0, 0)
          AND CAST(RestaurantId AS STRING) IN ({_comma_separated})
          AND OrderContainer.CustomerInfo.GeoPosition.Latitude IS NOT NULL
          AND OrderContainer.CustomerInfo.GeoPosition.Longitude IS NOT NULL
          AND OrderContainer.RestaurantInfo.Latitude IS NOT NULL
          AND OrderContainer.RestaurantInfo.Longitude IS NOT NULL
    """)  # noqa

    _map = lambda x: timedelta(
        hours=x.hour,
        minutes=x.minute,
        seconds=x.minute)

    rows.timestamp = rows.timestamp.apply(_map)

    restaurants = [
        Restaurant(
            cell['restaurant_id'],
            cell['restaurant_lat'],
            cell['restaurant_lng'])
        for cell in rows[[
            'restaurant_id',
            'restaurant_lat',
            'restaurant_lng']]
        .drop_duplicates(subset='restaurant_id')
        .to_dict(orient='records')
    ]

    rows = rows.to_dict(orient='records')

    customers = [
        Customer(
            cell['customer_id'],
            cell['customer_lat'],
            cell['customer_lng'])
        for cell in rows
    ]

    sessions = [
        Session(
            cell['customer_id'],
            cell['restaurant_id'],
            cell['timestamp'])
        for cell in rows
    ]

    return restaurants, customers, sessions, []


def skip_load_agents(date: datetime.date, *args: str) -> Tuple[
        List[Restaurant], List[Customer], List[Session], List[Courier]]:
    """Load agents."""

    _comma_separated = ','.join([f'"{arg}"' for arg in args])

    rows = read_gbq(f"""
        WITH

        zones AS (
          SELECT
            sys_delivery_zone_id
          FROM
            `just-data-warehouse.delco_analytics_team_dwh.dim_courier_delivery_zones`
          WHERE
            zone_name IN ( {_comma_separated} ) ),
        
        orders AS (
          SELECT
            sys_resto_id AS restaurant_id,
            GENERATE_UUID() AS customer_id,
            custo_lat AS customer_lat,
            custo_long AS customer_lng,
            EXTRACT(TIME FROM order_datetime) AS `timestamp`
          FROM
            `just-data-warehouse.delco_analytics_team_dwh.fact_orders_resto`
          WHERE
            tenant_id = "ca"
            AND order_date = DATE("{date}")
            AND EXTRACT(TIME FROM order_datetime) >= TIME(6, 0, 0)
            AND sys_delivery_zone_id IN (SELECT * FROM zones)
            AND order_status = 'COMPLETED'
            AND order_type = 'DELIVERY' )
        
        SELECT
          o.restaurant_id,
          r.location_latitude AS restaurant_lat,
          r.location_longitude AS restaurant_lng,
          o.customer_id,
          o.customer_lat,
          o.customer_lng,
          o.timestamp
        FROM
          orders o
        INNER JOIN
          `just-data-warehouse.delco_analytics_team_dwh.dim_resto`  r
        ON
          o.restaurant_id = r.sys_Resto_id
        WHERE
          r.location_latitude IS NOT NULL
          AND r.location_longitude IS NOT NULL
          AND o.customer_lat IS NOT NULL
          AND o.customer_lng IS NOT NULL 
    """)

    _map = lambda x: timedelta(
        hours=x.hour,
        minutes=x.minute,
        seconds=x.minute)

    rows.timestamp = rows.timestamp.apply(_map)

    restaurants = [
        Restaurant(
            cell['restaurant_id'],
            cell['restaurant_lat'],
            cell['restaurant_lng'])
        for cell in rows[[
            'restaurant_id',
            'restaurant_lat',
            'restaurant_lng']]
        .drop_duplicates(subset='restaurant_id')
        .to_dict(orient='records')
    ]

    rows = rows.to_dict(orient='records')

    customers = [
        Customer(
            cell['customer_id'],
            cell['customer_lat'],
            cell['customer_lng'])
        for cell in rows
    ]

    sessions = [
        Session(
            cell['customer_id'],
            cell['restaurant_id'],
            cell['timestamp'])
        for cell in rows
    ]

    rows = read_gbq(f"""
        WITH
        
        zones AS (
          SELECT
            sys_delivery_zone_id,
            center_lat AS lat,
            center_long AS lng
          FROM
            `just-data-warehouse.delco_analytics_team_dwh.dim_courier_delivery_zones`
          WHERE
            tenant_id = "ca"
            AND zone_name IN ( {_comma_separated} ) )
        
        SELECT
          GENERATE_UUID() AS courier_id,
          lat,
          lng,
          EXTRACT(TIME FROM start_date) AS start_time,
          EXTRACT(TIME FROM end_date) AS end_time
        FROM
          `just-data-warehouse.clean_skip_data_lake.courier_shifts_courier_shifts_ca` s
        INNER JOIN
          zones z
        ON
          s.delivery_zone_id = z.sys_delivery_zone_id
        WHERE
          tenant_id = "ca"
          AND DATE(start_date) = "{date}"
          AND EXTRACT(TIME FROM start_date) >= TIME(6, 0, 0)
          AND start_date IS NOT NULL
          AND end_date IS NOT NULL
          AND start_date < end_date
          AND shift_type = "REGULAR"
    """)  # noqa

    rows.start_time = rows.start_time.apply(_map)
    rows.end_time = rows.end_time.apply(_map)

    # TODO overflow
    idx = rows.start_time > rows.end_time
    rows.loc[idx, 'end_time'] += timedelta(1)

    rows = rows.to_dict(orient='records')

    couriers = [
        Courier(
            row['courier_id'],
            row['lat'],
            row['lng'],
            row['start_time'],
            row['end_time']
        )
        for row in rows
    ]

    for row in rows:
        Courier(
            row['courier_id'],
            row['lat'],
            row['lng'],
            row['start_time'],
            row['end_time']
        )

    return restaurants, customers, sessions, couriers
