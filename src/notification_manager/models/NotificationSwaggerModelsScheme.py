import apiflask.fields
from loguru import logger

from apiflask import Schema, fields
from apiflask.fields import String, Integer, List, Dict, Boolean
from apiflask.validators import Length, OneOf

from src.notification_manager.models.queue_types import QueueType

message_field = fields.Dict(required=True, description='Data to send')
queue_enum = String(required=True, validate=OneOf([q.value for q in QueueType.__members__.values()]),
                    example='offering.new', description="Queue name to send the notification")


class ServiceNotification(Schema):
    receiver_id = queue_enum
    message = message_field


class UserNotification(Schema):
    receiver_id = String(required=True, description='User ID for notify a user', example='UserID123')
    origin = String(required=True, description='Origin of the notification')
    status = String(required=True, description='Status of the notification')
    type = queue_enum
    predefined = Boolean(required=False, example='true', description='')
    message = message_field


class Notification(Schema):
    id = String(required=True, description='Autogenerated ID for identification')
    action = String(required=True, description='Action for the notification')
    status = String(required=True, description='Status of the notification')
    origin = String(required=True, description='Origin of the notification')
    receptor = String(required=True, description='Destination of the notification')
    data = Dict(description='Contains the data of the notification')
    unread = Boolean(description='True if the notification has not been read, otherwise false')


# ---------------------------------------------QUEUES MODELS-----------------------------------------

class QueueInput(Schema):
    name = queue_enum
    endpoint = String(required=False,
                      description='Specific endpoint for this queue, if not specified, the generic endpoint for this '
                                  'service will be used')


class Queue(QueueInput):
    id = String(required=True, description='Autogenerated id for identification')
    # name = queue_enum
    active = Boolean(required=True, description='Describes if the queue is active to send notifications')


class ServiceInput(Schema):
    name = String(required=True, description='Name for the service', example='service-test')
    endpoint = String(required=True,
                      description='Generic endpoint for this service where the notifications will be sent')


class Service(ServiceInput):
    # service_id = String(required=True, description='Autogenerated ID for identify the Service')
    # name = String(required=True, description='Name of the Service to be identified by humans')
    # queues = QueueList
    queues = List(fields.Nested(Queue))

