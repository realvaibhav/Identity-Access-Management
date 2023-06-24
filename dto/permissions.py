from enum import Enum


class AccessLevelEnum(str, Enum):
    READ = "READ"
    WRITE = "WRITE"
    ADMIN = "ADMIN"
