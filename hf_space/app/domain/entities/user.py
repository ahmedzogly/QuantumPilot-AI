from dataclasses import dataclass, field
from datetime import datetime
import uuid
from typing import Optional

@dataclass
class User:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    email: str = ""
    hashed_password: str = ""
    full_name: str = ""
    is_active: bool = True
    is_superuser: bool = False
    created_at: datetime = field(default_factory=datetime.utcnow)
