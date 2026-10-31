"""
Agro-Climate Risk Agent.
Specialized autonomous agent analyzing micro-meteorological variables, soil moisture, and crop vulnerabilities.
"""
from typing import Dict, Any, List

class ClimateRiskAgent:
    """
    Evaluates micro-climate telemetry against agronomical thresholds for Indian crops.
    """

    CROP_VULNERABILITY = {
        "Wheat": {
            "rain_tolerance_mm": 15.0,
            "max_humidity_pct": 82.0,
            "soil_saturation_limit": 0.38,
            "critical_stage": "Grain filling & harvesting",
            "pathogens": ["Yellow Rust (Puccinia striiformis)", "Karnal Bunt", "Powdery Mildew"]
        },
        "Paddy": {
            "rain_tolerance_mm": 50.0,
            "max_humidity_pct": 95.0,
            "soil_saturation_limit": 0.48,
            "critical_stage": "Tillering / Maturity",
            "pathogens": ["Bacterial Leaf Blight (Xanthomonas)", "Rice Blast (Pyricularia oryzae)"]
        },
        "Basmati Paddy": {
            "rain_tolerance_mm": 35.0,
            "max_humidity_pct": 90.0,
            "soil_saturation_limit": 0.44,
            "critical_stage": "Flowering / Ripening",
            "pathogens": ["Sheath Blight", "Neck Blast", "Foot Rot"]
        },
        "Onion": {
            "rain_tolerance_mm": 10.0,
            "max_humidity_pct": 75.0,
            "soil_saturation_limit": 0.32,
            "critical_stage": "Bulb development & curing",
            "pathogens": ["Purple Blotch (Alternaria porri)", "Basal Rot (Fusarium)", "Downy Mildew"]
        },
        "Tomato": {
            "rain_tolerance_mm": 12.0,
            "max_humidity_pct": 80.0,
            "soil_saturation_limit": 0.35,
            "critical_stage": "Fruit setting & ripening",
            "pathogens": ["Early Blight", "Late Blight (Phytophthora)", "Leaf Curl Virus"]
        },
        "Cotton": {
            "rain_tolerance_mm": 20.0,
            "max_humidity_pct": 80.0,
            "soil_saturation_limit": 0.36,
            "critical_stage": "Boll opening & picking",
            "pathogens": ["Boll Rot", "Grey Mildew", "Bacterial Blight"]
        },
        "Potato": {
            "rain_tolerance_mm": 15.0,
            "max_humidity_pct": 85.0,
            "soil_saturation_limit": 0.36,
            "critical_stage": "Tuber initiation & bulking",
            "pathogens": ["Late Blight", "Black Scurf", "Common Scab"]
        },
        "Mustard": {
            "rain_tolerance_mm": 10.0,
            "max_humidity_pct": 78.0,
            "soil_saturation_limit": 0.34,
            "critical_stage": "Pod formation & seed filling",
            "pathogens": ["White Rust", "Alternaria Blight", "Downy Mildew"]
        }
    }

    async def analyze(self, weather_data: Dict[str, Any], crop: str = "Wheat") -> Dict[str, Any]:
        """
        Executes autonomous agronomical risk analysis on real-time weather & soil feeds.
        """
        current = weather_data.get("current", {})
        forecast_48h = weather_data.get("forecast_48h", {})
        rain_48h = forecast_48h.get("rainfall_total_mm", 0.0)
        prob_48h = forecast_48h.get("peak_precipitation_prob_pct", 0)
        temp = current.get("temperature_c", 25.0)
        humidity = current.get("humidity_pct", 60.0)
        soil_moist = current.get("soil_moisture_surface", 0.25)

        crop_profile = self.CROP_VULNERABILITY.get(crop, self.CROP_VULNERABILITY["Wheat"])
        
        advisories = []
        action_urgency = "LOW"
        risk_score = 15  # Baseline

        # 1. Rain & Harvest Window Assessment
        if rain_48h > crop_profile["rain_tolerance_mm"] or prob_48h > 70:
            risk_score += 45
            action_urgency = "CRITICAL" if rain_48h > (crop_profile["rain_tolerance_mm"] * 1.5) else "HIGH"
            advisories.append({
                "category": "HARVEST_PROTECTION",
                "urgency": "IMMEDIATE",
                "action": f"Halt harvesting or cover harvested stacks immediately. {rain_48h}mm rain predicted in next 48 hours exceeds crop threshold of {crop_profile['rain_tolerance_mm']}mm.",
                "scientific_rationale": "High moisture leads to grain discolouration, pre-harvest sprouting, and mycotoxin contamination."
            })
            advisories.append({
                "category": "IRRIGATION_CONTROL",
                "urgency": "IMMEDIATE",
                "action": "SUSPEND ALL CANAL & TUBEWELL IRRIGATION.",
                "scientific_rationale": "Upcoming precipitation will satisfy soil water deficit; irrigating now causes waterlogging and root hypoxia."
            })
        else:
            advisories.append({
                "category": "HARVEST_WINDOW",
                "urgency": "NORMAL",
                "action": "Safe 48-hour harvesting and fieldwork window open.",
                "scientific_rationale": f"Rainfall forecast is negligible ({rain_48h}mm, peak prob {prob_48h}%)."
            })

        # 2. Pathogen Risk Assessment
        if humidity > crop_profile["max_humidity_pct"] and temp >= 20.0:
            risk_score += 25
            pathogen_list = ", ".join(crop_profile["pathogens"][:2])
            advisories.append({
                "category": "DISEASE_ALERT",
                "urgency": "HIGH",
                "action": f"Preventative fungicide/biocontrol spray recommended for {pathogen_list}.",
                "scientific_rationale": f"Relative humidity ({humidity}%) and ambient temperature ({temp}°C) create micro-climate conditions favorable to spore germination."
            })

        # 3. Soil Saturation & Tractor Trafficability
        if soil_moist > crop_profile["soil_saturation_limit"]:
            risk_score += 15
            advisories.append({
                "category": "FIELD_TRAFFICABILITY",
                "urgency": "MEDIUM",
                "action": "Avoid heavy combine harvesters or tractor movement in fields.",
                "scientific_rationale": f"Topsoil moisture ({soil_moist} m³/m³) exceeds compaction threshold, risking severe soil compaction and rut formation."
            })

        risk_score = min(100, risk_score)

        return {
            "agent_name": "Agro-Climate Risk Agent",
            "crop": crop,
            "overall_climate_risk_score": risk_score,
            "urgency_level": action_urgency,
            "soil_moisture_status": "SATURATED" if soil_moist > 0.38 else ("OPTIMAL" if soil_moist > 0.20 else "DRY"),
            "advisories": advisories,
            "scientific_context": {
                "crop_critical_stage": crop_profile["critical_stage"],
                "target_pathogens": crop_profile["pathogens"]
            }
        }
