from enum import Enum

class InstanceTypes(str, Enum):
    PRODUCER = 'producer'
    WORKER = 'worker'
