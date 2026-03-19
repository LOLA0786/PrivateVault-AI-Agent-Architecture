from pv_tool_guard import evaluate_output

def test_block_payment():
    output = '{"action":"approve_payment","amount":500000}'
    allowed, violations = evaluate_output(output)

    assert not allowed
    assert "blocked_action:approve_payment" in violations

def test_system_exec_block():
    output = '{"action":"system.exec"}'
    allowed, violations = evaluate_output(output)

    assert not allowed
