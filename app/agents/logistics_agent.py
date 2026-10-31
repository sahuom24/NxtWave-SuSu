"""
Emergency Supply Logistics & Rerouting Agent.
Coordinates dynamic transport dispatch, road safety verification, and climate-hazard route avoidance.
"""
from typing import Dict, Any, List, Optional
from app.tools.routing_tool import get_osrm_route, plan_emergency_reroute

class LogisticsAgent:
    """
    Evaluates real physical transport corridors against active climate alerts.
    """

    async def plan_dispatch(
        self,
        origin_lat: float,
        origin_lon: float,
        target_mandi: Dict[str, Any],
        backup_mandi: Optional[Dict[str, Any]],
        climate_alert_active: bool,
        hazard_desc: str = "Severe downpour & low-lying waterlogging"
    ) -> Dict[str, Any]:
        """
        Determines whether primary road corridor is safe or requires dynamic emergency rerouting.
        """
        dest_lat = target_mandi.get("lat")
        dest_lon = target_mandi.get("lon")

        # Fetch live primary route from OSRM
        primary_route = await get_osrm_route(origin_lat, origin_lon, dest_lat, dest_lon)

        if not climate_alert_active or not backup_mandi:
            return {
                "agent_name": "Logistics Dispatch Agent",
                "route_status": "NORMAL_TRANSIT",
                "hazard_detected": False,
                "selected_route": primary_route,
                "destination_mandi": target_mandi.get("mandi_name"),
                "transit_summary": f"Direct route via {', '.join(primary_route.get('major_corridors', ['Main Road'])[:2])} ({primary_route.get('distance_km')} km, ~{primary_route.get('duration_hours')} hrs). Safe for vehicle dispatch.",
                "route_geojson": primary_route.get("route_geojson")
            }

        # Emergency Reroute Scenario: primary route has hazard risk
        backup_lat = backup_mandi.get("lat")
        backup_lon = backup_mandi.get("lon")
        reroute_plan = await plan_emergency_reroute(
            origin_lat, origin_lon,
            dest_lat, dest_lon,
            backup_lat, backup_lon,
            hazard_desc
        )

        return {
            "agent_name": "Logistics Dispatch Agent",
            "route_status": "EMERGENCY_REROUTE_ACTIVE",
            "hazard_detected": True,
            "hazard_description": hazard_desc,
            "compromised_destination": target_mandi.get("mandi_name"),
            "safe_destination": backup_mandi.get("mandi_name"),
            "original_distance_km": primary_route.get("distance_km"),
            "rerouted_distance_km": reroute_plan["recommended_safe_route"].get("distance_km"),
            "rerouted_duration_hours": reroute_plan["recommended_safe_route"].get("duration_hours"),
            "transit_summary": reroute_plan["recommendation"],
            "primary_route_geojson": primary_route.get("route_geojson"),
            "safe_route_geojson": reroute_plan["recommended_safe_route"].get("route_geojson")
        }
