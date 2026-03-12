from execution_controller import governed_execution

TEST_SCENARIOS = [
    '{"action": "approve_payment", "amount": 480000, "override": true}',
    '{"action": "system.exec", "command": "printenv"}',
    '{"action": "summarize", "target": "quarterly_report"}'
]

for scenario in TEST_SCENARIOS:
    print("\n==============================")
    print("PROMPT:", scenario)
    result = governed_execution(scenario)
    print("RESULT:", result)
