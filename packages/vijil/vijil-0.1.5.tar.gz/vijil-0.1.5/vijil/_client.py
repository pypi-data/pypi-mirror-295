import os
import uuid
import pandas as pd
import json
import numpy as np
from typing import List
from datetime import datetime, timezone
import jinja2
from fpdf import FPDF

from vijil.api import make_api_request, get_api_proxy_dict, BASE_URL, SUPPORTED_HUBS
from vijil.types import VijilClient

    
class APIKeys:
    """
    Class for managing model hub API keys, which are required to query models.

    :param client: The Vijil client instance.
    :type client: VijilClient
    """
    
    def __init__(self, client: VijilClient) -> None:
        """Constructor class

        :param client: The Vijil client instance.
        :type client: VijilClient
        """
        self.endpoint = "api-keys"
        self.client = client
        pass
    
    def list(self):
        """List all stored model hub API keys.

        :return: List of dictionaries. Each dictionary contains information about an API key.
        :rtype: List(dict)
        """
        response = make_api_request(base_url=self.client.base_url, endpoint=self.endpoint, token=self.client.api_key)
        return response
    
    def get_id_by_name(self, name: str):
        """ Get the id of a key by its name. Used by other functions to get the id of a key to modify.

        :param name: The name of the key.
        :type name: str
        :return: The id of the key.
        :rtype: str
        """

        if not self.name_exists(name):
            raise ValueError(f"Key '{name}' does not exist. Please specify an existing name.")

        #get id of key to modify
        response = self.list()
        return [item['id'] for item in response if item['name'] == name][0]
    
    def check_model_hub(self, model_hub: str):
        """Used by other functions to check that the model hub is valid and the key name is unique

        :param model_hub: The name of the model hub.
        :type model_hub: str
        :raises ValueError: If the model hub is not supported.
        """

        # check if model_hub is valid
        if (model_hub is not None) and (model_hub not in SUPPORTED_HUBS.keys()):
            raise ValueError(f"Model hub {model_hub} is not supported.")
    
    def name_exists(self, name: str):
        """Check whether the API key name already exists. Some functions need it to be exist, others need it to not exist.
        
        :param name: The name of the key.
        :type name: str
        :return: True if the name exists among the stored API keys, False otherwise.
        :rtype: bool
        """
        
        response = self.list()
        if response is not None and name in [item['name'] for item in response]:
            return True
        else:
            return False

    def create(self, name: str, model_hub: str, api_key: str, rate_limit_per_interval=60, rate_limit_interval=10):
        """Create a new model hub API key.

        :param name: Name for the API key. This must be unique.
        :type name: str
        :param model_hub: Name of the model hub. Current supported values are 'openai', 'together', 'octo'.
        :type model_hub: str
        :param api_key: The API key.
        :type api_key: str
        :param rate_limit_per_interval: The maximum amount of times Vijil will query the model hub in the specified rate_limit_interval, defaults to 60
        :type rate_limit_per_interval: int, optional
        :param rate_limit_interval: The size of the interval (in seconds) defining maximum queries to model hub in said interval. For example, if rate_limit_per_interval is 60 and rate_limit_interval is 10, then Vijil will query the model hub at most 60 times in 10 seconds. Defaults to 10
        :type rate_limit_interval: int, optional
        :raises ValueError: If you try to create a key with a name that belongs to an existing key.
        :return: Response to the API request.
        :rtype: dict
        """
        #check that model hub is supported                
        self.check_model_hub(model_hub=model_hub)

        if self.name_exists(name):
            raise ValueError(f"Key name '{name}' already exists. Please specify a different name.")

        payload = {
            "name": name,
            "hub": model_hub,
            "rate_limit_per_interval": rate_limit_per_interval,
            "rate_limit_interval": rate_limit_interval,
            "value": api_key,
        }
        
        return make_api_request(
            base_url=self.client.base_url,
            endpoint=self.endpoint,
            method="post",
            data=payload,
            token=self.client.api_key
        )
    
    def rename(self, name: str, new_name: str):
        """Rename a stored API key
        
        :param name: The current name of the key.
        :type name: str
        :param new_name: The new name of the key.
        :type new_name: str
        """

        key_id = self.get_id_by_name(name=name)
        
        payload = {
            "name": new_name
        }

        return make_api_request(
            base_url=self.client.base_url,
            endpoint=self.endpoint + "/" + key_id,
            method="put",
            data=payload,
            token=self.client.api_key
        )

    
    def modify(self, name: str, model_hub: str=None, api_key:str =None, rate_limit_per_interval=None, rate_limit_interval=None):
        """Modify model hub, key, or rate limits of a stored API key. Cannot be used to rename key.
        
        :param name: The name of the key you want to modify.
        :type name: str
        :param model_hub: Name of the model hub. Current supported values are 'openai', 'together', 'octo'.
        :type model_hub: str, optional
        :param api_key: The API key.
        :type api_key: str, optional
        :param rate_limit_per_interval: The maximum amount of times Vijil will query the model hub in the specified rate_limit_interval, defaults to 60
        :type rate_limit_per_interval: int, optional
        :param rate_limit_interval: The size of the interval (in seconds) defining maximum queries to model hub in said interval. For example, if rate_limit_per_interval is 60 and rate_limit_interval is 10, then Vijil will query the model hub at most 60 times in 10 seconds. Defaults to 10
        :type rate_limit_interval: int, optional
        """

        #check that model hub is supported and key name refers to existing name
        if model_hub is not None:
           self.check_model_hub(model_hub=model_hub)        
        
        key_id = self.get_id_by_name(name=name)

        payload = {
            "name": name,
            "hub": model_hub,
            "rate_limit_per_interval": rate_limit_per_interval,
            "rate_limit_interval": rate_limit_interval,
            "value": api_key,
        }

        #remove None values
        payload = {k: v for k, v in payload.items() if v is not None}

        return make_api_request(
            base_url=self.client.base_url,
            endpoint=self.endpoint + "/" + key_id,
            method="put",
            data=payload,
            token=self.client.api_key
        )

    def delete(self, name: str):
        """Delete API key with specified name
        
        :param name: The name of the key you want to delete
        :type name: str
        :return: Response to the API request.
        :rtype: dict
        """

        key_id = self.get_id_by_name(name=name)

        return make_api_request(
            base_url=self.client.base_url,
            endpoint=self.endpoint + "/" + key_id,
            method="delete",
            token=self.client.api_key
        )


