"""
supply-chain-risk-skill: Client SDK
Analyze and score supply chain disruption risk for e-commerce operations.
"""

from __future__ import annotations
from typing import Optional

HIGH_RISK_COUNTRIES = {"CN": 45, "RU": 80, "BY": 85, "IR": 90, "MM": 75, "VE": 70}
MODERATE_RISK_COUNTRIES = {"BD": 40, "PK": 45, "NG": 50, "ET": 50, "KH": 35}

RISK_THRESHOLDS = [
    (0,  25, "Low"),
    (25, 50, "Moderate"),
    (50, 75, "High"),
    (75, 100, "Critical"),
]


class SupplyChainRiskClient:
    """
    SDK for analyzing supply chain disruption risk.

    Evaluates:
      - Geographic concentration risk
      - Single-source dependency
      - Supplier reliability
      - Lead time variance
      - Inventory buffer adequacy
    """

    def analyze(
        self,
        suppliers: list[dict],
        inventory_days: float = 30.0,
        single_source_categories: Optional[list[str]] = None,
    ) -> dict:
        """
        Run full supply chain risk analysis.

        Args:
            suppliers: List of dicts with fields:
                - name (str)
                - country (str) -- ISO 2-letter code
                - lead_time_days (int)
                - reliability_score (float) -- 0.0 to 1.0
                - category (str)
            inventory_days: Days of inventory currently on hand.
            single_source_categories: Categories with only one supplier.

        Returns:
            dict with: risk_score, risk_level, risk_factors, recommendations
        """
        if not suppliers:
            return {"risk_score": 100, "risk_level": "Critical", "risk_factors": [], "recommendations": ["Add at least one supplier to analyze."]}

        single_source = single_source_categories or []
        risk_factors = []

        # 1. Geographic concentration
        geo_score, geo_recs = self._geo_risk(suppliers)
        risk_factors.append({"factor": "Geographic Concentration", "score": geo_score, "weight": 0.25, "recommendations": geo_recs})

        # 2. Single-source dependency
        dep_score, dep_recs = self._dependency_risk(suppliers, single_source)
        risk_factors.append({"factor": "Single-Source Dependency", "score": dep_score, "weight": 0.30, "recommendations": dep_recs})

        # 3. Supplier reliability
        rel_score, rel_recs = self._reliability_risk(suppliers)
        risk_factors.append({"factor": "Supplier Reliability", "score": rel_score, "weight": 0.25, "recommendations": rel_recs})

        # 4. Lead time variance
        lt_score, lt_recs = self._lead_time_risk(suppliers)
        risk_factors.append({"factor": "Lead Time Variance", "score": lt_score, "weight": 0.10, "recommendations": lt_recs})

        # 5. Inventory buffer
        inv_score, inv_recs = self._inventory_risk(inventory_days, suppliers)
        risk_factors.append({"factor": "Inventory Buffer", "score": inv_score, "weight": 0.10, "recommendations": inv_recs})

        # Composite risk score (weighted)
        total = sum(f["score"] * f["weight"] for f in risk_factors)
        risk_score = round(min(max(total, 0), 100), 1)

        risk_level = "Low"
        for low, high, label in RISK_THRESHOLDS:
            if low <= risk_score < high:
                risk_level = label
                break

        all_recs = []
        for f in sorted(risk_factors, key=lambda x: x["score"] * x["weight"], reverse=True):
            all_recs.extend(f["recommendations"])

        return {
            "risk_score": risk_score,
            "risk_level": risk_level,
            "risk_factors": risk_factors,
            "recommendations": all_recs[:8],
            "supplier_count": len(suppliers),
            "inventory_days": inventory_days,
        }

    def _geo_risk(self, suppliers: list[dict]) -> tuple[float, list[str]]:
        countries = [s.get("country", "US").upper() for s in suppliers]
        unique_countries = set(countries)
        score = 0.0
        recs = []
        if len(unique_countries) == 1:
            score += 40
            recs.append("Diversify supplier geography across at least 3 countries.")
        elif len(unique_countries) == 2:
            score += 20
        country_counts = {}
        for c in countries:
            country_counts[c] = country_counts.get(c, 0) + 1
        dominant_pct = max(country_counts.values()) / len(countries)
        if dominant_pct > 0.7:
            score += 20
            recs.append(f"Over 70% of suppliers concentrated in one country — reduce dependency.")
        for country in unique_countries:
            country_risk = HIGH_RISK_COUNTRIES.get(country, MODERATE_RISK_COUNTRIES.get(country, 0))
            if country_risk >= 70:
                score += 15
                recs.append(f"Supplier in high-risk country ({country}) — develop alternative source.")
            elif country_risk >= 40:
                score += 8
        return round(min(score, 100), 1), recs

    def _dependency_risk(self, suppliers: list[dict], single_source: list[str]) -> tuple[float, list[str]]:
        score = 0.0
        recs = []
        if single_source:
            score += len(single_source) * 15
            for cat in single_source[:3]:
                recs.append(f"Qualify a backup supplier for '{cat}' category.")
        categories = [s.get("category", "general") for s in suppliers]
        unique_cats = set(categories)
        for cat in unique_cats:
            suppliers_in_cat = [s for s in suppliers if s.get("category") == cat]
            if len(suppliers_in_cat) == 1:
                score += 10
                if cat not in single_source:
                    recs.append(f"Only one supplier for '{cat}' — add a secondary source.")
        return round(min(score, 100), 1), recs

    def _reliability_risk(self, suppliers: list[dict]) -> tuple[float, list[str]]:
        scores = []
        recs = []
        for s in suppliers:
            rel = float(s.get("reliability_score", 0.8))
            scores.append(rel)
            if rel < 0.7:
                recs.append(f"Supplier '{s.get('name', 'Unknown')}' has low reliability ({rel:.0%}) — review or replace.")
            elif rel < 0.85:
                recs.append(f"Supplier '{s.get('name', 'Unknown')}' reliability below benchmark — request improvement plan.")
        avg_rel = sum(scores) / len(scores) if scores else 0.5
        score = round((1 - avg_rel) * 100, 1)
        if avg_rel >= 0.9:
            recs = []  # No issues
        return score, recs

    def _lead_time_risk(self, suppliers: list[dict]) -> tuple[float, list[str]]:
        lead_times = [int(s.get("lead_time_days", 30)) for s in suppliers]
        if not lead_times:
            return 50.0, ["No lead time data provided."]
        avg_lt = sum(lead_times) / len(lead_times)
        max_lt = max(lead_times)
        score = 0.0
        recs = []
        if avg_lt > 60:
            score += 40
            recs.append("Average lead time exceeds 60 days — negotiate shorter terms or air freight options.")
        elif avg_lt > 30:
            score += 20
        if max_lt > 90:
            score += 30
            recs.append(f"Longest lead time is {max_lt} days — develop contingency stock plan.")
        variance = max(lead_times) - min(lead_times) if len(lead_times) > 1 else 0
        if variance > 30:
            score += 15
            recs.append("High lead time variance across suppliers — standardize or buffer accordingly.")
        return round(min(score, 100), 1), recs

    def _inventory_risk(self, inventory_days: float, suppliers: list[dict]) -> tuple[float, list[str]]:
        avg_lead_time = sum(int(s.get("lead_time_days", 30)) for s in suppliers) / max(len(suppliers), 1)
        safety_days = avg_lead_time * 1.5
        score = 0.0
        recs = []
        if inventory_days < avg_lead_time:
            score += 60
            recs.append(f"Inventory ({inventory_days:.0f} days) below lead time ({avg_lead_time:.0f} days) — immediate reorder required.")
        elif inventory_days < safety_days:
            score += 30
            recs.append(f"Inventory buffer below recommended safety stock of {safety_days:.0f} days.")
        elif inventory_days > 180:
            score += 10
            recs.append("Excess inventory (>180 days) — review demand forecasting to reduce holding costs.")
        return round(min(score, 100), 1), recs
