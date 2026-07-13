from dataclasses import dataclass, field
from datetime import datetime
import uuid
from typing import Optional

@dataclass
class Project:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    description: str = ""
    owner_id: str = ""
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    
    def update(self, name: Optional[str] = None, description: Optional[str] = None):
        if name:
            self.name = name
        if description:
            self.description = description
        self.updated_at = datetime.utcnow()
