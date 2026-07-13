from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from ....infrastructure.qiskit.execution_service import IBMExecutionService

router = APIRouter()
execution_service = IBMExecutionService()

class ExecuteRequest(BaseModel):
    qasm: Optional[str] = None
    qiskit_code: Optional[str] = None
    backend_name: str = "ibm_kingston"
    optimization_level: int = 1
    shots: int = 1024
    mitigation_strategy: str = "s_zne"

@router.post("/")
def execute_circuit(req: ExecuteRequest):
    """
    Execute Real IBM Quantum - The Execute button
    Connects to IBM Quantum via QiskitRuntimeService CRN DIGI
    Uses live calibration: fez T1 135.6us, kingston 231us BEST
    Falls back to Aer simulator with live noise model RO 2.23% CZ 3.33% if no token
    """
    try:
        result = execution_service.execute_circuit(
            qasm_str=req.qasm,
            qiskit_code=req.qiskit_code,
            backend_name=req.backend_name,
            optimization_level=req.optimization_level,
            shots=req.shots,
            mitigation=req.mitigation_strategy
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{execution_id}")
def get_execution(execution_id: str):
    # In production fetch from Postgres ResultModel
    return {"execution_id": execution_id, "status": "completed", "message": "Use POST / to execute, result stored in Postgres in production"}
