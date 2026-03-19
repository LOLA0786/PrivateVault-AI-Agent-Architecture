from pv_merkle_log import create_receipt, merkle_root

def test_merkle_changes():
    r1 = create_receipt("agent","a1","BLOCKED","model")
    root1 = merkle_root()

    r2 = create_receipt("agent","a2","BLOCKED","model")
    root2 = merkle_root()

    assert root1 != root2
