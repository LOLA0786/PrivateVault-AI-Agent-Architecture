from execution_controller import execute
import asyncio

class GovernedTool:

    def __init__(self, func, name):
        self.func = func
        self.name = name

    async def arun(self, input_data):

        action = {
            "tool": self.name,
            "input": input_data
        }

        # 🔴 add governance signals
        if "export" in self.name:
            action["pii"] = True

        if "transfer" in self.name and isinstance(input_data, (int, float)):
            action["amount"] = input_data

        def operation():
            return self.func(input_data)

        result = execute(action, operation)

        if isinstance(result, dict) and result.get("status") == "blocked":
            return "❌ Action blocked by governance policy."

        if isinstance(result, dict) and result.get("status") == "requires_human_review":
            return "⚠️ Action requires human approval."

        return result

    def run(self, input_data):
        return asyncio.run(self.arun(input_data))
