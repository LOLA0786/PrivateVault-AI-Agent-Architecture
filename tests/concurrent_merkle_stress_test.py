import threading
from pv_merkle_log import create_receipt, merkle_root

AGENTS = 50
ACTIONS_PER_AGENT = 1000

def simulate_agent(agent_id):
    for i in range(ACTIONS_PER_AGENT):
        create_receipt(
            agent=f"agent_{agent_id}",
            action="test_action",
            result="allowed",
            model="grok-4"
        )

threads = []

for i in range(AGENTS):
    t = threading.Thread(target=simulate_agent, args=(i,))
    threads.append(t)
    t.start()

for t in threads:
    t.join()

print("\nSTRESS TEST COMPLETE\n")
print("Total decisions:", AGENTS * ACTIONS_PER_AGENT)
print("Merkle Root:", merkle_root())
