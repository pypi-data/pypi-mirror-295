from openagi.agent import Admin
from openagi.worker import Worker
from openagi.actions.files import WriteFileAction, ReadFileAction
from openagi.actions.tools.youtubesearch import YouTubeSearchTool
from openagi.llms.openai import OpenAIModel, OpenAIConfigModel
from openagi.llms.azure import AzureChatOpenAIModel
from openagi.memory import Memory
from openagi.planner.task_decomposer import TaskPlanner
import os

os.environ["AZURE_BASE_URL"] = "https://internkey.openai.azure.com/"
os.environ["AZURE_DEPLOYMENT_NAME"] = "intern-gpt4"
os.environ["AZURE_MODEL_NAME"] = "gpt-4o-mini"
os.environ["AZURE_OPENAI_API_KEY"] = "c66fa9c426a4441f962f8c86b7cf2169"
os.environ["AZURE_OPENAI_API_VERSION"] = "2023-05-15"  # Add this line to set the API version


config = AzureChatOpenAIModel.load_from_env_config()
llm = AzureChatOpenAIModel(config=config)



# just changing my account
# Define the planner
planner = TaskPlanner(
    llm=llm,
    retry_threshold=5
)

# Define the admin
admin = Admin(
    llm=llm,
    planner=planner,
    max_iterations=5,
    memory=Memory(long_term=True, ltm_threshold=0.7),
    output_format="markdown"
)

# Define the worker agent
youtube_agent = Worker(
    role="YoutubeResearchAgent",
    instructions="""
    Strictly follow these steps:
    1. Generate a detailed study plan for the topic the user wants to study. The topics should start from easy and 
    progress in difficulty level. 
    2. For each topic, provide a very brief description and add 1 youtube video link.
    3. Display the whole plan, neatly formatted.
    """,
    actions=[YouTubeSearchTool],
    force_output=True,
    max_iterations=5
)

admin.assign_workers([youtube_agent])

# Run the agent to generate a study plan for Game Theory
admin.run(
    query="""I want a plan to study game theory.""",
    description="""Create a detailed study plan for studying game theory with all major topics listed, 
    along with a reference YouTube video for each topic."""
)
