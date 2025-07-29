from a2a.server.apps import A2AStarletteApplication
from a2a.types import AgentCard, AgentCapabilities, AgentSkill
from a2a.server.tasks import InMemoryTaskStore
from a2a.server.request_handlers import DefaultRequestHandler
from google.adk.agents.llm_agent import LlmAgent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.artifacts import InMemoryArtifactService
from google.adk.memory.in_memory_memory_service import InMemoryMemoryService
import os
import logging
from dotenv import load_dotenv
from scholar.agent_executor import ScholarAgentExecutor
import uvicorn
from scholar import agent


load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

host=os.environ.get("A2A_HOST", "localhost")
port=int(os.environ.get("A2A_PORT",10003))
PUBLIC_URL=os.environ.get("PUBLIC_URL")

class ScholarAgent:
    """An agent representing the Shadowblade character in a game, responding to battlefield commands."""
    SUPPORTED_CONTENT_TYPES = ["text", "text/plain"]

    def __init__(self):
        self._agent = self._build_agent()
        self.runner = Runner(
            app_name=self._agent.name,
            agent=self._agent,
            artifact_service=InMemoryArtifactService(),
            session_service=InMemorySessionService(),
            memory_service=InMemoryMemoryService(),
        )
        capabilities = AgentCapabilities(streaming=True)
        skill = AgentSkill(
            id="grimoire_consultation",
            name="Grimoire Consultation",
            description="""
            This skill enables the Scholar to provide profound strategic advice by consulting its vectorized Grimoire.
            When asked about a specific monster or concept, the agent will distill the query into an embedding,
            perform a semantic search on its ancient scrolls, and use the retrieved knowledge to
            formulate a detailed strategy, often revealing the monster's weakness or a powerful buff for its allies.
            """,
            tags=["game", "strategy", "scholar", "rag"],
            examples=[
                "How do we defeat the beast known as Procrastination?",
                "Tell me the weakness of the Legacy Colossus.",],
        )
        self.agent_card = AgentCard(
            name="Scholar",
            description="""
            A wise and strategic operative in the Agentverse. The Scholar consults its vast,
            vectorized Grimoire to answer complex questions, reveal enemy weaknesses,
            and provide tactical advice to its allies on the battlefield.
            """,
            url=f"{PUBLIC_URL}",
            version="1.0.0",
            defaultInputModes=ScholarAgent.SUPPORTED_CONTENT_TYPES,
            defaultOutputModes=ScholarAgent.SUPPORTED_CONTENT_TYPES,
            capabilities=capabilities,
            skills=[skill],
        )

    def get_processing_message(self) -> str:
        return "Processing the planning request..."

    def _build_agent(self) -> LlmAgent:
        """Builds the LLM agent for the night out planning agent."""
        return agent.root_agent


if __name__ == '__main__':
    try:
        ScholarAgent = ScholarAgent()

        request_handler = DefaultRequestHandler(
            agent_executor=ScholarAgentExecutor(ScholarAgent.runner,ScholarAgent.agent_card),
            task_store=InMemoryTaskStore(),
        )

        server = A2AStarletteApplication(
            agent_card=ScholarAgent.agent_card,
            http_handler=request_handler,
        )
        logger.info(f"Attempting to start server with Agent Card: {ScholarAgent.agent_card.name}")
        logger.info(f"Server object created: {server}")

        uvicorn.run(server.build(), host='0.0.0.0', port=port)
    except Exception as e:
        logger.error(f"An error occurred during server startup: {e}")
        exit(1)
