Kubernetes Jobs Python Demo
===========================

[![Pre-commit: enabled](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white&style=flat)](https://github.com/pre-commit/pre-commit)

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)

Demo project to run Kubernetes jobs from Python script using Kubernetes python client. 

In this project was implemented this manifest Job file:

```yaml
---
apiVersion: batch/v1
kind: Job
metadata:
  name: shuffle-job-uuid-v4
  namespace: shuffler
  labels:
    job_name: shuffle-job-uuid-v4
spec:
  template:
    metadata:
      labels:
        app: shuffle-pod-uuid-v4
      name: shuffle-pod-uuid-v4
    spec:
      containers:
        - image: "borysol25/k8s-shuffler:latest"
          imagePullPolicy: Always
          name: "shuffler"
          command:
            - python3
            - shuffler.py
          args:
            - "test-shuffle"
      restartPolicy: Never
```

Requirements
-----------
Setup
- Docker Desktop installed and running
- Kubectl installed - https://kubernetes.io/docs/tasks/tools/install-kubectl
- For Mac users using Minikube is recommended

Developing
-----------

Install pre-commit hooks to ensure code quality checks and style checks

    $ make install_hooks

Then see `Configuration` section

You can also use these commands during dev process:

- To run mypy checks

      $ make types

- To run flake8 checks

      $ make style

- To run black checks:

      $ make format

- To run together:

      $ make lint

Local install
-------------

Setup and activate a python3 virtualenv via your preferred method. e.g. and install production requirements:

    $ make ve

For remove virtualenv:

    $ make clean


Local run
-------------
Build docker image:

    $ make docker_build

Run local shuffler script:

    $ python main/shuffler.py kubernetes

Or run it in docker:

    $ docker run --rm k8s-shuffler kubernetes

Run job in Kubernetes cluster from script:

```python
from time import sleep
from uuid import uuid4

from main.executor import KubernetesJobManager


def main() -> None:
    """
    Project entry point.
    """
    _id = uuid4()

    image = "borysol25/k8s-shuffler:latest"
    container = "shuffler"
    image_pull_policy = "Always"
    command = ["python3", "shuffler.py"]
    args = "test-shuffle"
    namespace = "shuffler"
    pod_name = f"shuffle-pod-{_id}"
    job_name = f"shuffle-job-{_id}"

    # Create Kubernetes job executor instance
    k8s_manager = KubernetesJobManager(
        image=image,
        container_name=container,
        image_pull_policy=image_pull_policy,
        command=command,
        args=args,
        namespace=namespace,
        pod_name=pod_name,
        job_name=job_name,
    )

    job = k8s_manager.execute_job()

    while True:
        status = k8s_manager.get_job_status(job=job)
        print(f"Got status `{status}` for job: {job_name}")
        sleep(2)


if __name__ == "__main__":
    main()

```


