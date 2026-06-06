import json
from datetime import datetime

def save_report(findings: dict, path: str = "report.json"):
    data = {
        "generated_at": datetime.utcnow().isoformat(),
        "target": findings.get("target", ""),
        "total_findings": sum(len(v) for v in findings.values() if isinstance(v, list)),
        "findings": findings,
    }
    with open(path, "w") as f:
        json.dump(data, f, indent=2)
    print(f"\n[+] Report saved to {path}")

def print_summary(findings: dict):
    print("\n" + "="*50)
    print(f"  SCAN SUMMARY - {findings.get('target', '')}")
    print("="*50)
    for key, value in findings.items():
        if isinstance(value, list) and len(value) > 0:
            print(f"    {key:<30} {len(value)} findings")
    print("="*50 + "\n")