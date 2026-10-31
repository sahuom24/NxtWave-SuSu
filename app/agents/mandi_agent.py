"""
Mandi Economic Arbitrage & Market Strategy Agent.
Evaluates price spreads, logistics friction, and optimal time-to-market decisions for agricultural produce.
"""
from typing import Dict, Any, List

class MandiArbitrageAgent:
    """
    Formulates commercial and logistics decisions based on real-time APMC price dispersion.
    """

    async def analyze(self, mandi_data: Dict[str, Any]) -> Dict[str, Any]:
        crop = mandi_data.get("crop", "Wheat")
        quantity = mandi_data.get("quantity_quintals", 50.0)
        msp = mandi_data.get("msp_benchmark")
        best_mandi = mandi_data.get("best_net_mandi", {})
        closest_mandi = mandi_data.get("closest_mandi", {})
        arbitrage = mandi_data.get("arbitrage_opportunity")

        modal_price = best_mandi.get("modal_price_qtl", 0)
        msp_comparison = None
        if msp:
            msp_diff = modal_price - msp
            msp_comparison = {
                "msp_rate": msp,
                "current_realized": modal_price,
                "spread_above_msp": msp_diff,
                "status": "PREMIUM_OVER_MSP" if msp_diff >= 0 else "DISTRESS_BELOW_MSP"
            }

        recommendations = []
        if arbitrage:
            recommendations.append({
                "type": "ARBITRAGE_CAPTURE",
                "action": f"Bypass {closest_mandi.get('mandi_name')} and dispatch to {best_mandi.get('mandi_name')}.",
                "financial_gain": f"+₹{arbitrage['extra_net_profit_inr']:,} net profit (after factoring in +{arbitrage['extra_distance_km']} km extra diesel/freight costs)."
            })
        else:
            recommendations.append({
                "type": "LOCAL_SALE",
                "action": f"Sell locally at {closest_mandi.get('mandi_name')}.",
                "financial_gain": f"Closest terminal yields highest net return of ₹{closest_mandi.get('net_price_realized_qtl')}/qtl."
            })

        # Storage vs Immediate Sale Strategy
        if msp_comparison and msp_comparison["status"] == "DISTRESS_BELOW_MSP":
            recommendations.append({
                "type": "WAREHOUSE_RECEIPT_FINANCING",
                "action": "Consider depositing in WDRA-accredited warehouse using Electronic Negotiable Warehouse Receipt (e-NWR) to claim 7% interest subvention loan instead of distress selling below MSP."
            })

        return {
            "agent_name": "Mandi Economic Arbitrage Agent",
            "crop": crop,
            "quantity_quintals": quantity,
            "optimal_market": best_mandi.get("mandi_name"),
            "target_district": best_mandi.get("district"),
            "expected_net_revenue_inr": best_mandi.get("net_revenue"),
            "effective_realized_rate_per_qtl": best_mandi.get("net_price_realized_qtl"),
            "msp_benchmarking": msp_comparison,
            "strategic_recommendations": recommendations,
            "nearby_options_evaluated": len(mandi_data.get("all_nearby_mandis", []))
        }
