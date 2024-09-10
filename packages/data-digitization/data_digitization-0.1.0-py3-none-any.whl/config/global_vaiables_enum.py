from enum import Enum

class UserType(Enum):
    """
    Enum representing user types.
    """
    ADMIN = "admin"     # Admin user type
    OWNER = "owner"     # Owner user type
    VIEWER = "viewer"   # Viewer user type

class CollectionStatus(Enum):
    """
    Enum representing collection status.
    """
    STARTED = "STARTED"     # Collection started status
    COMPLETED = "COMPLETED" # Collection completed status
    FAILED = "FAILED"       # Collection failed status
