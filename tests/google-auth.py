from google.auth import compute_engine
from google.cloud.container_v1 import ClusterManagerClient
from kubernetes import client

from google.oauth2 import service_account
import os
def google_authenticate(project_id, zone, cluster_id):
    SCOPES = ['https://www.googleapis.com/auth/cloud-platform']
    f = open('/Users/dylanblake/key.json', "r")
    key = f.read()
    try:
        fw = open('key.json', 'r')
        fw.close()
    except:
        fw = open('key.json', 'w')
        fw.write(key)
        fw.close()
    credentials = service_account.Credentials.from_service_account_file("key.json", scopes=SCOPES)
    cluster_manager_client = ClusterManagerClient(credentials=credentials)
    cluster = cluster_manager_client.get_cluster(project_id, zone, cluster_id)
    configuration = client.Configuration()
    configuration.host = "https://"+cluster.endpoint+":443"
    configuration.verify_ssl = False
    configuration.api_key = {"authorization": "Bearer " + credentials.token}
    return configuration

def test_gke():
    configuration = google_authenticate('conductive-fold-275020', 'us-central1-c', 'launch-cluster')
    client.Configuration.set_default(configuration)
    v1 = client.CoreV1Api()
    print("Listing pods with their IPs:")
    pods = v1.list_pod_for_all_namespaces(watch=False)
    for i in pods.items:
        print("%s\t%s\t%s" % (i.status.pod_ip, i.metadata.namespace, i.metadata.name))

if __name__ == '__main__':
    test_gke()
    # test_gke()