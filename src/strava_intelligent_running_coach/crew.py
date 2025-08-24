import os
from crewai import LLM
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import (
	ScrapeWebsiteTool
)
from crewai.project import before_kickoff
import requests
from stravalib.client import Client
from dotenv import load_dotenv

load_dotenv()


@CrewBase
class StravaIntelligentRunningCoachCrew:
    """StravaIntelligentRunningCoach crew"""

    def get_athlete(self):
        access_token = os.getenv("strava_access_token")
        http_get="https://www.strava.com/api/v3/athlete" 
        response = requests.get(http_get, headers={"Authorization": f"Bearer {access_token}"})
        return response.json()['id']

    def activity(self):
        access_token = os.getenv("strava_access_token")
        activities_access_token = os.getenv("strava_activities_access_token")

        all_activities = []
        page = 1
        
        per_page = 200  # Strava's maximum per page
        
        session = requests.Session()
        session.headers.update({"Authorization": f"Bearer {activities_access_token}"})

        while True:
            url = "https://www.strava.com/api/v3/athlete/activities"
            params = {
                "per_page": per_page,
                "page": page
            }

            # OPTIMIZATION 3: Use session for faster connections
            response = session.get(url, params=params)

            activities = response.json()
            if not activities:
                break  # no more activities

            # OPTIMIZATION 4: Use list comprehension instead of loop
            filtered_activities = [
                {
                    'id': activity.get('id'),
                    'name': activity.get('name'),
                    'type': activity.get('type') == 'Run',
                    'distance': activity.get('distance'),
                    'moving_time': activity.get('moving_time'),
                    'elapsed_time': activity.get('elapsed_time'),
                    'total_elevation_gain': activity.get('total_elevation_gain'),
                    'start_date': activity.get('start_date'),
                    'average_speed': activity.get('average_speed'),
                    'max_speed': activity.get('max_speed'),
                }
                for activity in activities
            ]

            all_activities.extend(filtered_activities)
            page += 1
        return all_activities

    @before_kickoff
    def get_all_activities(self, inputs):
        activities = self.activity()
        inputs['all_strava_data'] = activities
        return inputs
    
    @agent
    def activity_data_fetcher(self) -> Agent:
        
        return Agent(
            config=self.agents_config["activity_data_fetcher"],
            # tools=[
			# 	ScrapeWebsiteTool()
            # ],
            reasoning=False,
            inject_date=True,
            llm=LLM(
                model="gpt-4.1",
                temperature=0.2,
            ),
        )
    
    
    @agent
    def performance_analytics_expert(self) -> Agent:
        
        return Agent(
            config=self.agents_config["performance_analytics_expert"],
            tools=[

            ],
            reasoning=False,
            inject_date=True,
            llm=LLM(
                model="gpt-4.1",
                temperature=0.2,
            ),
        )
    
    # @agent
    # def route_planning_specialist(self) -> Agent:
        
    #     return Agent(
    #         config=self.agents_config["route_planning_specialist"],
    #         tools=[
	# 			ScrapeWebsiteTool()
    #         ],
    #         reasoning=False,
    #         inject_date=True,
    #         llm=LLM(
    #             model="gpt-4o-mini",
    #             temperature=0.7,
    #         ),
    #     )
    
    @agent
    def personalized_running_coach(self) -> Agent:
        
        return Agent(
            config=self.agents_config["personalized_running_coach"],
            tools=[
				# ScrapeWebsiteTool()
            ],
            reasoning=False,
            inject_date=True,
            llm=LLM(
                model="gpt-4.1",
                temperature=0.2,
            ),
        )
    @task
    def fetch_activity_history(self) -> Task:
        return Task(
            config=self.tasks_config["fetch_activity_history"],
           
        )
   
    @task
    def analyze_performance_trends(self) -> Task:
        return Task(
            config=self.tasks_config["analyze_performance_trends"],
        )
    
    @task
    def recommend_training_distances(self) -> Task:
        return Task(
            config=self.tasks_config["recommend_training_distances"],
        )
    
    # @task
    # def generate_route_recommendations(self) -> Task:
    #     return Task(
    #         config=self.tasks_config["generate_route_recommendations"],
    #     )
    
    @task
    def create_personalized_training_plan(self) -> Task:
        return Task(
            config=self.tasks_config["create_personalized_training_plan"],
        )
    

    @crew
    def crew(self) -> Crew:
        """Creates the StravaIntelligentRunningCoach crew"""
        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
        )
