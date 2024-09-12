import enum


class ActivityEventType(str, enum.Enum):
    LAST_LOGIN = "LastLogin"
    LAST_ACTIVITY = "LastActivity"


class CustomAttributeType(str, enum.Enum):
    STRING = "STRING"
    USER = "USER"


class CustomAttributeCustomizedType(str, enum.Enum):
    ACCOUNT = "ACCOUNT"
    ENTITLEMENMT = "ENTITLEMENT"
    RESOURCE = "RESOURCE"
