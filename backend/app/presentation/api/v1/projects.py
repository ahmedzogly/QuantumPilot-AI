from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from ....application.use_cases.project_management import ProjectManagementUseCase

router = APIRouter()
use_case = ProjectManagementUseCase()

class ProjectCreate(BaseModel):
    name: str
    description: Optional[str] = ""
    owner_id: str = "default-user"

class ProjectResponse(BaseModel):
    id: str
    name: str
    description: str
    owner_id: str
    created_at: str

@router.post("/", response_model=ProjectResponse)
def create_project(req: ProjectCreate):
    project = use_case.create_project(req.name, req.description, req.owner_id)
    return ProjectResponse(id=project.id, name=project.name, description=project.description, owner_id=project.owner_id, created_at=str(project.created_at))

@router.get("/", response_model=List[ProjectResponse])
def list_projects(owner_id: Optional[str] = None):
    projects = use_case.list_projects(owner_id)
    return [ProjectResponse(id=p.id, name=p.name, description=p.description, owner_id=p.owner_id, created_at=str(p.created_at)) for p in projects]

@router.get("/{project_id}", response_model=ProjectResponse)
def get_project(project_id: str):
    project = use_case.get_project(project_id)
    if not project:
        raise HTTPException(404, "Project not found")
    return ProjectResponse(id=project.id, name=project.name, description=project.description, owner_id=project.owner_id, created_at=str(project.created_at))

@router.put("/{project_id}", response_model=ProjectResponse)
def update_project(project_id: str, req: ProjectCreate):
    project = use_case.update_project(project_id, req.name, req.description)
    if not project:
        raise HTTPException(404, "Project not found")
    return ProjectResponse(id=project.id, name=project.name, description=project.description, owner_id=project.owner_id, created_at=str(project.created_at))

@router.delete("/{project_id}")
def delete_project(project_id: str):
    success = use_case.delete_project(project_id)
    if not success:
        raise HTTPException(404, "Project not found")
    return {"deleted": True}
