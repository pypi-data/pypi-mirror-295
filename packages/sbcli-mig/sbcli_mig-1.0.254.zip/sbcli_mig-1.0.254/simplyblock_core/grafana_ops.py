# coding=utf-8
import requests
import logging
from jinja2 import Environment, FileSystemLoader
from requests.auth import HTTPBasicAuth
import json






logger = logging.getLogger()


GRAFANA_API_KEY = 'YOUR_GRAFANA_API_KEY'
GRAFANA_BASE_URL = 'http://your-grafana-instance/api'

headers = {
    'Authorization': f'Bearer {GRAFANA_API_KEY}',
    'Content-Type': 'application/json'
}


    

def create_grafana_organization(org_name, org_cluster,api_endpoint,cluster_secret):
    if not api_endpoint.startswith("https://"):
        if api_endpoint.startswith("http://"):
            api_endpoint = api_endpoint.replace("http://", "https://", 1)
        else:
            api_endpoint = "https://" + api_endpoint
            
    api_endpoint = api_endpoint.rstrip('/') + "/grafana"

    session = requests.Session()
    session.auth = HTTPBasicAuth("admin", cluster_secret)
    session.headers.update({
        'Content-Type': 'application/json'
    })
    data = {
        'name': org_name
    }
    response = session.post(
        f'{api_endpoint}/api/orgs',
        data=json.dumps(data)
    )

    if response.status_code == 200:
        logger.info("Organization created successfully.")
        response_data = response.json()
        
        logger.info(response_data.get('orgId'))
    else:
        print(f'Failed to create organization. Status code: {response.status_code}')    

    logger.info("creating a folder for organization")
    data = {
        'title': org_name
    }
    response = session.post(
        f'{api_endpoint}/api/folders',
        data=json.dumps(data)
    )
    
    if response.status_code == 200:
        logger.info("folder created for organization successfully.")
    else:
        print(f'Failed to create folder, Status code: {response.status_code}')
        
    return (response.json()).get('url')





# def update_grafana_organization(org_id, data):
#     response = requests.put(f'{GRAFANA_BASE_URL}/orgs/{org_id}', headers=headers, json=data)
#     return response

# def delete_grafana_organization(org_id):
#     response = requests.delete(f'{GRAFANA_BASE_URL}/orgs/{org_id}', headers=headers)
#     return response