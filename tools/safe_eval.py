#your_module/tools/safe_eval.py
import odoo.tools.safe_eval as safe_eval
from opcode import opmap

safe_eval._SAFE_OPCODES.update(set(opmap[x] for x in ['IMPORT_NAME', 'IMPORT_FROM'] if x in opmap))
safe_eval._ALLOWED_MODULES.extend(['requests', 'json'])