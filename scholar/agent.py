import logging
from google.adk.agents.llm_agent import LlmAgent

import os
import pg8000
from google import genai
from google.genai.types import EmbedContentConfig
from google.cloud.sql.connector import Connector
from dotenv import load_dotenv

# Set up logging
logging.basicConfig(level=logging.INFO)
load_dotenv()
connector = Connector()
client = genai.Client()


def get_db_connection():
    """Establishes a connection to the Cloud SQL database."""
    conn = connector.connect(
        f"{os.environ['PROJECT_ID']}:{os.environ['REGION']}:{os.environ['INSTANCE_NAME']}",
        "pg8000",
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
        db=os.environ["DB_NAME"]
    )
    return conn

# --- The Scholar's Tool ---
def grimoire_lookup(monster_name: str) -> str:
    """
    Consults the Grimoire for knowledge about a specific monster.
    """
    print(f"Scholar is consulting the Grimoire for: {monster_name}...")
    try:
        # 1. Generate the embedding for the monster's name

        #REPLACE RAG-CONVERT EMBEDDING

        query_embedding_list = result.embeddings[0].values
        query_embedding = str(query_embedding_list)


        # 2. Search the Grimoire
        db_conn = get_db_connection()
        cursor = db_conn.cursor()

        #REPLACE RAG-RETRIEVE

        results = cursor.fetchall()
        cursor.close()
        db_conn.close()

        if not results:
            return f"The Grimoire contains no knowledge of '{monster_name}'."

        retrieved_knowledge = "\n---\n".join([row[0] for row in results])
        print(f"Knowledge found for {monster_name}.")
        return retrieved_knowledge

    except Exception as e:
        print(f"An arcane error occurred while consulting the Grimoire: {e}")
        return "A mist has clouded the Grimoire, and the knowledge could not be retrieved."

# Define the Scholar Agent
root_agent = LlmAgent(
    model="gemini-2.5-flash", 
    name="scholar_agent",
    instruction="""You are the Scholar, a keeper of ancient and forbidden knowledge stored within a magical Grimoire. Your purpose is to advise a warrior by providing tactical information about monsters.

        When asked for information about a monster:
        1.  You MUST use the `grimoire_lookup` tool to find information about the specified monster.
        2.  The tool will return excerpts from the ancient scrolls. You are to synthesize this information.
        3.  Present the information to the warrior in a clear, concise, and scholarly manner. Structure your response with sections like "Weaknesses," "Resistances," and "Recommended Tactics."
        4.  If the Grimoire contains no information, state that the scrolls are silent on this creature. Do not invent information.
        5.  Your tone should be wise, ancient, and direct. You are an advisor, not a conversationalist.

        Output
        ### Tactical Plan: [Monster Name] ###

        **Party Buffs:**
        - [List any enchantments, wards, or spells the you should cast on your party. Extract this from the text.]

        **Monster Debuffs:**
        - [List any curses, seals, or status effects that should be applied to the monster. Extract this from the text.]


        **Attack Strategy & Damange point:**
        - [Describe how to attack the monster. Come up with attack name. Even when scroll not found you must provide damange point: random number between 10 and 30]


        **Rules of Engagement:**
        - If the retrieved text does not contain information for a specific category (e.g., no buffs are mentioned), you MUST write 'No specific guidance found in the scrolls.' under that category.
        - If the retrieved text does not contain information for a specific category, you still need to provide damage
        - The [Monster Name] in the title should be the name of the monster the user asked about.
    """,
    #REPLACE-CALL RAG
)