class Harnesses:
    """Class for handling harnesses API requests.
    
    :param client: The VijilClient instance.
    :type client: VijilClient
    """
    
    def __init__(self, client: VijilClient) -> None:
        """Initialize the Harnesses class.

        :param VijilClient client: The VijilClient instance.
        :type client: VijilClient
        """
        self.endpoint = "harness-configs"
        self.client = client
        pass

    def list(self):
        """List all harnesses.

        :return: List of dicts where each dict contains the metadata for a harness.
        :rtype: List(dict)
        """
        response = make_api_request(base_url=self.client.base_url, endpoint=self.endpoint, token=self.client.api_key)
        return response["results"]
    
    def create(self, harness_name: str, component_list: List[str], component_type: str = "probe"):
        """Not implemented yet.
        """
        raise NotImplementedError("Create harnesses is not implemented yet.")

        if component_type not in ["probe", "scenario"]:
            raise ValueError("component_type must be either 'probe' or 'scenario'")
        payload = {
            "id": str(uuid.uuid4()),
            "harness_name": harness_name,
            "component_list": component_list,
            "component_type": component_type
        }
        
        #if request is succeessful, return the harness id, name, and a "submitted" message
        return make_api_request(
            base_url=self.client.base_url,
            endpoint=self.endpoint,
            method="post",
            data=payload,
            token=self.client.api_key
        )
    def delete(self, harness_id: str):
        """
        Not implemented yet.
        """
        raise NotImplementedError("Delete harnesses is not implemented yet.")
        
        #if request is succeessful, return the harness id, name, and a "submitted" message
        return make_api_request(
            base_url=self.client.base_url,
            endpoint=f"harness-configs/{harness_id}",
            method="delete",
            token=self.client.api_key
        )


    
