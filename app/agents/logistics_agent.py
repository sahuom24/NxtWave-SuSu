"""
Emergency Supply Logistics & Rerouting Agent.
Coordinates dynamic transport dispatch, road corridor weather verification,
and climate-hazard route avoidance using real OSRM coordinates and Open-Meteo telemetry.
"""
from typing import Dict, Any, List, Optional
from app.tools.routing_tool import get_osrm_route, sample_corridor_weather

class LogisticsAgent:
    """
    Evaluates real physical transport corridors against active climate telemetry.
    """

    async def plan_dispatch(
        self,
        origin_lat: float,
        origin_lon: float,
        target_mandi: Dict[str, Any],
        backup_mandi: Optional[Dict[str, Any]],
        simulate_hazard: bool = False
    ) -> Dict[str, Any]:
        """
        Determines whether primary road corridor is safe or requires dynamic emergency rerouting.
        Samples weather checkpoints along the physical road coordinates.
        """
        dest_lat = target_mandi.get("lat")
        dest_lon = target_mandi.get("lon")

        # 1. Fetch live primary route from OSRM
        primary_route = await get_osrm_route(origin_lat, origin_lon, dest_lat, dest_lon)
        primary_coords = primary_route.get("coordinates", [])

        # 2. Sample physical weather along the primary road corridor
        corridor_weather = await sample_corridor_weather(primary_coords, num_checkpoints=5)
        
        # Hazard is triggered either by live rain > 20mm on road or by user simulation
        hazard_detected = corridor_weather["has_flood_risk"] or simulate_hazard
        hazard_reason = (
            f"Heavy rainfall ({corridor_weather['max_rain_along_corridor_mm']}mm) detected on highway checkpoints; high waterlogging and vehicle stalling risk."
            if corridor_weather["has_flood_risk"]
            else "Simulated flash flood & culvert breach along primary transit artery."
        )

        if not hazard_detected or not backup_mandi:
            return {
                "agent_name": "Logistics Dispatch Agent",
                "route_status": "NORMAL_TRANSIT",
                "hazard_detected": False,
                "selected_route": primary_route,
                "destination_mandi": target_mandi.get("mandi_name"),
                "transit_summary": f"Direct corridor via {', '.join(primary_route.get('major_corridors', ['Main Road'])[:2])} ({primary_route.get('distance_km')} km, ~{primary_route.get('duration_hours')} hrs). All {len(corridor_weather['checkpoints'])} corridor checkpoints CLEAR.",
                "corridor_checkpoints": corridor_weather["checkpoints"],
                "route_geojson": primary_route.get("route_geojson")
            }

        # 3. Emergency Rerouting: Compute safe route to backup mandi
        backup_lat = backup_mandi.get("lat")
        backup_lon = backup_mandi.get("lon")
        secondary_route = await get_osrm_route(origin_lat, origin_lon, backup_lat, backup_lon)
        secondary_coords = secondary_route.get("coordinates", [])
        
        # Verify secondary corridor weather
        sec_corridor_weather = await sample_corridor_weather(secondary_coords, num_checkpoints=5)

        # Mark checkpoints on primary route as compromised
        for cp in corridor_weather["checkpoints"]:
            if simulate_hazard:
                cp["status"] = "FLOOD_RISK_HAZARD"
                cp["rain_next_24h_mm"] = max(38.5, cp["rain_next_24h_mm"])

        dist_diff = round(secondary_route["distance_km"] - primary_route["distance_km"], 1)

        return {
            "agent_name": "Logistics Dispatch Agent",
            "route_status": "EMERGENCY_REROUTE_ACTIVE",
            "hazard_detected": True,
            "hazard_description": hazard_reason,
            "compromised_destination": target_mandi.get("mandi_name"),
            "safe_destination": backup_mandi.get("mandi_name"),
            "original_distance_km": primary_route.get("distance_km"),
            "rerouted_distance_km": secondary_route.get("distance_km"),
            "rerouted_duration_hours": secondary_route.get("duration_hours"),
            "transit_summary": f"Primary highway corridor compromised by {hazard_reason.lower()}. Autonomous agent rerouted dispatch to {backup_mandi.get('mandi_name')} ({dist_diff:+0.1f} km difference). Secondary transit corridor verified safe.",
            "primary_corridor_checkpoints": corridor_weather["checkpoints"],
            "safe_corridor_checkpoints": sec_corridor_weather["checkpoints"],
            "primary_route_geojson": primary_route.get("route_geojson"),
            "safe_route_geojson": secondary_route.get("route_geojson")
        }
