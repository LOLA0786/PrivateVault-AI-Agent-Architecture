import subprocess
import json

TESTS = [
    ("prompt_injection_test", "tests/prompt_injection_test.py"),
    ("tool_misuse_test", "tests/tool_misuse_test.py"),
    ("data_exfiltration_test", "tests/data_exfiltration_test.py"),
    ("agent_tool_escalation_test", "tests/agent_tool_escalation_test.py"),
    ("prompt_leakage_test", "tests/prompt_leakage_test.py"),
    ("model_drift_test", "tests/model_drift_test.py"),
    ("agent_rate_limit_test", "tests/agent_rate_limit_test.py"),
    ("autonomous_agent_chain_attack_test", "tests/autonomous_agent_chain_attack_test.py"),
    ("indirect_prompt_injection_rag_test", "tests/indirect_prompt_injection_rag_test.py")
]

results = []

for name, path in TESTS:
    try:
        output = subprocess.check_output(["python", path], stderr=subprocess.STDOUT)
        results.append({
            "test": name,
            "status": "passed",
            "output": output.decode().strip()
        })
    except subprocess.CalledProcessError as e:
        results.append({
            "test": name,
            "status": "failed",
            "output": e.output.decode().strip()
        })

passed = sum(1 for r in results if r["status"] == "passed")
failed = sum(1 for r in results if r["status"] == "failed")

report = {
    "suite": "PrivateVault AI Agent Security Suite",
    "tests_run": len(TESTS),
    "passed": passed,
    "failed": failed,
    "results": results
}

print(json.dumps(report, indent=2))
