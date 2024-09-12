import json
from typing import Optional
import time

import requests

from e2enetworks.cloud.tir.helpers import plan_name_to_sku_item_price_id, plan_name_to_sku_id
from e2enetworks.cloud.tir.skus import Plans, client
from e2enetworks.cloud.tir.utils import prepare_object
from e2enetworks.constants import (BASE_GPU_URL, INSTANCE_TYPE, NOTEBOOK,CUSTOM, SSH_ENABLE, SSH_DISABLE, SSH_UPDATE,
                                   PAID_USAGE, headers, AUTO_RENEW_STATUS, AUTO_TERMINATE_STATUS, CONVERT_TO_HOURLY_BILLING)


class Notebooks:
    def __init__(
            self,
            team: Optional[str] = "",
            project: Optional[str] = ""
    ):
        client_not_ready = (
            "Client is not ready. Please initiate client by:"
            "\n- Using e2enetworks.cloud.tir.init(...)"
        )
        if not client.Default.ready():
            raise ValueError(client_not_ready)

        if project:
            client.Default.set_project(project)

        if team:
            client.Default.set_team(team)

    def create(self, name, plan_name, image_type, image_version_id=None,
               dataset_id_list=[], disk_size_in_gb=30, is_jupyterlab_enabled=True, public_key=[],
               notebook_type="new", notebook_url="", registry_namespace_id=None, 
               e2e_registry_image_url=None, sku_item_price_id=None, commited_policy=None, 
               next_sku_item_price_id=None,):

        skus, skus_table = Plans().get_plans_list(NOTEBOOK, image_version_id)
        hourly_sku_item_price_id = plan_name_to_sku_item_price_id(skus, plan_name)
        sku_item_price_id = sku_item_price_id if sku_item_price_id else hourly_sku_item_price_id
        COMMITED_POLICY = [AUTO_RENEW_STATUS, AUTO_TERMINATE_STATUS, CONVERT_TO_HOURLY_BILLING]

        if sku_item_price_id != hourly_sku_item_price_id and not commited_policy:
            raise ValueError("commited_policy is required")
        if commited_policy and commited_policy not in COMMITED_POLICY:
            raise ValueError(f"commited_policy is should be in %s" % COMMITED_POLICY)
        
        if (commited_policy == AUTO_RENEW_STATUS or commited_policy == CONVERT_TO_HOURLY_BILLING) \
        and not next_sku_item_price_id :
            raise ValueError("next_sku_item_price_id is required")
        if commited_policy == AUTO_TERMINATE_STATUS :
            next_sku_item_price_id = None
        elif commited_policy == CONVERT_TO_HOURLY_BILLING :
            next_sku_item_price_id = hourly_sku_item_price_id
        

        if image_type!=CUSTOM and not image_version_id :
            raise ValueError("image_version_id is required")
        
        if image_type==CUSTOM and (not registry_namespace_id or not e2e_registry_image_url):
            raise ValueError("registry_namespace_id and e2e_registry_image_url are required")

        payload = json.dumps({
            "name": name,
            "dataset_id_list": dataset_id_list,
            "image_type": image_type,
            "is_jupyterlab_enabled": is_jupyterlab_enabled,
            "public_key": public_key,
            "sku_item_price_id": sku_item_price_id,
            "auto_shutdown_timeout": None,
            "instance_type": PAID_USAGE,
            "disk_size_in_gb": disk_size_in_gb,
            "notebook_type": notebook_type,
            "notebook_url": notebook_url,
        })
        new_payload = json.loads(payload)
        if image_type == CUSTOM :
            new_payload["registry_namespace_id"] = registry_namespace_id
            new_payload["e2e_registry_image_url"] = e2e_registry_image_url
        else :
            new_payload["image_version_id"] = image_version_id
        
        if commited_policy :
            new_payload["committed_instance_policy"] = commited_policy
            new_payload["next_sku_item_price_id"] = next_sku_item_price_id
        
        payload = json.dumps(new_payload)

        headers['Authorization'] = f'Bearer {client.Default.access_token()}'
        url = f"{BASE_GPU_URL}teams/{client.Default.team()}/projects/{client.Default.project()}/notebooks/?" \
              f"apikey={client.Default.api_key()}"
        response = requests.post(url=url, headers=headers, data=payload)
        return prepare_object(response)

    def get(self, notebook_id):

        if type(notebook_id) != int:
            raise ValueError(notebook_id)

        url = f"{BASE_GPU_URL}teams/{client.Default.team()}/projects/{client.Default.project()}/notebooks/" \
              f"{notebook_id}/"
        req = requests.Request('GET', url)
        response = client.Default.make_request(req)
        return prepare_object(response)

    def list(self):

        url = f"{BASE_GPU_URL}teams/{client.Default.team()}/projects/{client.Default.project()}/notebooks/"
        req = requests.Request('GET', url)
        response = client.Default.make_request(req)
        return prepare_object(response)

    def delete(self, notebook_id):
        if type(notebook_id) != int:
            raise ValueError(notebook_id)

        url = f"{BASE_GPU_URL}teams/{client.Default.team()}/projects/{client.Default.project()}/notebooks/" \
              f"{notebook_id}/"
        req = requests.Request('DELETE', url)
        response = client.Default.make_request(req)
        response = response.text
        response = json.loads(response)
        if response.get('code')==200:
            return response.get('message')
        raise ValueError("notebook not available with given id")
        return False

    def stop(self, notebook_id):
        if type(notebook_id) != int:
            raise ValueError(notebook_id)
        
        url = f"{BASE_GPU_URL}teams/{client.Default.team()}/projects/{client.Default.project()}/notebooks/" \
              f"{notebook_id}/actions/?action=stop&"
        req = requests.Request('PUT', url)
        response = client.Default.make_request(req)
        
        if response.status_code==200:
            print("Stopping notebook. it may take a few seconds ...")
            time.sleep(10)
            print("Stopped notebook")
        return prepare_object(response)

    def start(self, notebook_id):
        if type(notebook_id) != int:
            raise ValueError(notebook_id)

        url = f"{BASE_GPU_URL}teams/{client.Default.team()}/projects/{client.Default.project()}/notebooks/" \
              f"{notebook_id}/actions/?action=start&"
        req = requests.Request('PUT', url)
        response = client.Default.make_request(req)
        if response.status_code==200:
            print("Starting notebook. it may take a few seconds ...")
        return prepare_object(response)

    def configure_ssh(self, notebook_id: int, action: str, ssh_keys_to_add=[], ssh_keys_to_remove=[]):
        if not isinstance(notebook_id, int):
            raise ValueError("notebook_id is not a valid integer.")
        if isinstance(ssh_keys_to_add, str):
            ssh_keys_to_add = [ssh_keys_to_add]
        if isinstance(ssh_keys_to_remove, str):
            ssh_keys_to_remove = [ssh_keys_to_remove]

        if action not in [SSH_ENABLE, SSH_DISABLE, SSH_UPDATE]:
            raise ValueError("Invalid action... available actions: ['enable', 'disable', 'update']")
        if action == SSH_UPDATE and not ssh_keys_to_add and not ssh_keys_to_remove:
            raise ValueError("'update' action requires either 'ssh_keys_to_add' or 'ssh_keys_to_remove'")
        if action == SSH_ENABLE and not ssh_keys_to_add:
            raise ValueError("'enable' action requires 'ssh_keys_to_add'")

        if action == SSH_DISABLE:
            disable_url = f"{BASE_GPU_URL}teams/{client.Default.team()}/projects/{client.Default.project()}/notebooks/{notebook_id}/ssh-keys/"
            req = requests.Request('DELETE', disable_url)
        elif action == SSH_ENABLE:
            enable_url = f"{BASE_GPU_URL}teams/{client.Default.team()}/projects/{client.Default.project()}/notebooks/{notebook_id}/ssh-keys/"
            req = requests.Request('PUT', enable_url, json={"ssh_keys_to_add": ssh_keys_to_add})
        elif action == SSH_UPDATE:
            update_url = f"{BASE_GPU_URL}teams/{client.Default.team()}/projects/{client.Default.project()}/notebooks/{notebook_id}/ssh-keys/"
            req = requests.Request('PUT', update_url, json={"ssh_keys_to_add": ssh_keys_to_add, "ssh_keys_to_remove": ssh_keys_to_remove})
        else:
            raise ValueError("Invalid action...")
        response = client.Default.make_request(req)
        if response.status_code == 200:
            print("SSH configured successfully.")
        return prepare_object(response)

    def list_attached_ssh_keys(self, notebook_id: int):
        if type(notebook_id) is not int:
            raise ValueError("notebook_id is not a valid integer")
        url = f"{BASE_GPU_URL}teams/{client.Default.team()}/projects/{client.Default.project()}/notebooks/{notebook_id}/ssh-keys/"
        req = requests.Request('GET', url)
        return prepare_object(client.Default.make_request(req))

    def upgrade(self, notebook_id, plan_name, sku_item_price_id, commited_policy, next_sku_item_price_id=None):
        if type(notebook_id) != int:
            raise ValueError(notebook_id)
        
        if type(plan_name) != str:
            raise ValueError(plan_name)
        
        if type(sku_item_price_id) != int:
            raise ValueError(sku_item_price_id)
        
        if type(commited_policy) != str:
            raise ValueError(next_sku_item_price_id)
        
        skus, skus_table = Plans().get_plans_list(NOTEBOOK)
        hourly_sku_item_price_id = plan_name_to_sku_item_price_id(skus, plan_name)
        sku_id = plan_name_to_sku_id(skus, plan_name)
        sku_item_price_id = sku_item_price_id if sku_item_price_id else hourly_sku_item_price_id
        COMMITED_POLICY = [AUTO_RENEW_STATUS, AUTO_TERMINATE_STATUS, CONVERT_TO_HOURLY_BILLING]

        if sku_item_price_id != hourly_sku_item_price_id and not commited_policy:
            raise ValueError("commited_policy is required")
        if commited_policy not in COMMITED_POLICY:
            raise ValueError(f"commited_policy is should be in %s" % COMMITED_POLICY)
        
        if (commited_policy == AUTO_RENEW_STATUS or commited_policy == CONVERT_TO_HOURLY_BILLING) \
        and not next_sku_item_price_id :
            raise ValueError("next_sku_item_price_id is required")
        if commited_policy == AUTO_TERMINATE_STATUS :
            next_sku_item_price_id = None
        elif commited_policy == CONVERT_TO_HOURLY_BILLING :
            next_sku_item_price_id = hourly_sku_item_price_id
        
        payload = json.dumps(
                        {
                    "sku_id": sku_id,
                    "sku_item_price_id": sku_item_price_id,
                    "committed_instance_policy": commited_policy,
                    "next_sku_item_price_id": next_sku_item_price_id
                }
        )

        headers['Authorization'] = f'Bearer {client.Default.access_token()}'
        url = f"{BASE_GPU_URL}teams/{client.Default.team()}/projects/{client.Default.project()}/notebooks/" \
              f"{notebook_id}/?apikey={client.Default.api_key()}"
        response = requests.put(url=url, headers=headers, data=payload)
        return prepare_object(response)

    def upgrade_pvc(self, notebook_id, size):
        if type(notebook_id) != int:
            raise ValueError(notebook_id)

        if type(size) != int:
            raise ValueError(notebook_id)

        payload = json.dumps({
            "size": size})
        headers['Authorization'] = f'Bearer {client.Default.access_token()}'
        url = f"{BASE_GPU_URL}teams/{client.Default.team()}/projects/{client.Default.project()}/notebooks/" \
              f"{notebook_id}/pvc/upgrade/?apikey={client.Default.api_key()}"
        response = requests.put(url=url, headers=headers, data=payload)
        return prepare_object(response)
    
    def registry_namespace_list(self):
        url = f"{BASE_GPU_URL}teams/{client.Default.team()}/projects/{client.Default.project()}/container_registry/"
        req = requests.Request('GET', url)
        response = client.Default.make_request(req)
        return prepare_object(response)
    
    def registry_detail(self, registry_namespace_id):
        url = f"{BASE_GPU_URL}teams/{client.Default.team()}/projects/{client.Default.project()}/container_registry/{registry_namespace_id}/namespace-repository/"
        req = requests.Request('GET', url)
        response = client.Default.make_request(req)
        return prepare_object(response)
    
    def commited_policy(self):
        INSTANCE_UPDATION_LIST = [AUTO_RENEW_STATUS, AUTO_TERMINATE_STATUS, CONVERT_TO_HOURLY_BILLING]
        print(INSTANCE_UPDATION_LIST)
        

    @staticmethod
    def help():
        print("\t\tNotebook Class Help")
        print("\t\t=================")
        help_text = f"""
                Notebooks class provides methods to interact with notebooks in a project.

                Available methods:
                1. create(
                    name(required):String, 
                    plan(required):String=> Plans Can be listed using tir. Plans Apis",
                    image_id(required), 
                    instance_type={INSTANCE_TYPE}, 
                    disk_size_in_gb=30,
                    notebook_type="new",
                    notebook_url="",
                    is_jupyterlab_enabled: bool,
                    public_key: list (required if JupyterLab is disabled))
                2. get(notebook_id): Get information about a notebook.
                3. list(): List all notebooks in the project.
                4. delete(notebook_id): Delete a notebook.
                5. stop(notebook_id): Stop a running notebook.
                6. start(notebook_id): Start a stopped notebook.
                7. upgrade(notebook_id, size): Upgrade the size of a notebook's PVC.
                8. list_attached_ssh_keys(notebook_id): List all attached ssh keys.
                9. configure_ssh(notebook_id, action('enable', 'disable', 'update'), ssh_keys_to_add(optional), ssh_keys_to_remove(optional)): Enable, disable or update ssh keys by adding or removing keys.

                Usage:
                notebooks = Notebooks(team, project)
                notebooks.create("test-notebook", "CPU-C3-4-8GB-0", 9, 
                    instance_type="paid_usage", 
                    disk_size_in_gb=30,
                    notebook_type="new",
                    notebook_url="")
                notebooks.get(notebook_id)
                notebooks.list()
                notebooks.delete(notebook_id)
                notebooks.stop(notebook_id)
                notebooks.start(notebook_id)
                notebooks.upgrade_pvc(notebook_id, size)
                notebooks.list_attached_ssh_keys(notebook_id)
                notebooks.configure_ssh(notebook_id, action, ssh_keys_to_add(optional), ssh_keys_to_remove(optional))
                """
        print(help_text)
