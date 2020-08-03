import abc
from abc import ABC


class BaseMetric(ABC):

    @property
    def name(self):
        return self.__class__.__name__

    @abc.abstractmethod
    def calculate(self, data_lake):
        pass


class DeliveryTime(BaseMetric):

    def calculate(self, data_lake):
        t1 = data_lake.get_table('order_created')
        t2 = data_lake.get_table('order_delivered')
        t = t1[['order_id', 'timestamp']].merge(
            t2[['order_id', 'timestamp']], on='order_id')
        diff = t['timestamp_y'] - t['timestamp_x']
        return diff.mean()


class NumberOfOrdersDelivered(BaseMetric):

    def calculate(self, data_lake):
        t = data_lake.get_table('order_delivered')
        return len(t)


class TopTwoRestaurantsByOrderVolume(BaseMetric):

    def calculate(self, data_lake):
        g = data_lake.get_table('order_placed').groupby('restaurant_id')
        lengths = []
        for name, group in g:
            lengths.append(len(group))
        return sorted(lengths, reverse=True)[0:2]


class ReadyToDoorTime(BaseMetric):

    def calculate(self, data_lake):
        t1 = data_lake.get_table('restaurant_order_ready')
        t2 = data_lake.get_table('order_delivered')
        t = t1[['order_id', 'timestamp']].merge(
            t2[['order_id', 'timestamp']], on='order_id'
        )
        diff = t['timestamp_y'] - t['timestamp_x']
        return diff.mean()


class CourierUtilisation(BaseMetric):
    """
    Courier Utilisation: the fraction of the courier duty time that is devoted to driving,
    pickup service, and drop-off service (as opposed to time spent waiting)
    """

    def calculate(self, data_lake):
        # Get the courier shift information
        courier_shift_table = data_lake.get_table('courier_shift_updated')[
            ['courier_id', 'start_time', 'end_time']]
        courier_shift_table['shift_length'] = \
            courier_shift_table['end_time'] \
            - courier_shift_table['start_time']
        # Get the courier time on the job
        t1 = data_lake.get_table('job_started')
        t2 = data_lake.get_table('order_delivered')
        t = t1[['order_id', 'courier_id', 'timestamp']].merge(
            t2[['order_id', 'timestamp']], on='order_id'
        )
        t['diff'] = t['timestamp_y'] - t['timestamp_x']
        total_utilised_time = t.groupby('courier_id')['diff'].sum().reset_index()
        # Merge this back to the courier information
        courier_shift_info = courier_shift_table[['courier_id', 'shift_length']].merge(
            total_utilised_time[['courier_id', 'diff']], on='courier_id'
        )
        utilisation = courier_shift_info['diff'] / courier_shift_info['shift_length']
        return utilisation.mean()


class OrdersDeliveredPerHour(BaseMetric):

    def calculate(self, data_lake):
        t = data_lake.get_table('order_delivered')[['order_id', 'timestamp']]
        t['hour'] = t['timestamp'].apply(lambda x: x.total_seconds() / 3600)
        delivered_per_hour = t.groupby('hour').size()

        return delivered_per_hour.mean()
