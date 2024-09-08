import os
import requests
from typing import Dict, Any
from pydantic import BaseModel, Field

BASE_URL = "https://arena-server.clusterprotocol.ai/v1/api"

class JobData(BaseModel):
    model_id: str
    input: dict
    # Add more fields as needed

class ClusterArena:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.environ.get('CLUSTER_ARENA_API_KEY')
        if not self.api_key:
            raise ValueError("No API key found!")
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'cluster-api-key': self.api_key
        })

    def get_jobs(self) -> Dict[str, Any]:
        try:
            response = self.session.get(f"{BASE_URL}/jobs")
            response.raise_for_status()
            return response.json()
        except requests.RequestException as error:
            raise Exception(f"Error fetching jobs: {str(error)}")

    def add_job(self, job_data: JobData) -> Dict[str, Any]:
        try:
            # Pydantic will handle validation
            job_data_dict = job_data.dict()
            response = self.session.post(f"{BASE_URL}/jobs", json=job_data_dict)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as error:
            raise Exception(f"Error adding job: {str(error)}")

    def get_job_details(self, job_id: str) -> Dict[str, Any]:
        try:
            response = self.session.get(f"{BASE_URL}/jobs/{job_id}")
            response.raise_for_status()
            return response.json()
        except requests.RequestException as error:
            raise Exception(f"Error fetching job details: {str(error)}")