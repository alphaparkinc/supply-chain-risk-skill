# supply-chain-risk-skill

> **GenPark AI Agent Skill** — Analyze supply chain disruption risk for e-commerce operations.

## Features

- 5 risk dimensions: Geographic Concentration, Single-Source Dependency, Supplier Reliability, Lead Time Variance, Inventory Buffer
- Weighted composite risk score (0-100)
- Risk levels: Low / Moderate / High / Critical
- Prioritized action recommendations
- Works fully offline — no external APIs needed

## Quick Start

```python
from client import SupplyChainRiskClient

client = SupplyChainRiskClient()
result = client.analyze(
    suppliers=[
        {"name": "Acme Mfg", "country": "CN", "lead_time_days": 45, "reliability_score": 0.80, "category": "electronics"},
    ],
    inventory_days=30,
    single_source_categories=["electronics"],
)
print(f"Risk Score: {result['risk_score']}/100 — {result['risk_level']}")
for rec in result["recommendations"]:
    print(f"  - {rec}")
```

## Installation

```bash
python example_usage.py  # No external dependencies
```

---
Built by [GenPark](https://genpark.ai) | [alphaparkinc](https://github.com/alphaparkinc)
