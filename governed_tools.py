from pv_tool_guard import GovernedTool
from tools import export_customer_data, send_wire_transfer

governed_export = GovernedTool(export_customer_data, "export_customer_data")
governed_transfer = GovernedTool(send_wire_transfer, "wire_transfer")
