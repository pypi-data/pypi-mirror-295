import requests
import json 
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from google.cloud import storage
from datetime import datetime
# from .gitlab_manager import GitLabManager
import random

class AIC():
    timestamp = datetime.today().strftime('%Y%m%d')
    
    def __init__(self, api_key, project, workspace, gitlab_namespace=None, pipelines=[], gitlab_token=None, qa=False):
        self.base_url = 'https://prod.jdpower.ai/apis/core/v1' if not qa else 'https://aic.qa.jdpower.com/apis/core/v1'
        self.api_key = api_key
        self.headers = {
            'accept': '*/*',
            'api-key': api_key,
            'Content-Type': 'application/json'
        }
        self.project_id = self.get_project_id(project)
        self.workspace = workspace
        self.workspace_id = self.get_workspace_id(workspace)
        # self.get_data()
        self.pipelines = self.pop_pipelines()
        self.pipeline_configs = self.pop_pipeline_config(pipelines)
        if gitlab_token and gitlab_namespace:
            self.gitlab_manager = GitLabManager(self, gitlab_token=gitlab_token, gitlab_namespace=gitlab_namespace)
            print('Git instance initialized.')
    
    def get_data(self):
        print(f'Project ID: {self.project_id}')
        print(f'Workspace ID: {self.workspace_id}')
        print(f'Drive ID: {self.drive_id}')
    
    
    def get_config(self):
        return self.pipeline_configs
    
    
    def get_project_id(self, project):
        url = f"{self.base_url}/projects"
        response = requests.get(url, headers=self.headers)
        for obj in response.json():
            if obj['name'] == project:
                return obj['$id']
        raise Exception(f'No project with name {project} found')
    
    
    def get_workspace_id(self, workspace):
        url = f"{self.base_url}/projects/{self.project_id}/workspaces"
        response = requests.get(url, headers=self.headers)
        for obj in response.json():
            if obj['name'] == workspace:
                return obj['$id']
        raise Exception(f'No workspace with name {workspace} found')
        

    def pop_pipelines(self):
        """
        Fetch and populate pipelines from the current workspace and store them in the instance's pipelines attribute.
        """
        pipelines = []
        url = f"{self.base_url}/projects/{self.project_id}/workspaces/{self.workspace_id}/jobs"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()  # Check for HTTP errors

        # Extract pipeline names and IDs
        for obj in response.json().get('jobs', []):
            pipeline_name = obj.get('title', 'NO TITLE')
            pipeline_id = obj.get('$id')
            pipelines.append({'name': pipeline_name, 'id': pipeline_id})

        self.pipelines = pipelines
        print(f"Loaded {len(pipelines)} pipelines from workspace '{self.workspace}'.")

        return pipelines

    
    def fetch_pipeline_config(self, pipeline, direct=False):
        """Fetch a single pipeline configuration. Direct flag indicates reading directly from AIC, prior to attribute normalization"""
        name = pipeline['name']
        if direct:
            id = pipeline['$id']
        else:
            id = pipeline['id']
        url = f"{self.base_url}/projects/{self.project_id}/workspaces/{self.workspace_id}/jobs/{id}"
        print(f'Retrieving config for {name}...')
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            data = response.json()
            return {'name': name, 'jobConfig': data['jobConfig'], 'id':data['jobConfig']['$id']}
        else:
            print(f'Failed to fetch {name}: {response.status_code}')
            return None

    
    
    def pop_pipeline_config(self, pipelines):
        """Fetch configurations for the given pipelines in parallel using ThreadPoolExecutor."""
        configs = []
        with ThreadPoolExecutor() as executor:
            pipeline_map = {pipeline_name.upper(): pipeline_name for pipeline_name in pipelines}
            futures = {executor.submit(self.fetch_pipeline_config, pipeline): pipeline['name'] for pipeline in self.pipelines if pipeline['name'].upper() in pipeline_map}
            for future in futures:
                result = future.result()
                if result:
                    configs.append(result)
                else:
                    print(f'Pipeline {futures[future]} not found or failed to fetch.')

        return configs
    
     # Method to push pipeline configs to GitLab
    def push_to_gitlab(self, pipelines=[]):
        """Pushes pipeline configurations to GitLab concurrently."""
        if not pipelines:
            pipelines = self.pipeline_configs
        
        with ThreadPoolExecutor() as executor:
            futures = {
                executor.submit(self.gitlab_manager.push_file_to_repo, config['name'].replace(" ", "_"), 
                                f"{config['name']}.json", 
                                json.dumps(config['jobConfig'], indent=4)): config['name']
                for config in pipelines
            }

            for future in as_completed(futures):
                pipeline_name = futures[future]
                try:
                    future.result()  # Retrieve the result to raise any exceptions that occurred
                except Exception as e:
                    print(f"Failed to push pipeline: {pipeline_name} due to {e}")

            
    @staticmethod
    def push_source_code(AIC_prod, AIC_qa, prod_to_qa=False, qa_to_prod=False, pipelines=[], push_to_branch=False):
        """
        Overwrite pipeline configurations between production and QA based on the specified direction 
        and only for the specified pipelines, with an option to push to a new branch.

        Args:
            AIC_prod: Instance of AIC with production pipeline configurations.
            AIC_qa: Instance of AIC with QA pipeline configurations.
            prod_to_qa: Boolean indicating whether to overwrite QA with production configurations.
            qa_to_prod: Boolean indicating whether to overwrite production with QA configurations.
            pipelines: List of pipeline names that should be processed for pushing configurations.
            push_to_branch: Boolean indicating whether to push to a new branch instead of the main branch.
        """
        if not pipelines:
            raise ValueError("List of pipelines is empty. Please specify tables to push source code.")

        if (prod_to_qa and qa_to_prod) or (not prod_to_qa and not qa_to_prod):
            raise ValueError(f"Incorrect push configuration: prod_to_qa={prod_to_qa}, qa_to_prod={qa_to_prod}.")

        for prod_pipeline in AIC_prod.pipeline_configs:
            prod_name = prod_pipeline['name']
            print(f"Processing Production pipeline: {prod_name}")

            if prod_name not in pipelines:
                print(f"Skipping {prod_name} as it is not in the specified pipelines list.")
                continue

            for qa_pipeline in AIC_qa.pipeline_configs:
                qa_name = qa_pipeline['name']
                print(f"Checking QA pipeline: {qa_name}")

                if qa_name not in pipelines:
                    print(f"Skipping {qa_name} as it is not in the specified pipelines list.")
                    continue

                if prod_name == qa_name:
                    print(f"Found matching pipelines: {prod_name} -> {qa_name}")

                    if prod_to_qa:
                        print(f"Overwriting QA config with Production config for pipeline: {prod_name} -> {qa_name}")
                        original_id = qa_pipeline['jobConfig']['$id']
                        qa_pipeline['jobConfig'] = prod_pipeline['jobConfig']
                        qa_pipeline['jobConfig']['$id'] = original_id

                        for variable in qa_pipeline['jobConfig']['variables']:
                            if variable['id'] == 'QA':
                                variable['value'] = 'True'
                                print(f"Setting QA variable to True for pipeline: {qa_name}")
                                break

                        if push_to_branch:
                            branch_name = f"PUSH_{datetime.now().strftime('%Y%m%d%H%M%S')}"
                            print(f"Creating branch {branch_name} for QA pipeline: {qa_name}")
                            response = AIC_qa.create_pipeline_branch(qa_pipeline)
                            if response:
                                print(f"Successfully pushed to branch: {branch_name}")
                            else:
                                print(f"Failed to push to branch: {branch_name}")
                                print(response)
                        else:
                            print(f"Updating QA pipeline: {qa_name}")
                            AIC_qa.write_config_to_pipeline(qa_pipeline)

                    elif qa_to_prod:
                        print(f"Overwriting Production config with QA config for pipeline: {qa_name} -> {prod_name}")
                        original_id = prod_pipeline['jobConfig']['$id']
                        prod_pipeline['jobConfig'] = qa_pipeline['jobConfig']
                        prod_pipeline['jobConfig']['$id'] = original_id

                        for variable in prod_pipeline['jobConfig']['variables']:
                            if variable['id'] == 'QA':
                                variable['value'] = 'False'
                                print(f"Setting QA variable to False for pipeline: {prod_name}")
                                break

                        if push_to_branch:
                            branch_name = f"PUSH_{datetime.now().strftime('%Y%m%d%H%M%S')}"
                            print(f"Creating branch {branch_name} for Production pipeline: {prod_name}")
                            response = AIC_prod.create_pipeline_branch(prod_pipeline)
                            if response:
                                print(f"Successfully pushed to branch: {branch_name}")
                            else:
                                print(f"Failed to push to branch: {branch_name}")
                        else:
                            print(f"Updating Production pipeline: {prod_name}")
                            AIC_prod.write_config_to_pipeline(prod_pipeline)
                    break  # Stop searching once a match is found
            else:
                print(f'No matching pipelines found for Production pipeline: {prod_name}')


    def write_config_to_pipeline(self, config):
        """
        Upload the given configuration to the corresponding pipeline job.
        
        Args:
            config: Dictionary containing the pipeline configuration and name.
        """
        # Extract the job ID and configuration details
        job_id = config.get('id')  # Ensure 'id' is part of the config dictionary
        job_config = config['jobConfig']
        name = config['name']
        
        # Construct the upload URL
        url = f"{self.base_url}/projects/{self.project_id}/workspaces/{self.workspace_id}/jobs"
        

        try:
            # Send the request to update the pipeline configuration
            response = requests.post(url, headers=self.headers, json=job_config)
            response.raise_for_status()  # Check for HTTP errors
            print(f"Successfully updated the pipeline: {name}")
            if response.json()['jobId'] != job_id:
                print('PUSH CONFIGURATION INCORRECT. REVIEW DESTINATION TABLE')
        except requests.exceptions.HTTPError as err:
            print(f'HTTP error occurred while updating pipeline {name}: {err}')
            print(f'Status Code: {response.status_code}')
            print(f'Response Text: {response.text}')
        except Exception as err:
            print(f'Other error occurred while updating pipeline {name}: {err}')
        return None


    def create_pipeline_branch(self, config):
        """
        Create a new branch for the given pipeline configuration using a timestamp-based name format.

        Args:
            config: Dictionary containing the pipeline configuration and name.
        """
        # Extract necessary identifiers and job configuration details
        job_id = config.get('id')
        job_config = config['jobConfig']
        name = config['name']

        # Construct the URL for creating a new branch
        url = f"{self.base_url}/projects/{self.project_id}/workspaces/{self.workspace_id}/interactive-pipeline/{job_id}/branches"

        # Generate a branch name using the current timestamp in the format YYYYMMDDHHMMSS
        branch_name = f"PUSH_{datetime.now().strftime('%Y%m%d%H%M%S')}"

        # Prepare the payload using the job configuration
        payload = {
            'name': branch_name,
            'config': job_config  # Pass the entire job config as required
        }

        try:
            # Send the request to create a new branch
            response = requests.put(url, headers=self.headers, json=payload)
            response.raise_for_status()  # Check for HTTP errors
            print(f"Successfully created a new branch for the pipeline: {name}")
        except requests.exceptions.HTTPError as err:
            print(f'HTTP error occurred while creating branch for pipeline {name}: {err}')
            print(f'Status Code: {response.status_code}')
            print(f'Response Text: {response.text}')
        except Exception as err:
            print(f'Other error occurred while creating branch for pipeline {name}: {err}')

        return response
    

    def get_pipelines(self, workspace_id):
        """
        Retrieve all pipelines in the specified workspace.

        Args:
            workspace_id (str): Workspace ID to retrieve pipelines from.
        """
        url = f"{self.base_url}/projects/{self.project_id}/workspaces/{workspace_id}/jobs"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return [{'name': obj.get('title', 'NO TITLE'), 'id': obj['$id']} for obj in response.json().get('jobs', [])]
    

    def copy_pipelines(self, target_workspace_name, pipelines_to_copy):
        """
        Copy pipelines from the current workspace to the target workspace.

        Args:
            target_workspace_name (str): Name of the target workspace.
            pipelines_to_copy (list): List of pipeline names to copy.
        """
        # Get the target workspace ID using the workspace name
        target_workspace_id = self.get_workspace_id(target_workspace_name)

        # Fetch the existing pipelines in the target workspace
        target_pipelines = self.get_pipelines(target_workspace_id)
        target_pipeline_names = {pipeline['name']: pipeline['id'] for pipeline in target_pipelines}

        for pipeline_name in pipelines_to_copy:
            # Fetch the pipeline config from the source workspace
            pipeline = next((p for p in self.pipelines if p['name'] == pipeline_name), None)
            if not pipeline:
                print(f"Pipeline '{pipeline_name}' not found in the source workspace.")
                continue

            pipeline_config = self.fetch_pipeline_config(pipeline)

            if not pipeline_config:
                print(f"Failed to fetch configuration for pipeline: {pipeline_name}")
                continue

            # Use the unified create_or_update_pipeline method
            print(f"Copying pipeline '{pipeline_name}' to target workspace '{target_workspace_name}'.")
            self.create_or_update_pipeline(target_workspace_id, pipeline_config)



    def create_or_update_pipeline(self, workspace_id, pipeline_config):
        """
        Create or update a pipeline in the specified workspace.

        Args:
            workspace_id (str): Workspace ID where the pipeline will be created or updated.
            pipeline_config (dict): Configuration of the pipeline to be created or updated.
        """
        url = f"{self.base_url}/projects/{self.project_id}/workspaces/{workspace_id}/jobs"

        # Construct the payload
        payload = {
            'title': pipeline_config['name'],
            'stages': pipeline_config['jobConfig'].get('stages', []),
            'variables': pipeline_config['jobConfig'].get('variables', []),
            'sourceStage': pipeline_config['jobConfig'].get('sourceStage', {}),
            'sinkStage': pipeline_config['jobConfig'].get('sinkStage', {}),
            # Include any other necessary fields
        }

        print(f"Attempting to create or update pipeline '{pipeline_config['name']}'")

        try:
            response = requests.post(url, headers=self.headers, json=payload)
            response.raise_for_status()
            print(f"Pipeline '{pipeline_config['name']}' created or updated successfully.")
        except requests.exceptions.HTTPError as err:
            if response.status_code == 409:  # Conflict, indicating pipeline already exists
                print(f"Pipeline '{pipeline_config['name']}' exists, attempting to update.")
                self.update_pipeline(workspace_id, pipeline_config['id'], pipeline_config)
            else:
                print(f'HTTP error occurred while creating or updating pipeline {pipeline_config["name"]}: {err}')
                print(f'Status Code: {response.status_code}')
                print(f'Response Text: {response.text}')

    def update_pipeline(self, workspace_id, pipeline_id, pipeline_config):
        """
        Update an existing pipeline in the specified workspace.

        Args:
            workspace_id (str): Workspace ID where the pipeline will be updated.
            pipeline_id (str): Pipeline ID of the pipeline to be updated.
            pipeline_config (dict): Updated configuration of the pipeline.
        """
        url = f"{self.base_url}/projects/{self.project_id}/workspaces/{workspace_id}/jobs/{pipeline_id}"

        # Reuse the create payload for updates
        payload = {
            'title': pipeline_config['name'],
            'stages': pipeline_config['jobConfig'].get('stages', []),
            'variables': pipeline_config['jobConfig'].get('variables', []),
            'sourceStage': pipeline_config['jobConfig'].get('sourceStage', {}),
            'sinkStage': pipeline_config['jobConfig'].get('sinkStage', {}),
        }

        try:
            response = requests.post(url, headers=self.headers, json=payload)
            response.raise_for_status()
            print(f"Pipeline '{pipeline_config['name']}' updated successfully.")
        except requests.exceptions.HTTPError as err:
            print(f'HTTP error occurred while updating pipeline {pipeline_config["name"]}: {err}')
            print(f'Status Code: {response.status_code}')
            print(f'Response Text: {response.text}')