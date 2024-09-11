import json
import logging
import sys
import time
from dataclasses import dataclass
from typing import Optional, Sequence, Dict

import requests
from dotenv import load_dotenv
from rdflib import Graph
from requests import Response

log = logging.getLogger('fairspace_api')
load_dotenv()


# Custom request retry logic
# A backoff factor to apply between attempts after the second try
# Request will be retried num_retries only in case of erroneous response with code > 500 or connection error
def request_retry(method: str, url: str, num_retries: int = 4, backoff_factor: int = 120, **kwargs):
    retry_count = 0
    for _ in range(num_retries):
        try:
            time.sleep(backoff_factor * retry_count)
            response = requests.request(method, url, **kwargs)
            if response.status_code < 500:
                return response
        except requests.exceptions.ConnectionError:
            pass
    return None


def report_duration(task, start):
    duration = time.time() - start
    if duration >= 1:
        log.info(f'{task} took {duration:.0f}s.')
    else:
        log.info(f'{task} took {1000 * duration:.0f}ms.')


@dataclass
class Count:
    totalElements: int
    timeout: bool


@dataclass
class Page:
    totalPages: int
    totalElements: int
    rows: Sequence[any]
    hasNext: bool
    timeout: bool
    page: Optional[int] = None
    size: Optional[int] = None


