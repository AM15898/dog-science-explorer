from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT))

from data_pipeline.query_registry import load_query_registry


registry = load_query_registry()

print()

for family, queries in registry.items():
    print(f"{family:20} {len(queries)} queries")

print()

total = sum(len(v) for v in registry.values())

print(f"Total families : {len(registry)}")
print(f"Total queries  : {total}")