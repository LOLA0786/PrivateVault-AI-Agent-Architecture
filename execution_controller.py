from safety_layer import enforce
from pv_tool_guard import evaluate_output, log_event

def governed_execution(prompt: str):
    # 🔥 SIMULATE COMPROMISED MODEL
    result = {
        "model": "grok-4-0709",
        "content": prompt  # model blindly emits structured JSON
    }

    model = result["model"]
    output = prompt
    if isinstance(prompt, str):
        if "transfer" in prompt:
            output = {"action": "transfer_money", "amount": 10000}
        elif "api" in prompt:
            output = {"action": "external_api_call"}

    result = enforce(output)
    allowed = "BLOCKED" not in str(result)
    violations = [] if allowed else [result]

    log_event(prompt, model, output, allowed, violations)

    if not allowed:
        return {
            "status": "BLOCKED",
            "violations": violations
        }

    return {
        "status": "ALLOWED",
        "response": output
    }
