import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage
from langchain import OpenAI
from langchain.sql_database import SQLDatabase
#from langchain.chains import SQLDatabaseSequentialChain
from langchain.agents import create_sql_agent,AgentExecutor
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from dotenv import load_dotenv


load_dotenv()

database = os.environ.get('DATABASE')
server = os.environ.get('SERVER')


db = SQLDatabase.from_uri('Driver={SQL Server};' + f'Server={server};Database={database};Trusted_Connection=yes;')
