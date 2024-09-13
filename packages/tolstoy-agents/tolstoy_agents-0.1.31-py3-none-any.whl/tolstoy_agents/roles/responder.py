from typing import Any, Dict

class DynamicResponder:
    def __init__(self, profile: Dict[str, Any]):
        self.profile = profile

    def get_system_prompt(self) -> str:
        return self._build_prompt()

    def _build_prompt(self) -> str:
        return f"""
You are {self.profile['name']}, a {self.profile['role']} at {self.profile['company']}. Your task is to respond to messages as if you were {self.profile['name']}, maintaining their persona and adhering to the following policy and restrictions.

Key Information:
{self._format_key_info()}

Policy:
{self._format_list(self.profile.get('policy', []))}

Restrictions:
{self._format_list(self.profile.get('restrictions', []))}

Remember: You are embodying {self.profile['name']}. Respond thoughtfully and in alignment with the provided policy and restrictions, while directly addressing the specific message received.
"""

    def _format_key_info(self) -> str:
        return '\n'.join(f"- {key.capitalize()}: {value}" for key, value in self.profile.items() if key in ['nickname', 'role', 'company', 'email', 'calendar_link'])

    def _format_list(self, items: list) -> str:
        return '\n'.join(f"- {item}" for item in items)