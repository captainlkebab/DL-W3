from crewai import Agent, Crew, Process, Task
from langchain_groq import ChatGroq
from learning_types import LearningProfile, LearningPlan
import os
import yaml

class TheoryExpertCrew:
    def __init__(self, learning_profile: LearningProfile):
        self.learning_profile = learning_profile
        self.llm = ChatGroq(
            temperature=0.7,
            # model_name="groq/llama-3.3-70b-versatile"
            # model_name="groq/llama2-70b-4096"
            # model_name="groq/gemma-7b-it"
            model_name="groq/llama-3.3-70b-versatile"
        )
        self.config_path = os.path.join(os.path.dirname(__file__), "config")
        
        # Lade Konfigurationsdateien
        with open(os.path.join(self.config_path, "agents.yaml"), 'r') as f:
            self.agents_config = yaml.safe_load(f)
        with open(os.path.join(self.config_path, "tasks.yaml"), 'r') as f:
            self.tasks_config = yaml.safe_load(f)
            
        # Erstelle Agents beim Initialisieren
        self.agents = self.create_agents()

    def create_agents(self) -> dict[str, Agent]:
        agents = {}
        for agent_name, config in self.agents_config.items():
            agent = Agent(
                role=config["role"],
                goal=config["goal"],
                backstory=config["backstory"],
                allow_delegation=False,
                llm=self.llm
            )
            agents[agent_name] = agent
        return agents

    def get_tasks(self) -> list[Task]:
        tasks = []
        for task_config in self.tasks_config.values():
            agent_name = task_config["agent"]
            if agent_name not in self.agents:
                raise ValueError(f"Agent {agent_name} not found")
                
            tasks.append(
                Task(
                    description=task_config["description"],
                    expected_output=task_config["expected_output"],
                    agent=self.agents[agent_name]
                )
            )
        return tasks

    def crew(self) -> Crew:
        return Crew(
            agents=list(self.agents.values()),
            tasks=self.get_tasks(),
            process=Process.sequential,
            verbose=True
        ) 