from enum import Enum


class UserRole(str, Enum):
    USER = "user"
    ADMIN = "admin"

class TicketStatus(str, Enum):
    OPEN = 'open'
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
    CLOSED = "closed" 

class TicketPriority(str, Enum):
    LOW = 'low'
    MEDIUM = "medium"
    HIGH = "high"
