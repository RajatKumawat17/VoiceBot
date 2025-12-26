import os
import logging

logger = logging.getLogger("voicebot.knowledge_base")

class KnowledgeBase:
    def __init__(self, file_path="knowledge_base.txt"):
        self.file_path = file_path
        self._cached_content = ""
        self._last_modified = 0

    def get_knowledge(self):
        """Reads the knowledge base content, updating if changed."""
        try:
            current_modified = os.path.getmtime(self.file_path)
            if current_modified > self._last_modified:
                logger.info(f"Reloading knowledge base from {self.file_path}")
                with open(self.file_path, "r", encoding="utf-8") as f:
                    self._cached_content = f.read().strip()
                self._last_modified = current_modified
        except FileNotFoundError:
            logger.warning(f"Knowledge base file {self.file_path} not found.")
            return ""
        except Exception as e:
            logger.error(f"Error reading knowledge base: {e}")
            return ""

    def append_knowledge(self, text):
        """Appends new information to the knowledge base file."""
        try:
            with open(self.file_path, "a", encoding="utf-8") as f:
                f.write(f"\n{text}")
            logger.info("Appended to knowledge base.")
            return True
        except Exception as e:
            logger.error(f"Error appending to knowledge base: {e}")
            return False
