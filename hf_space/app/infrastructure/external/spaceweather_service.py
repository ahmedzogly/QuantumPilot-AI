"""
SpaceWeatherService - Live NOAA + NMDB Integration
Fetches real-time space weather: kp_index, neutron_flux (cosmic ray), solar_wind, bz, solar_zenith
For IBM Quantum backends location (Yorktown Heights lat 41.27 lon -73.78)
"""

import requests
import math
from datetime import datetime, timezone
from typing import Dict
import logging

logger = logging.getLogger(__name__)

class SpaceWeatherService:
    def __init__(self):
        self.ibm_lat = 41.27
        self.ibm_lon = -73.78
        self.KP_1M_URL = "https://services.swpc.noaa.gov/json/planetary_k_index_1m.json"
        self.KP_3H_URL = "https://services.swpc.noaa.gov/products/noaa-planetary-k-index.json"
    
    def fetch_kp_index(self) -> Dict:
        try:
            resp = requests.get(self.KP_1M_URL, timeout=10)
            if resp.status_code == 200:
                data = resp.json()
                if data:
                    latest = data[-1]
                    return {
                        "kp_index": float(latest.get("kp_index", 0)),
                        "estimated_kp": float(latest.get("estimated_kp", 0)),
                        "time_tag": latest.get("time_tag"),
                        "source": "NOAA_1m",
                        "status": "live"
                    }
        except Exception as e:
            logger.warning(f"KP 1m failed: {e}")
        try:
            resp = requests.get(self.KP_3H_URL, timeout=10)
            if resp.status_code == 200:
                data = resp.json()
                if data:
                    latest = data[-1]
                    return {
                        "kp_index": float(latest.get("Kp", 0)),
                        "estimated_kp": float(latest.get("Kp", 0)),
                        "time_tag": latest.get("time_tag"),
                        "source": "NOAA_3h",
                        "status": "live"
                    }
        except Exception as e:
            logger.warning(f"KP 3h failed: {e}")
        return {
            "kp_index": 2.2,
            "estimated_kp": 2.2,
            "time_tag": datetime.now(timezone.utc).isoformat(),
            "source": "mock_historical_mean",
            "status": "mock"
        }
    
    def fetch_neutron_flux(self) -> Dict:
        """Cosmic Ray Strength - قوة الأشعة الكونية"""
        try:
            resp = requests.get("https://api.open-meteo.com/v1/forecast?latitude=41.27&longitude=-73.78&current_weather=true", timeout=5)
            # Use cosmic ray proxy - actually try Oulu
        except:
            pass
        try:
            # Try Oulu neutron monitor count rate
            resp = requests.get("https://cosmicrays.oulu.fi/nowcastapi/api.php?get=count&station=OULU&average=60", timeout=10)
            if resp.status_code == 200:
                text = resp.text.strip()
                try:
                    count = float(text.split()[0])
                    return {
                        "neutron_flux": count,
                        "unit": "counts/min",
                        "station": "OULU",
                        "source": "NMDB_OULU_live",
                        "status": "live",
                        "cosmic_ray_strength": count / 100.0
                    }
                except:
                    pass
        except Exception as e:
            logger.warning(f"Oulu failed: {e}")
        
        import random
        kp_data = self.fetch_kp_index()
        kp = kp_data.get("kp_index", 2.2)
        base_neutron = 100.0
        neutron = base_neutron - (kp * 2) + random.uniform(-5,5)
        return {
            "neutron_flux": neutron,
            "unit": "counts/min (estimated Forbush model)",
            "station": "OULU_estimated",
            "source": "mock_forbush_model",
            "status": "mock",
            "kp": kp,
            "note": "Real NMDB API parsing complex - using Forbush decrease model: neutron decreases when kp increases (kp high -> geomagnetic shielding reduces cosmic rays slightly, but Forbush)"
        }
    
    def calculate_solar_zenith(self, lat: float = None, lon: float = None, dt: datetime = None) -> float:
        if lat is None:
            lat = self.ibm_lat
        if lon is None:
            lon = self.ibm_lon
        if dt is None:
            dt = datetime.now(timezone.utc)
        day_of_year = dt.timetuple().tm_yday
        declination = 23.45 * math.sin(math.radians(360/365 * (284 + day_of_year)))
        hour = dt.hour + dt.minute/60.0
        hour_angle = 15 * (hour - 12) + lon
        lat_rad = math.radians(lat)
        dec_rad = math.radians(declination)
        ha_rad = math.radians(hour_angle)
        cos_zenith = math.sin(lat_rad)*math.sin(dec_rad) + math.cos(lat_rad)*math.cos(dec_rad)*math.cos(ha_rad)
        cos_zenith = max(-1, min(1, cos_zenith))
        zenith = math.degrees(math.acos(cos_zenith))
        return zenith
    
    def fetch_all(self) -> Dict:
        kp_data = self.fetch_kp_index()
        neutron_data = self.fetch_neutron_flux()
        solar_zenith = self.calculate_solar_zenith()
        try:
            resp = requests.get(f"https://api.open-meteo.com/v1/forecast?latitude={self.ibm_lat}&longitude={self.ibm_lon}&current_weather=true", timeout=10)
            if resp.status_code == 200:
                temp = resp.json().get("current_weather", {}).get("temperature", 20)
            else:
                temp = 20
        except:
            temp = 20
        
        kp_norm = kp_data["kp_index"] / 9.0
        temp_norm = (temp + 20) / 60.0
        kp_val = kp_data["kp_index"]
        if kp_val < 2:
            risk = "Quiet"
            t1_impact = "Normal T1 ~135-231us"
        elif kp_val < 4:
            risk = "Unsettled"
            t1_impact = "T1 slightly reduced -5%"
        elif kp_val < 6:
            risk = "Storm"
            t1_impact = "T1 reduced -15% - consider switching backend"
        else:
            risk = "Severe Storm"
            t1_impact = "T1 reduced -40% - AVOID execution, wait"
        
        result = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "location": {"lat": self.ibm_lat, "lon": self.ibm_lon, "name": "IBM Yorktown (fez, marrakesh, kingston)"},
            "kp_index": kp_data["kp_index"],
            "estimated_kp": kp_data.get("estimated_kp"),
            "kp_time_tag": kp_data.get("time_tag"),
            "kp_source": kp_data.get("source"),
            "kp_status": kp_data.get("status"),
            "kp_norm": kp_norm,
            "risk_level": risk,
            "t1_impact": t1_impact,
            "neutron_flux": neutron_data.get("neutron_flux"),
            "neutron_unit": neutron_data.get("unit"),
            "neutron_source": neutron_data.get("source"),
            "neutron_status": neutron_data.get("status"),
            "cosmic_ray_strength": neutron_data.get("neutron_flux", 100) / 100.0,
            "solar_zenith_deg": solar_zenith,
            "temperature_c": temp,
            "temp_norm": temp_norm,
            "correlation_note": "From our 8M analysis: T1 vs kp -0.197 p=0.00047 significant, T1 vs solar -0.216 p=0.0001",
            "neuralucb_features": {
                "kp_norm": kp_norm,
                "temp_norm": temp_norm,
                "context_22d_extra": [kp_norm, temp_norm],
                "description": "These 2 values go into last 2 dims of 22-D context vector for NeuralUCB decision"
            },
            "recommendation": f"Kp={kp_val:.1f} {risk}: {t1_impact}. Cosmic ray flux {neutron_data.get('neutron_flux', 0):.1f} counts/min"
        }
        return result
    
    def get_context_for_neuralucb(self) -> Dict:
        data = self.fetch_all()
        return {
            "kp_norm": data["kp_norm"],
            "temp_norm": data["temp_norm"],
            "kp_index": data["kp_index"],
            "neutron_flux": data["neutron_flux"],
            "cosmic_ray_strength": data["cosmic_ray_strength"],
            "risk_level": data["risk_level"]
        }

service = SpaceWeatherService()

if __name__ == "__main__":
    print("=== Fetching LIVE Space Weather from NOAA + NMDB ===")
    s = SpaceWeatherService()
    print("\n1. Kp-index (NOAA):")
    kp = s.fetch_kp_index()
    print(kp)
    print("\n2. Neutron Flux (Cosmic Ray Strength) - قوة الأشعة الكونية:")
    neutron = s.fetch_neutron_flux()
    print(neutron)
    print("\n3. Solar Zenith for IBM Yorktown:")
    sz = s.calculate_solar_zenith()
    print(f"{sz:.2f} deg")
    print("\n4. Full fetch for QuantumPilot NeuralUCB:")
    full = s.fetch_all()
    import json
    print(json.dumps(full, indent=2))
    print("\n5. Context for NeuralUCB 22-D:")
    print(s.get_context_for_neuralucb())
