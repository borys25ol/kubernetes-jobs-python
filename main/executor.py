"""
Module with Kubernetes Jobs manager.
"""
from typing import Union

from kubernetes import client, config

from main.log import get_logger

logger = get_logger(name="executor")

config.load_kube_config()


def get_job_name(job: Union[str, client.V1Job]) -> str:
    """Return the name of a job"""
    return job if isinstance(job, str) else job.metadata.name


def is_failed(job: client.V1Job) -> bool:
    """Return True if the job is failed."""
    return bool(job.status.failed)


def is_succeeded(job: client.V1Job) -> bool:
    """Return True if the job has succeeded."""
    return bool(job.status.succeeded)


def is_completed(job: client.V1Job) -> bool:
    """Return True if the job has completed (either failed or succeeded)."""
    return is_failed(job) or is_succeeded(job)


def is_active(job: client.V1Job) -> bool:
    """Return True if the job is active (running)."""
    return bool(job.status.active)


def get_status(job: client.V1Job) -> str:
    """Return current job status."""
    if is_failed(job):
        return "FAILED"
    elif is_succeeded(job):
        return "SUCCEEDED"
    elif is_active(job):
        return "ACTIVE"
    return "PENDING"


class KubernetesJobManager:
    """
    Kubernetes client to execute jobs.
    """

    def __init__(
        self,
        image: str,
        container_name: str,
        command: list[str],
        args: str,
        pod_name: str,
        job_name: str,
        namespace: str = "default",
        image_pull_policy: str = "Never",
    ):
        self.image = image
        self.container = container_name
        self.image_pull_policy = image_pull_policy
        self.command = command
        self.args = args
        self.namespace = namespace
        self.pod_name = pod_name
        self.job_name = job_name
        self.api = client.ApiClient()
        self.batch_api = client.BatchV1Api()

    def execute_job(self) -> client.V1Job:
        container = self._create_container(
            image=self.image,
            name=self.container,
            pull_policy=self.image_pull_policy,
            args=self.args,
            command=self.command,
        )
        # Create a pod template spec.
        pod_template = self._create_pod_template(
            pod_name=self.pod_name, container=container
        )
        # Create a job.
        job = self._create_job(job_name=self.job_name, pod_template=pod_template)

        # Execute job.
        self.batch_api.create_namespaced_job(namespace=self.namespace, body=job)

        return job

    def get_job_status(self, job: Union[str, client.V1Job]) -> str:
        job = self.batch_api.read_namespaced_job_status(
            name=get_job_name(job=job), namespace=self.namespace
        )
        return get_status(job=job)

    @staticmethod
    def _create_container(
        image: str, name: str, pull_policy: str, args: str, command: list[str]
    ) -> client.V1Container:
        container = client.V1Container(
            image=image,
            name=name,
            image_pull_policy=pull_policy,
            args=[args],
            command=command,
        )
        logger.info(
            f"Created container with name: {container.name}, "
            f"image: {container.image} and args: {container.args}"
        )
        return container

    @staticmethod
    def _create_pod_template(
        pod_name: str, container: client.V1Container
    ) -> client.V1PodTemplateSpec:
        pod_template = client.V1PodTemplateSpec(
            spec=client.V1PodSpec(
                restart_policy="Never",
                containers=[container],
                automount_service_account_token=False,
            ),
            metadata=client.V1ObjectMeta(name=pod_name, labels={"pod_name": pod_name}),
        )
        return pod_template

    @staticmethod
    def _create_job(
        job_name: str, pod_template: client.V1PodTemplateSpec
    ) -> client.V1Job:
        metadata = client.V1ObjectMeta(name=job_name, labels={"job_name": job_name})
        job = client.V1Job(
            api_version="batch/v1",
            kind="Job",
            metadata=metadata,
            spec=client.V1JobSpec(backoff_limit=0, template=pod_template),
        )
        return job
