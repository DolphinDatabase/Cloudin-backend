import subprocess
import pytest
from kubernetes import client, config
from time import sleep
import requests

CHART_DIR = "cloudin-midall"
CHART_NAME = "cloudin-midall-1.0.0.tgz"
RELEASE_NAME = "cloudin"
NAMESPACE = "k8s-test"
INITIAL_REPLICAS = 1
FINAL_REPLICAS = 3

@pytest.fixture(scope="session")
def setup_teardown():
    subprocess.run(["helm", "package", CHART_DIR])

    config.kube_config.load_kube_config(context="k3d-mycluster")

    api = client.CoreV1Api()
    api.create_namespace(body=client.V1Namespace(metadata=client.V1ObjectMeta(name=NAMESPACE)))

    yield

    subprocess.run(["helm", "uninstall", RELEASE_NAME, "-n", NAMESPACE])

    api.delete_namespace(name=NAMESPACE, body=client.V1DeleteOptions())

def test_autoscaling(setup_teardown):
    CHART = "{CHART_DIR}/{CHART_NAME}"
    subprocess.run(["helm", "install", RELEASE_NAME, "-n", NAMESPACE, CHART, "--wait"])

    sleep(10)

    api = client.AppsV1Api()
    deployment = api.read_namespaced_deployment(name=RELEASE_NAME, namespace=NAMESPACE)
    assert deployment.spec.replicas == INITIAL_REPLICAS

    for _ in range(10):
        response = requests.get("http://localhost/config/test")
        assert response.status_code == 200

    sleep(60)

    deployment = api.read_namespaced_deployment(name=RELEASE_NAME, namespace=NAMESPACE)
    assert deployment.spec.replicas >= FINAL_REPLICAS