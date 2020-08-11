full_data = '''
with 
    delivery as (
                SELECT order_id_local, driver_id, driver_assigned_latitude, driver_assigned_longitude, driver_assigned_time_stamp, 
                handle_time, way_to_pick_up_timestamp, driver_completes_delivery_time_stamp 
                FROM `just-data-warehouse.international_reporting.es_delivery_data_013_orders_detail` 
               ),
 rest as(
         SELECT restaurant_key, address_latitude as rlat, address_longitude as rlon  
         FROM `just-data-warehouse.core_ecommerce.restaurant`
         WHERE country_code = 'ES' 

SELECT orders.order_id_local , order_date.order_date_local, order_date.order_datetime_local, 
geo_delivery.delivery_city, geo_delivery.order_latitude, 
 geo_delivery.order_longitude,  order_events.oiw_event_timestamp_utc, 
restaurant.restaurant_key,rlat, rlon, order_events.delivered_event_timestamp_utc, 
order_events.order_accepted_timestamp_utc, order_events.placed_timestamp,driver_assigned_latitude,
 driver_assigned_longitude, driver_assigned_time_stamp, 
handle_time, way_to_pick_up_timestamp, driver_completes_delivery_time_stamp,
 rds.rds_order_flag, driver_id  
 
FROM `just-data-warehouse.opensource_local.orders_es` 
left join
rest
on restaurant.restaurant_key = rest.restaurant_key
left join
delivery
on    orders.order_id_local = delivery.order_id_local
WHERE 
order_status.order_status_good = TRUE
AND order_date.order_date_local > '2020-01-01'
AND geo_delivery.order_latitude is not null
AND geo_delivery.order_longitude is not null
AND rlat is not null
AND rlon is not null
LIMIT 100000
              '''
#TODO añadir peso de orders a rest              

qrestaurants =  '''  
                 SELECT distinct restaurant_key, address_latitude, address_longitude 
                 FROM `just-data-warehouse.core_ecommerce.restaurant`
                 WHERE country_code = 'ES' 
                 AND address_latitude is not null
                 AND address_longitude is not null
                 AND address_city = 'Sevilla'
                 
                 limit 1000000000
                '''              


orders = '''
SELECT orders.order_id_local , order_date.order_date_local, order_date.order_datetime_local, 
geo_delivery.delivery_city, geo_delivery.order_latitude as address_latitude, geo_delivery.order_longitude  as address_longitude
 
FROM `just-data-warehouse.opensource_local.orders_es`  
WHERE 
order_status.order_status_good = TRUE
AND order_date.order_date_local > '2020-01-01'
AND geo_delivery.order_latitude is not null
AND geo_delivery.order_longitude is not null 
AND geo_delivery.delivery_city = 'Sevilla'
LIMIT 100000
'''          