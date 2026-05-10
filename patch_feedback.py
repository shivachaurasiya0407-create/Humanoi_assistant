from pathlib import Path

path = Path('automation/feedback_loop.py')
text = path.read_text(encoding='utf-8')
needle = '    def get_action_history(self) -> List[Dict[str, Any]]:\n        """Get history of actions and their verification results."""\n        return self.action_history.copy()\n'
idx = text.find(needle)
if idx == -1:
    raise SystemExit('needle not found')
insert = '    def get_recent_feedback(self, limit: int = 10) -> List[Dict[str, Any]]:\n        """Return recent verification feedback entries."""\n        return self.action_history[-limit:]\n\n'
new_text = text[: idx + len(needle)] + insert + text[idx + len(needle) :]
path.write_text(new_text, encoding='utf-8')
print('patched')
