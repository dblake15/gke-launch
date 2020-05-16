from os import path
import sys
from kubernetes import client, config
from google.auth import compute_engine
from google.cloud.container_v1 import ClusterManagerClient
from google.oauth2 import service_account
import os
def main():
    # config.load_kube_config()
    project_id = "conductive-fold-275020"
    zone = "us-central1-c"
    cluster_id = "launch-cluster"
    # config.load_kube_config()
    SCOPES = ['https://www.googleapis.com/auth/cloud-platform']
    path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
    credentials = service_account.Credentials.from_service_account_file(path, scopes=SCOPES)
    cluster_manager_client = ClusterManagerClient(credentials=credentials)
    cluster = cluster_manager_client.get_cluster(project_id, zone, cluster_id)
    configuration = client.Configuration()
    configuration.host = "https://"+cluster.endpoint+":443"
    configuration.verify_ssl = False
    configuration.api_key = {"authorization": "Bearer " + credentials.token}
    client.Configuration.set_default(configuration)

    v1 = client.AppsV1Api()
    # if sys.argv[1]:
    #     name = sys.argv[1]
    # else:
    name = 'cir-anders-openmp'
    resp = v1.delete_namespaced_deployment(name=name, namespace="default")
    print("Deployment {} deleted.".format(name))

if __name__ == '__main__':
    main()