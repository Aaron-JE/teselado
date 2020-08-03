from collections import defaultdict

from marshmallow import Schema, fields
from marshmallow.validate import Range


class BaseSchema(Schema):

    topic = fields.Integer(required=True)
    timestamp = fields.TimeDelta('seconds', required=True)


from datetime import timedelta
s = BaseSchema()
s.validate(s.validate({'topic': 2.5, 'k': 3, 'timestamp': timedelta(0)}))


class EmptySchema(BaseSchema):

    pass


class CustomerLanded(BaseSchema):

    customer_id = fields.Integer(required=True)


class CourierShiftUpdatedSchema(BaseSchema):

    courier_id = fields.Integer(required=True)
    start_time = fields.TimeDelta('seconds', required=True)
    end_time = fields.TimeDelta('seconds', required=True)


class OrderPlacedSchema(BaseSchema):

    restaurant_id = fields.Integer(required=True)
    customer_id = fields.Integer(required=True)


class OrderCreatedSchema(BaseSchema):

    order_id = fields.Integer(required=True)


class CourierLocationSchema(BaseSchema):

    courier_id = fields.Integer(required=True)
    courier_lat = fields.Float(
        required=True,
        validate=Range(min=-90.0, max=90.0))
    courier_lng = fields.Float(
        required=True,
        validate=Range(min=-180.0, max=180.0))


class CourierBaseSchema(BaseSchema):

    order_id = fields.Integer(required=True)
    courier_id = fields.Integer(required=True)


class CourierAssignedSchema(CourierBaseSchema):

    pass


class CourierAcceptedSchema(CourierBaseSchema):

    pass


class CourierRejectedSchema(CourierBaseSchema):

    pass


class JobStartedSchema(CourierBaseSchema):

    pass


class CourierWaitingSchema(CourierBaseSchema):

    pass


class OrderReadySchema(CourierBaseSchema):

    pass


class OrderDeliveredSchema(CourierBaseSchema):

    pass


class SchemaRegistry:

    registry = defaultdict(lambda: EmptySchema(), {
        'simulation_started': EmptySchema(),
        'customer_landed': CustomerLanded(),
        'courier_shift_updated': CourierShiftUpdatedSchema(),
        'order_placed': OrderPlacedSchema(),
        'order_created': OrderCreatedSchema(),
        'courier_location': CourierLocationSchema(),
        'courier_assigned': CourierAssignedSchema(),
        'courier_accepted': CourierAcceptedSchema(),
        'courier_rejected': CourierRejectedSchema(),
        'job_started': JobStartedSchema(),
        'courier_waiting': CourierWaitingSchema(),
        'order_ready': OrderReadySchema(),
        'order_delivered': OrderDeliveredSchema()
    })

    @classmethod
    def load(cls, topic, data):
        return cls.registry[topic].load(data)

    @classmethod
    def dump(cls, topic, data):
        return cls.registry[topic].dump(data)
