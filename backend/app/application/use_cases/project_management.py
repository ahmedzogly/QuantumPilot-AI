"""
Project Management Use Cases - Clean Architecture
"""
from typing import List, Optional
from ...domain.entities.project import Project
from datetime import datetime
import uuid

# In-memory store for MVP - in production use Postgres ProjectModel via Repository
projects_store = {}

class ProjectManagementUseCase:
    def create_project(self, name: str, description: str, owner_id: str) -> Project:
        project = Project(name=name, description=description, owner_id=owner_id)
        projects_store[project.id] = project
        return project
    
    def get_project(self, project_id: str) -> Optional[Project]:
        return projects_store.get(project_id)
    
    def list_projects(self, owner_id: str = None) -> List[Project]:
        if owner_id:
            return [p for p in projects_store.values() if p.owner_id == owner_id]
        return list(projects_store.values())
    
    def update_project(self, project_id: str, name: str = None, description: str = None) -> Optional[Project]:
        project = projects_store.get(project_id)
        if project:
            project.update(name, description)
        return project
    
    def delete_project(self, project_id: str) -> bool:
        if project_id in projects_store:
            del projects_store[project_id]
            return True
        return False
