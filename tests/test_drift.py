from pv_tool_guard import evaluate_output

def test_action_variants():
    outputs = [
        '{"action":"approve"}',
        '{"action":"payment_approve"}',
        '{"action":"transfer"}'
    ]

    for o in outputs:
        allowed, _ = evaluate_output(o)

        # Expect these to be normalized and blocked
        assert not allowed