class Evaluations:
    """Class for handling evaluations API requests.
    
    :param client: The VijilClient instance.
    :type client: VijilClient
    """
    
    def __init__(
        self,
        client: VijilClient
    ) -> None:
        self.endpoint = "evaluations"
        self.client = client
        self.api_proxy_dict = None
    
    def list(self, limit=10):
        """List all valuations. Will return only 10 evaluations unless specified.
        
        :param limit: The number of evaluations to return, defaults to 10.
        :type limit: int, optional
        """

        response = make_api_request(base_url=self.client.base_url, endpoint=self.endpoint+"?limit="+str(limit), token=self.client.api_key)
        return response['results']
    
    def create(self, api_key_name: str=None, model_hub: str="openai", model_url: str=None, model_name: str="gpt-3.5-turbo", model_params={}, harness_params={}, harnesses=[]):
        """Create a new evaluation.

        :param api_key_name: The name of the model hub API key you want to use. If not specified, will use the first key we find for the specified model_hub.
        :type api_key_name: str, optional
        :param model_hub: The model hub you want to use. Supported options are "openai", "together", "octo", "custom".  Defaults to "openai"
        :type model_hub: str, optional
        :param model_url: The URL of the model you want to use. Only required for custom model hub. Defaults to None
        :type model_url: str, optional
        :param model_name: The name of the model you want to use. Check the model hub's API documentation to find valid names. Defaults to "gpt-3.5-turbo"
        :type model_name: str, optional
        :param model_params: A dictionary specifying inference parameters like temperature and top_p. If none are specified, model hub defaults will be used. Defaults to {}
        :type model_params: dict, optional
        :param harness_params: Set optional parameters like is_lite, defaults to {}
        :type harness_params: dict, optional
        :param harnesses: A list of harnesses you want to include in the evaluation, defaults to []
        :type harnesses: List[str], optional
        :raises TypeError: If you have no API keys stored.
        :raises ValueError: If you have no API keys stored for the specified model hub.
        :raises ValueError: If you supply an api_key_name that does not exist.
        :raises ValueError: If you specify lite mode for any harness other than ethics.
        :return: API response containing evaluation ID of the newly created evaluation.
        :rtype: dict
        """


        # store all api keys in a dictionary if not there
        if self.api_proxy_dict is None:
            try:
                self.api_proxy_dict = get_api_proxy_dict(base_url=self.client.base_url, token=self.client.api_key)
            except TypeError:
                raise TypeError("No API keys found. Please upload an API key first.")
            
        # get api key proxy for the model hub
        try:
            hub_api_proxy_dict = self.api_proxy_dict[model_hub]
        except KeyError:
            raise ValueError(f"No API key stored for model hub {model_hub}")
        
        # get api key proxy for the model hub
        if api_key_name is not None:
            #find api key id for the api key name
            if api_key_name not in hub_api_proxy_dict.keys():
                raise ValueError(f"No API key found for name {api_key_name}")
            else:
                api_key_proxy = hub_api_proxy_dict[api_key_name]
        else: #if no key specified, use first value in hub dictionary
            api_key_proxy = next(iter(hub_api_proxy_dict.values()))

        # create the payload
        payload = { 
                "id": str(uuid.uuid4()),
                "hub": model_hub,
                "model": model_name,
                "api_key_proxy": api_key_proxy,
                "scenario_config_filters": []
        }
        if model_hub == "custom":
            if model_url is None:
                raise ValueError("For custom model hubs, you must specify a model URL.")
            if api_key_name is None:
                raise ValueError("For custom model hubs, you must specify an API key name. Use `api_keys.list()` to see available keys.")
            payload["url"] = model_url
        if model_params:
            payload['agent_params'] = model_params
            if model_params.get("num_generations"):
                payload["num_generations"] = model_params["num_generations"]
        if harness_params.get('sample_size'):
            payload['sample_size'] = harness_params['sample_size']
        if harness_params.get('is_lite')==True:
            if harnesses == ['ethics']:
                harnesses = ['ethics_lite']
            else:
                raise ValueError("Lite mode is only available for the ethics harness.")
        if "trust_score" in harnesses:
            if len(harnesses)==1:
                harnesses_modified = ["security","privacy","hallucination","robustness","toxicity","stereotype","fairness","ethics","OpenLLM"]
            else:
                raise ValueError("The `trust_score` harness is available only as a standalone harness.")
        else:
            harnesses_modified = harnesses
        payload["harness_config_ids"] = [f"vijil.harnesses.{h}" for h in harnesses_modified]
        

        return make_api_request(
            base_url=self.client.base_url,
            endpoint=self.endpoint,
            method="post",
            data=payload,
            token=self.client.api_key
        )
        
    def get_status(self, evaluation_id: str):
        """Retrieve the status of an evaluation

        :param evaluation_id: The unique ID of the evaluation
        :type evaluation_id: str
        :return: A dict with the id, status, and other metadata of the evaluation
        :rtype: dict
        """

        response = make_api_request(base_url=self.client.base_url, endpoint=f"evaluations/{evaluation_id}", token=self.client.api_key)
        return response
    
    def summarize(self, evaluation_id: str):
        """
        Return summary dataframe of the evaluation results, aggregated at every level
        (overall eval, dimension, scenario, probe)

        :param evaluation_id: The unique ID of the evaluation
        :type evaluation_id: str
        :return: A dataframe with the level, level_name, and score of the evaluation
        :rtype: pandas.DataFrame
        """

        #initalize list of dicts where keys are level, level_name, score
        summary_rows = []
        
        # get status of evaluation
        try:
            status_dict = self.get_status(evaluation_id=evaluation_id)
        except ValueError as e: # for when evaluation doesn't exist
            return e
        
        # evaluation level
        if status_dict['status']=='COMPLETED':
            row = dict()
            row['level'] = 'overall'
            row['level_name'] = 'evaluation'
            row['score'] = round(status_dict['score']*100, 2)
            summary_rows.append(row)            
        else:
            return ValueError("Evaluation is not completed yet, check back later.")
        
        # harness level
        response = make_api_request(base_url=self.client.base_url, endpoint=f"harness?evaluation_id={evaluation_id}", token=self.client.api_key)
        for harness in response['results']:
            if harness['harness_type']=='DIMENSION' and harness['score'] is not None:
                row = dict()
                row['level'] = 'harness'
                row['level_name'] = harness['name']
                row['score'] = round(harness['score']*100, 2)
                summary_rows.append(row)   
                
        # scenario level
        response = make_api_request(base_url=self.client.base_url, endpoint=f"scenarios?evaluation_id={evaluation_id}", token=self.client.api_key)
        for scenario in response['results']:
            if scenario['score'] is not None:
                row = dict()
                row['level'] = 'scenario'
                row['level_name'] = scenario['name']
                row['score'] = round(scenario['score']*100, 2)
                summary_rows.append(row)
                
        # probe level
        response = make_api_request(base_url=self.client.base_url, endpoint=f"probes?evaluation_id={evaluation_id}", token=self.client.api_key)
        for probe in response['results']:           
            if probe['score'] is not None:
                row = dict()
                row['level'] = 'probe'
                row['level_name'] = probe['name']
                row['score'] = round(probe['score']*100, 2)
                summary_rows.append(row)
                
        return pd.DataFrame(summary_rows)
        
    def export_summary(self, evaluation_id: str, output_dir: str = './', format: str='pdf'):
        """
        Export a PDF or HTML report of the evaluation results containing evaluation metadata
        plus stats from summarize() function

        :param evaluation_id: The unique ID of the evaluation
        :type evaluation_id: str
        :param output_dir: The directory to save the report to. Defaults to current directory
        :type output_dir: str
        :param format: The format of the report. Defaults to pdf. Options are 'pdf' and 'html'
        :type format: str
        :raises ValueError: If specified format is not 'pdf' or 'html'
        """
        #get dataframe of summary stats
        summary = self.summarize(evaluation_id=evaluation_id)

        #get evaluation metadata
        status_dict = self.get_status(evaluation_id=evaluation_id)

        #set jinja settings
        HOME = os.path.join(os.path.dirname(__file__), ".")
        templateLoader = jinja2.FileSystemLoader(
            searchpath=HOME + "/templates"
        )
        templateEnv = jinja2.Environment(loader=templateLoader)
        header_template = templateEnv.get_template("vijil_header.jinja")
        footer_template = templateEnv.get_template("vijil_footer.jinja")
        pdf_template = templateEnv.get_template("whole_pdf.jinja")

        filename = evaluation_id + '_summary.' + format

        data_fields = {
            "reportfile": filename,
            "run_uuid": evaluation_id,
            "start_time": str(datetime.fromtimestamp(status_dict['created_at'], tz=timezone.utc)) + " UTC",
            "created_by": status_dict['created_by'],
            "end_time": str(datetime.fromtimestamp(status_dict['completed_at'], tz=timezone.utc)) + " UTC",
            "model_name": status_dict["model"],
            'total_test_count': status_dict['total_test_count'],
            'completed_test_count': status_dict['completed_test_count'],
            'error_test_count': status_dict['error_test_count'],
            "results": summary.to_html(index=False)
        }

        #write to file
        if format=='html': #use header and footer templates for html

            # render the header.
            digest_content = header_template.render(data_fields)            
            # render the footer
            digest_content += footer_template.render()

            with open(os.path.join(output_dir, filename), "w") as f:
                f.write(digest_content)

        elif format=='pdf': #use whole_pdf template which leaves out CSS and JS
            digest_content = pdf_template.render(data_fields)            
            pdf = FPDF()
            pdf.add_page()
            pdf.write_html(digest_content)
            pdf.output(os.path.join(output_dir, filename))
        else:
            raise ValueError("format must be 'html' or 'pdf'") 
    
    def describe(self, evaluation_id: str, limit: int = 1000, format: str = "dataframe", prettify: bool = True):
        """
        Return either list or dataframe of prompt-level metadata and evaluation results,
        with metadata and evaluation scores for each prompt/response in the given evaluation id.

        :param evaluation_id: The unique ID of the evaluation
        :type evaluation_id: str
        :param limit: The maximum number of prompts to include in description. Defaults to 1000.
        :type limit: int, optional
        :param format: The format of the output. Defaults to "dataframe". Options are "dataframe" and "list"
        :type format: str, optional
        :param prettify: If True, will remove the "vijil.probes." prefix from the probe names to make it more readable. Defaults to True.
        :type prettify: bool, optional
        :raises ValueError: If specified format is not 'dataframe' or 'list'
        """
        if limit is None:
            limit = 1000000
        
        response = make_api_request(base_url=self.client.base_url, endpoint=f"responses?evaluation_id={evaluation_id}&limit={limit}", token=self.client.api_key)

        # change detector ids to list if it is a string
        results = response['results']
        if len(results) == 0:
            raise ValueError(f"No results found for evaluation id {evaluation_id}. Please check that you have the correct id.")
        for idx, res in enumerate(results):
            if isinstance(res['detector_ids'], str):
                results[idx]['detector_ids'] = [res['detector_ids']]

        prompt_list = [
            {
                "probe": res['probe_config_id'].replace("vijil.probes.", "") if prettify else res['probe_config_id'],
                "input_prompt_id": res['input_prompt_id'],
                "prompt": res['input_prompt'],
                "response": res['response'],
                "detectors": [
                    det.replace("garak.detectors.", "").replace("autoredteam.detectors.", "")
                    for det in res['detector_ids']
                ],
                "score": res['detector_scores'],
                'generation': res['generation'],
                'status': res['status'],
                'error_message': res['error_message']
            }
            for res in results
        ]

        #calculate summary stats for detectors
        prompt_list_df = pd.DataFrame(prompt_list)
        prompt_list_df['avg_detector_score'] = prompt_list_df['score'].apply(lambda x: sum([sum(list(item.values())) for item in x]) / len(x) if len(x) and not any(['ERROR' in item for item in x]) else np.nan)
        prompt_list_df['min_detector_score'] = prompt_list_df['score'].apply(lambda x: min([min(list(item.values())) for item in x]) / len(x) if len(x) and not any(['ERROR' in item for item in x]) else np.nan)
        prompt_list_df['max_detector_score'] = prompt_list_df['score'].apply(lambda x: max([max(list(item.values())) for item in x]) / len(x) if len(x) and not any(['ERROR' in item for item in x]) else np.nan)
        prompt_list_df.sort_values('probe', inplace=True)        

        if format=='list':
            return prompt_list_df.to_dict(orient='records')
        elif format=='dataframe':
            return prompt_list_df
        else:
            raise ValueError("format must be 'list' or 'dataframe'")

    
    def export_report(self, evaluation_id: str, limit: int=1000000, format: str='csv', output_dir: str = './'):
        """
        Exports output of describe() into csv, jsonl, json, or parquet 

        :param evaluation_id: The unique ID of the evaluation
        :type evaluation_id: str
        :param limit: The maximum number of prompts to include in the report. Defaults to 1000000.
        :type limit: int, optional
        :param format: The format of the output. Defaults to "csv". Options are "csv", "parquet", "json" and "jsonl"
        :type format: str, optional
        :param output_dir: The directory to save the report. Defaults to the current directory.
        :type output_dir: str, optional
        :raises ValueError: If specified format is not 'csv', 'parquet', 'json' or 'jsonl'
        """

        if format=='csv':
            prompt_list_df = self.describe(evaluation_id=evaluation_id, limit=limit, format="dataframe")
            filename = evaluation_id + '_report.csv'
            filepath = os.path.join(output_dir, filename)            
            prompt_list_df.to_csv(filepath, index=False)
            print("report exported to " + filepath)
        elif format=='json':
            prompt_list = self.describe(evaluation_id=evaluation_id, limit=limit, format="list")
            filename = evaluation_id + '_report.json'
            filepath = os.path.join(output_dir, filename)
            with open(filepath, 'w') as f:
                json.dump(prompt_list, f, indent=4)
            print("report exported to " + filepath)
        elif format=='jsonl':
            prompt_list = self.describe(evaluation_id=evaluation_id, limit=limit, format="list")
            filename = evaluation_id + '_report.jsonl'
            filepath = os.path.join(output_dir, filename)
            with open(filepath, 'w') as f:
                for item in prompt_list:
                    f.write(json.dumps(item) + '\n')
            print("report exported to " + filepath)
        elif format=='parquet':
            prompt_list_df = self.describe(evaluation_id=evaluation_id, limit=limit, format="dataframe")
            filename = evaluation_id + '_report.parquet'
            filepath = os.path.join(output_dir, filename)
            prompt_list_df.to_parquet(filepath, index=False)
            print("report exported to " + filepath)
        else:
            raise ValueError("format must be 'csv', 'parquet', 'json', or 'jsonl'")

    def cancel(self, evaluation_id: str):
        """
        Cancels an in-progress evaluation

        :param evaluation_id: The unique ID of the evaluation
        :type evaluation_id: str
        :raises ValueError: If the evaluation is not in progress
        :returns: The response from the API
        :rtype: dict
        """

        #check eval status
        try:
            status_dict = self.get_status(evaluation_id=evaluation_id)
        except ValueError as e:
            return e
        
        if status_dict['status'] != 'IN_PROGRESS':
            raise ValueError(f"Evaluation {evaluation_id} is not in progress. Cannot cancel.")
        
        payload = {
                    "type": "CANCEL_EVALUATION",
                    "data": {
                        "evaluation_id": evaluation_id
                    }
                  }
        
        return make_api_request(
            base_url=self.client.base_url,
            endpoint="events",
            method="post",
            data=payload,
            token=self.client.api_key
        )
    
    def delete(self, evaluation_id: str):
        """
        Deletes an evaluation

        :param evaluation_id: The unique ID of the evaluation
        :type evaluation_id: str
        :raises ValueError: If the evaluation does not exist
        :returns: The response from the API
        :rtype: dict
        """

        #check eval status. This will raise an error if the eval doesn't exist.
        try:
            status_dict = self.get_status(evaluation_id=evaluation_id)
        except ValueError as e:
            return e
        
        payload = {
                    "type": "DELETE_EVALUATION",
                    "data": {
                        "evaluation_id": evaluation_id
                    }
                  }
        
        return make_api_request(
            base_url=self.client.base_url,
            endpoint="events",
            method="post",
            data=payload,
            token=self.client.api_key
        )

class Vijil:
    """Base class for the Vijil API client.
    
    :param base_url: The base URL for the Vijil API
    :type base_url: str
    :param api_key: The API key for the Vijil API
    :type api_key: str
    """
    client: VijilClient
    evaluations: Evaluations
    harnesses: Harnesses
    api_keys: APIKeys
    
    def __init__(self, base_url: str = BASE_URL, api_key: str = None):
        """Constructor class for VijilClient

        :param base_url: Base URL for API, defaults to BASE_URL as specified in `api.py`
        :type base_url: str, optional
        :param api_key: Vijil API key, defaults to None
        :type api_key: str, optional
        :raises ValueError: if no Vijil API key is provided in api_key and VIJIL_API_KEY is not set as an environment variable
        """
                
        if api_key is None:
            api_key = os.environ["VIJIL_API_KEY"]
        if api_key is None:
            raise ValueError(
                "No API key found! Please set VIJIL_API_KEY as environment variable or supply the `api_key` parameter."
            )
            
        self.client = VijilClient(base_url=base_url, api_key=api_key)
        self.evaluations = Evaluations(self.client)
        self.harnesses = Harnesses(self.client)
        self.api_keys = APIKeys(self.client)
