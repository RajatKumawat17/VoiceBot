import os
import logging

logger = logging.getLogger("voicebot.prompt_manager")

class PromptManager:
    def __init__(self, file_path="system_prompt.txt"):
        self.file_path = file_path
        self._cached_prompt = ""
        self._last_modified = 0

    def get_prompt(self):
        """Reads the system prompt from the file, updating if changed."""
        try:
            current_modified = os.path.getmtime(self.file_path)
            if current_modified > self._last_modified:
                logger.info(f"Reloading system prompt from {self.file_path}")
                with open(self.file_path, "r", encoding="utf-8") as f:
                    self._cached_prompt = f.read().strip()
                self._last_modified = current_modified
        except FileNotFoundError:
            logger.warning(f"System prompt file {self.file_path} not found. Using default.")
            return "You are a helpful assistant."
        except Exception as e:
            logger.error(f"Error reading system prompt: {e}")
        
        return self._cached_prompt
