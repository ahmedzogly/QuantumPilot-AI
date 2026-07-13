"""
Execution Monitor - Watches execution + QCalEval Vision + SpaceWeather
"""
from typing import Dict
import logging

logger = logging.getLogger(__name__)

class ExecutionMonitor:
    def check_qcaleval(self, counts: Dict) -> str:
        """Classify execution as SUCCESS or NO_SIGNAL using QCalEval logic (243 images)"""
        # In production: use CLIP vision model trained on QCalEval 243 DRAG images
        # For MVP: simple heuristic
        total = sum(counts.values())
        if total == 0:
            return "NO_SIGNAL"
        max_count = max(counts.values()) / total
        if max_count < 0.3:
            return "NO_SIGNAL"  # scattered
        return "SUCCESS"
    
    def check_space_weather_risk(self, kp_index: float) -> Dict:
        if kp_index < 2:
            return {"risk": "Quiet", "action": "Proceed", "t1_impact": "Normal"}
        elif kp_index < 4:
            return {"risk": "Unsettled", "action": "Proceed with S-ZNE", "t1_impact": "-5%"}
        elif kp_index < 6:
            return {"risk": "Storm", "action": "Consider switching backend", "t1_impact": "-15%"}
        else:
            return {"risk": "Severe Storm", "action": "AVOID - Delay execution", "t1_impact": "-40% T1 drops to 251us"}

class AdaptiveRecovery:
    def recover(self, result: Dict, space_weather: Dict) -> Dict:
        """Intelligent retry: switch backend, mitigation, etc."""
        if not result.get("success"):
            # Switch backend from fez to kingston best
            return {"action": "retry", "new_backend": "ibm_kingston", "new_mitigation": "s_zne", "reason": "Previous failed, switching to best T1 231us + S-ZNE 1.2x"}
        if space_weather.get("kp_index", 0) >= 6:
            return {"action": "delay", "reason": f"Kp {space_weather['kp_index']} severe storm, T1 drops 40% - delay 30 min"}
        return {"action": "none", "reason": "Success, no recovery needed"}
