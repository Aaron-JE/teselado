from marshmallow import Schema, fields, validate


timedelta = validate.Regexp(r'[0-9]{2}:[0-9]{2}:[0-9]{2}')
lat = validate.Range(min=-90.0, max=90.0)
lng = validate.Range(min=-180.0, max=180.0)


class RestaurantSchema(Schema):

    id = fields.Str(required=True)
    lat = fields.Float(required=True, validate=lat)
    lng = fields.Float(required=True, validate=lng)
    start_time = fields.String(required=True, validate=timedelta)
    end_time = fields.String(required=True, validate=timedelta)


class CustomerSchema(Schema):

    id = fields.Str(required=True)
    lat = fields.Float(required=True, validate=lat)
    lng = fields.Float(required=True, validate=lng)


class CourierSchema(Schema):

    id = fields.Str(required=True)
    lat = fields.Float(required=True, validate=lat)
    lng = fields.Float(required=True, validate=lng)
    start_time = fields.String(required=True, validate=timedelta)
    end_time = fields.String(required=True, validate=timedelta)


class SimulationSchema(Schema):

    restaurants = fields.List(fields.Nested(RestaurantSchema), required=True)
    customers = fields.List(fields.Nested(CustomerSchema), required=True)
    couriers = fields.List(fields.Nested(CourierSchema), required=True)