class FairspaceApi:
    def __init__(self, url, keycloak_url, realm, client_id, client_secret, username, password, verify_cert=True):
        self.url = url
        self.keycloak_url = keycloak_url
        self.realm = realm
        self.client_id = client_id
        self.client_secret = client_secret
        self.username = username
        self.password = password
        self.verify_cert = verify_cert
        self.current_token: Optional[str] = None
        self.token_expiry = None
        self.do_views_update = 'false'

    def fetch_token(self) -> str:
        log.info('Fetching token')
        """

        :return:
        """
        # Fetch access token
        params = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'username': self.username,
            'password': self.password,
            'grant_type': 'password'
        }
        headers = {
            'Content-type': 'application/x-www-form-urlencoded',
            'Accept': 'application/json'
        }

        keycloak_url = f"{self.keycloak_url}/{self.realm}/protocol/openid-connect/token"
        response = request_retry("POST",
                                 keycloak_url,
                                 data=params,
                                 headers=headers,
                                 verify=self.verify_cert)
        if response is None or not response.ok:
            log.error('Error fetching token!')
            if response:
                log.error(f'{response.status_code} {response.reason}')
            # return ""
            sys.exit(1)
        data = response.json()
        token = data['access_token']
        self.current_token = token
        self.token_expiry = time.time() + data['expires_in']
        return token

    def get_token(self) -> str:
        token_expiration_buffer = 5
        if self.token_expiry is None or self.token_expiry <= time.time() + token_expiration_buffer:
            return self.fetch_token()
        return self.current_token

    def get_current_user(self):
        headers = {'Authorization': 'Bearer ' + self.get_token()}
        response = requests.get(f'{self.url}/api/users/current', headers=headers, verify=self.verify_cert)
        if not response.ok:
            log.error('Error fetching current user')
            log.error(f'{response.status_code} {response.reason}')
            sys.exit(1)
        return response.json()

    def update_user(self, user_id, roles=dict()):
        data = {'id': user_id, **roles}
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': 'Bearer ' + self.get_token()
        }
        log.info(data)
        response = requests.patch(f'{self.url}/api/users/', data=json.dumps(data), headers=headers, verify=self.verify_cert)
        if not response.ok:
            log.error('Error updating user roles')
            log.error(f'{response.status_code} {response.reason}')
            sys.exit(1)
        log.info(f'Roles updated, {response}')
        return response

    def get_all_users(self):
        headers = {'Authorization': 'Bearer ' + self.get_token()}
        response = requests.get(f'{self.url}/api/users/', headers=headers, verify=self.verify_cert)
        if not response.ok:
            log.error('Error fetching users')
            log.error(f'{response.status_code} {response.reason}')
            sys.exit(1)

        return response.json()

    # add user to workspace
    # role: Member, Manager or None (remove from workspace)
    def update_user_workspace_role(self, workspace: str, user_id: str, role: str):
        data = {'workspace': workspace, 'user': user_id, 'role': role}
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': 'Bearer ' + self.get_token()
        }
        log.info(data)
        response = requests.patch(f'{self.url}/api/workspaces/users/', data=json.dumps(data), headers=headers, verify=self.verify_cert)
        if not response.ok:
            log.error('Error updating user roles')
            log.error(f'{response.status_code} {response.reason}')
            sys.exit(1)
        log.info(f'Roles updated, {response}')
        return response

    def find_or_create_workspace(self, code, title, description=""):
        # Fetch existing workspaces
        headers = {'Authorization': 'Bearer ' + self.get_token()}
        response = requests.get(f'{self.url}/api/workspaces/', headers=headers, verify=self.verify_cert)
        if not response.ok:
            log.error('Error fetching workspaces')
            log.error(f'{response.status_code} {response.reason}')
            sys.exit(1)
        workspaces = response.json()
        matches = [ws for ws in workspaces if ws['code'] == code]
        if len(matches) > 0:
            return matches[0]

        # Create new workspace
        log.info('Creating new workspace ...')
        headers['Content-type'] = 'application/json'
        response: Response = requests.put(f'{self.url}/api/workspaces/',
                                          data=json.dumps({'code': code, 'title': title, 'description': description}),
                                          headers=headers,
                                          verify=self.verify_cert)
        if not response.ok:
            log.error('Error creating workspace!')
            log.error(f'{response.status_code} {response.reason}')
            sys.exit(1)
        log.info('Workspace created.')
        return response.json()

    def exists(self, path):
        """ Check if a path exists
        """
        headers = {
            'Depth': '0',
            'Authorization': 'Bearer ' + self.get_token()
        }
        response = requests.request('PROPFIND', f'{self.url}/api/webdav/{path}/', headers=headers, verify=self.verify_cert)
        return response.ok

    def ensure_dir(self, path, workspace=None):
        if self.exists(path):
            return
        # Create directory
        headers = {'Authorization': 'Bearer ' + self.get_token()}
        if workspace is not None:
            headers['Owner'] = workspace['iri']
        response: Response = requests.request('MKCOL', f'{self.url}/api/webdav/{path}/', headers=headers, verify=self.verify_cert)
        if not response.ok:
            log.error(f"Error creating directory '{path}'!")
            log.error(f'{response.status_code} {response.reason}')
            sys.exit(1)

    def upload_files(self, path, files: Dict[str, any]):
        # Upload files
        start = time.time()
        headers = {
            'Authorization': 'Bearer ' + self.get_token()
        }
        response = request_retry("POST",
                                 f'{self.url}/api/webdav/{path}/',
                                 data={'action': 'upload_files'},
                                 files=files,
                                 headers=headers,
                                 verify=self.verify_cert)
        if not response.ok:
            log.error(f"Error uploading files into '{path}'!")
            log.error(f'{response.status_code} {response.reason}')
            sys.exit(1)
        report_duration('Uploading files', start)

    def upload_files_by_path(self, path, files):
        self.upload_files(path, {filename: open(file, 'rb') for (filename, file) in files.items()})

    def upload_empty_files(self, path, filenames):
        self.upload_files(path, {filename: '' for filename in filenames})

    def change_collection_status(self, collection, status):
        # Change status
        start = time.time()
        headers = {
            'Authorization': 'Bearer ' + self.get_token()
        }
        response = requests.post(f'{self.url}/api/webdav/{collection}/',
                                 data={'action': 'set_status', 'status': status},
                                 headers=headers,
                                 verify=self.verify_cert)
        if not response.ok:
            log.error(f"Error changing status of collection '{collection}'!")
            log.error(f'{response.status_code} {response.reason}')
            sys.exit(1)
        report_duration('Changing status', start)

    def change_collection_permission(self, collection, principal, access):
        # Change status
        start = time.time()
        headers = {
            'Authorization': 'Bearer ' + self.get_token()
        }
        response = requests.post(f'{self.url}/api/webdav/{collection}/',
                                 data={'action': 'set_permission', 'access': access, 'principal': principal},
                                 headers=headers,
                                 verify=self.verify_cert)
        if not response.ok:
            log.error(f"Error changing status of collection '{collection}'!")
            log.error(f'{response.status_code} {response.reason}')
            sys.exit(1)
        report_duration('Changing status', start)

    def get_data(self, path: str):
        txtfile = open(path, 'r')
        data = txtfile.read()
        txtfile.close()
        return data

    def query_sparql(self, query: str):
        start = time.time()
        headers = {
            'Content-Type': 'application/sparql-query',
            'Accept': 'application/json',
            'Authorization': 'Bearer ' + self.get_token()
        }
        response = request_retry("POST", f"{self.url}/api/rdf/query", data=query, headers=headers, verify=self.verify_cert)
        if not response.ok:
            log.error('Error querying metadata at ' + self.url)
            log.error(f'{response.status_code} {response.reason}')
            return {}
        report_duration('Querying', start)
        return response.json()

    def lookup(self, query: str, resource_type: str):
        headers = {
            'Accept': 'application/json',
            'Authorization': 'Bearer ' + self.get_token()
        }
        response = requests.post(
            f"{self.url}/api/search/lookup",
            data=json.dumps({'query': query, 'resourceType': resource_type}),
            headers=headers,
            verify=self.verify_cert
        )
        if not response.ok:
            log.error(f'Error during lookup search!')
            log.error(f'{response.status_code} {response.reason}')
            sys.exit(1)
        return response.json()

    def upload_metadata_by_path(self, path):
        data = self.get_data(path)
        update = path.endswith("duplicate.ttl")
        self.upload_metadata('turtle', data, update)

    def upload_metadata(self, fmt, data, update, retry_401: bool = False):
        if fmt == 'turtle':
            content_type = 'text/turtle'
        elif fmt == 'ld+json':
            content_type = 'application/ld+json'
        else:
            log.error(f'Unsupported format: {fmt}')
            sys.exit(1)
        headers = {
            'Content-type': content_type,
            'Authorization': 'Bearer ' + self.get_token()
        }

        if update:
            response = request_retry("PATCH", f"{self.url}/api/metadata/",
                                     data=data.encode('utf-8') if fmt == 'turtle' else json.dumps(data),
                                     params={'doViewsUpdate': self.do_views_update},
                                     headers=headers,
                                     verify=self.verify_cert)
        else:
            response = request_retry("PUT", f"{self.url}/api/metadata/",
                                     data=data.encode('utf-8') if fmt == 'turtle' else json.dumps(data),
                                     params={'doViewsUpdate': self.do_views_update},
                                     headers=headers,
                                     verify=self.verify_cert)

        if response is None or not response.ok:
            log.error('Error uploading metadata!')
            if response is not None:
                log.error(f'Error code: {response.status_code}, details: {response.content}')
                # Retry request (once) in case the application took more time to process and the token expired
                if response.status_code == 401 and not retry_401:
                    log.info('Retrying request after fetching new token...')
                    self.upload_metadata(fmt, data, update, True)
        else:
            log.info('Upload done, response: ' + str(response))
        return response

    def upload_metadata_graph(self, graph: Graph, update: bool):
        self.upload_metadata('turtle', graph.serialize(format='turtle'), update)

    def delete_triples(self, data):
        headers = {
            'Content-type': 'text/turtle',
            'Authorization': 'Bearer ' + self.get_token()
        }

        response = request_retry("DELETE", f"{self.url}/api/metadata/",
                                 data=data.encode('utf-8'),
                                 params={'doViewsUpdate': self.do_views_update},
                                 headers=headers,
                                 verify=self.verify_cert)

        if response is None or not response.ok:
            log.error('Error deleting metadata!')
            if response is not None:
                log.error(f'Error code: {response.status_code}, details: {response.content}')
        else:
            log.info('Triple deletion done, response: ' + str(response))
        return response

    def delete_by_iri(self, iri):
        headers = {
            'Authorization': 'Bearer ' + self.get_token()
        }

        response = request_retry("DELETE", f"{self.url}/api/metadata/",
                                 params={'subject': iri, 'doViewsUpdate': self.do_views_update},
                                 headers=headers,
                                 verify=self.verify_cert)

        if response is None or not response.ok:
            log.error('Error deleting metadata by IRI!')
            if response is not None:
                log.error(f'Error code: {response.status_code}, details: {response.content}')
        else:
            log.info('Entity deletion done, response: ' + str(response))
        return response

    def retrieve_view_config(self) -> Page:
        headers = {
            'Accept': 'application/json',
            'Authorization': 'Bearer ' + self.get_token()
        }
        response = requests.get(f"{self.url}/api/views/", headers=headers, verify=self.verify_cert)
        if not response.ok:
            log.error(f'Error retrieving view config!')
            log.error(f'{response.status_code} {response.reason}')
            sys.exit(1)
        return response.json()

    def retrieve_view_page(self,
                           view: str,
                           page=1,
                           size=20,
                           include_counts=False,
                           include_joined_views=False,
                           filters=None) -> Page:
        data = {
            'view': view,
            'page': page,
            'size': size,
            'includeCounts': include_counts,
            'includeJoinedViews': include_joined_views
        }
        if filters is not None:
            data['filters'] = filters
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': 'Bearer ' + self.get_token()
        }
        response = requests.post(f"{self.url}/api/views/", data=json.dumps(data), headers=headers, verify=self.verify_cert)
        if not response.ok:
            log.error(f'Error retrieving {view} view page!')
            log.error(f'{response.status_code} {response.reason}')
            sys.exit(1)
        return Page(**response.json())

    def count(self,
              view: str,
              filters=None) -> Count:
        data = {
            'view': view
        }
        if filters is not None:
            data['filters'] = filters
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': 'Bearer ' + self.get_token()
        }
        response = requests.post(f"{self.url}/api/views/count", data=json.dumps(data), headers=headers, verify=self.verify_cert)
        if not response.ok:
            log.error(f'Error retrieving count for {view} view!')
            log.error(f'{response.status_code} {response.reason}')
            sys.exit(1)
        return Count(**response.json())

    def reindex(self):
        headers = {
            'Accept': 'application/json',
            'Authorization': 'Bearer ' + self.get_token()
        }
        response = requests.post(f"{self.url}/api/maintenance/reindex", None, headers=headers, verify=self.verify_cert)
        if not response.ok:
            log.error(f'Error reindexing, possibly a reindex is already in progres.')
            log.error(f'{response.status_code} {response.reason}')
            sys.exit(1)

    def compact(self):
        headers = {
            'Accept': 'application/json',
            'Authorization': 'Bearer ' + self.get_token()
        }
        response = requests.post(f"{self.url}/api/maintenance/compact", None, headers=headers, verify=self.verify_cert)
        if not response.ok:
            log.error(f'Error compacting the database.')
            log.error(f'{response.status_code} {response.reason}')
            sys.exit(1)

    def maintenance_status(self):
        headers = {
            'Accept': 'application/json',
            'Authorization': 'Bearer ' + self.get_token()
        }
        response = requests.get(f"{self.url}/api/maintenance/status", headers=headers, verify=self.verify_cert)
        if not response.ok:
            log.error(f'Error checking maintenance status.')
            log.error(f'{response.status_code} {response.reason}')
            return "Error checking maintenance status."
        else:
            return response.text
