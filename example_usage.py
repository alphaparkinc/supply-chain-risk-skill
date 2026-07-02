"""
example_usage.py -- Demonstrates the SupplyChainRiskClient SDK.
"""
from client import SupplyChainRiskClient

def main():
    client = SupplyChainRiskClient()

    # Scenario 1: High-risk supply chain
    print("[1] High-Risk Supply Chain Analysis")
    suppliers = [
        {"name": "Guangzhou Electronics Co", "country": "CN", "lead_time_days": 45, "reliability_score": 0.78, "category": "electronics"},
        {"name": "Shenzhen Parts Ltd", "country": "CN", "lead_time_days": 60, "reliability_score": 0.82, "category": "components"},
        {"name": "Hong Kong Logistics", "country": "CN", "lead_time_days": 30, "reliability_score": 0.90, "category": "logistics"},
    ]
    result = client.analyze(
        suppliers=suppliers,
        inventory_days=25,
        single_source_categories=["electronics"],
    )
    print(f"Risk Score: {result['risk_score']}/100")
    print(f"Risk Level: {result['risk_level']}")
    print("Risk Factors:")
    for f in result["risk_factors"]:
        print(f"  {f['factor']:<30} Score: {f['score']:.1f}/100 (weight: {f['weight']*100:.0f}%)")
    print("\nTop Recommendations:")
    for i, rec in enumerate(result["recommendations"][:5], 1):
        print(f"  {i}. {rec}")

    # Scenario 2: Well-diversified supply chain
    print("\n[2] Low-Risk Diversified Supply Chain")
    suppliers2 = [
        {"name": "US Manufacturer A", "country": "US", "lead_time_days": 14, "reliability_score": 0.95, "category": "apparel"},
        {"name": "Portugal Factory B", "country": "PT", "lead_time_days": 21, "reliability_score": 0.92, "category": "apparel"},
        {"name": "Mexico Assembly C", "country": "MX", "lead_time_days": 18, "reliability_score": 0.88, "category": "accessories"},
        {"name": "India Textiles D", "country": "IN", "lead_time_days": 25, "reliability_score": 0.87, "category": "fabric"},
    ]
    result2 = client.analyze(suppliers=suppliers2, inventory_days=90)
    print(f"Risk Score: {result2['risk_score']}/100 | Risk Level: {result2['risk_level']}")

if __name__ == "__main__":
    main()
