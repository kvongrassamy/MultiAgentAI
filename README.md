# MultiAgentAI
The goal of this repository is to create a multiple agents to accomplish tasks when asked.  They should be able to complete sql query results and manipulate excel files

Front End

- Streamlit will be used as the front end.  There will be a single page because this project is to utilize multiple agents

Agent Orchestration

- Use LangChain to create multiple agents

- Create a master agent for users to chat with and give it tasks to complete

- The master agent would receive those task and pass it to specialized agents.  Specialized agents will be skilled in certain areas, for example an agent will know how to manipulate excel spread sheets and another will run sql queries and produce results

Backend

- Data will be stored in PyMongoDB and will use sample data

- Create a Vector Index in Pymongo DB

Multi Agent Workflow
- Supervisor Agent - This Agent's purpose is to facilitate the sub-agents and whenever their task is complete, he will move to the next agent to complete their task

- MongoDBAgent - This Agent pulls articles from the Mongo DB that is dependant on the users propmt

- WriterAgent - This agent will take the results from the MongoDBAgent findings and store it into a txt file and have it ready for download
![alt text](https://github.com/kvongrassamy/MultiAgentAI/mult_agent_graph.png)


SETUP
- Create vnenv (Python Version: 3.13):
```bash 
py -3.13 -m venv multiagentai
```

- activate the env with 
```bash 
source ./multiagentai/Scripts/activate
```

- install requirements: 
```bash
pip install -r requirements
```

- API Keys Are required: 
```bash
export LANGCHAIN_TRACING_V2=true
export LANGSMITH_API_KEY="YOUR_LANGSMITH_API_KEY"
export OPENAI_API_KEY="YOUR_OPENAI_API_KEY"
export ANTHROPIC_API_KEY="YOUR_ANTHROPIC_API_KEY"
```


-PyMongoDB set up is required:
    - Create a cluster. Create a database named "articles" and a table named "scientific_articles"
    - Create a cluster search atlas index. Instructions how to create one: https://www.mongodb.com/docs/atlas/atlas-vector-search/create-index/#procedure
        - Example: {
                    "fields": [
                        {
                        "numDimensions": 256,
                        "path": "embedding",
                        "similarity": "cosine",
                        "type": "vector"
                        }
                    ]
                    }
    - To load the data the script is in dataset_insert.py

Create a .env file and will need the MONGO_URI:
- MONGO_URI="YOUR MONGO URI CONNECTION STRING"

- In CMD/GitBash/PS run Parlant with: 
```bash
streamlit run sl_ome.py
```

- Once the app is running ask the Supervisor for an article and store it into a text file