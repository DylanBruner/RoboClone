from security.classprotection import SecurityManager

from security.secureloader import SecureLoader
from ui.battle.battlefield import BattleField
from ui.battle.battleview import BattleView
from ui.battlecreator import BattleCreator

# ==================== SECURITY SETUP ====================
NEEDS_BYPASS = [SecureLoader, BattleField, BattleView, BattleCreator]

# ================== END SECURITY SETUP ==================

for cls in NEEDS_BYPASS:
    SecurityManager.addBypass(cls)

SecurityManager.enable()