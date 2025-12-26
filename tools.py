from livekit.agents import llm
import logging
from typing import Annotated
from knowledge_base import KnowledgeBase

logger = logging.getLogger("voicebot.tools")
kb = KnowledgeBase()

# class AgentTools(llm.FunctionContext):
#     @llm.ai_callable(description="Get the current weather for a location")
#     def get_weather(self, location: Annotated[str, llm.TypeInfo(description="The city or location")]):
#         logger.info(f"Getting weather for {location}")
#         # Dummy implementation
#         return f"The weather in {location} is currently sunny and 25 degrees Celsius."
#
#     @llm.ai_callable(description="Add information to the knowledge base")
#     def add_to_knowledge_base(self, info: Annotated[str, llm.TypeInfo(description="The information to add")]):
#         logger.info(f"Adding to KB: {info}")
#         success = kb.append_knowledge(info)
#         if success:
#             return "Successfully added information to the knowledge base."
#         else:
#             return "Failed to add information to the knowledge base."

from livekit.agents import llm
from typing import Annotated
import logging
from knowledge_base import KnowledgeBase

logger = logging.getLogger("voicebot.tools")
kb = KnowledgeBase()

class AgentTools:
    @llm.function_tool(description="Get the current weather for a location")
    def get_weather(self, location: Annotated[str, "The city or location"]):
        logger.info(f"Getting weather for {location}")
        return f"The weather in {location} is currently sunny and 25 degrees Celsius."

    @llm.function_tool(description="Add information to the knowledge base")
    def add_to_knowledge_base(self, info: Annotated[str, "The information to add"]):
        logger.info(f"Adding to KB: {info}")
        success = kb.append_knowledge(info)
        if success:
            return "Successfully added information to the knowledge base."
        else:
            return "Failed to add information to the knowledge base."
