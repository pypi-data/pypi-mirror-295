# Marvin

[![Quality Gate Status](https://sonar.us-east.devhub-cloud.cisco.com/api/project_badges/measure?project=panoptica-marvin&metric=alert_status&token=sqb_aa88cc46acaf5b3d2d9f8c09843024776e7a66df)](https://sonar.us-east.devhub-cloud.cisco.com/dashboard?id=panoptica-marvin)
[![Coverage](https://sonar.us-east.devhub-cloud.cisco.com/api/project_badges/measure?project=panoptica-marvin&metric=coverage&token=sqb_aa88cc46acaf5b3d2d9f8c09843024776e7a66df)](https://sonar.us-east.devhub-cloud.cisco.com/dashboard?id=panoptica-marvin)
[![Code Smells](https://sonar.us-east.devhub-cloud.cisco.com/api/project_badges/measure?project=panoptica-marvin&metric=code_smells&token=sqb_aa88cc46acaf5b3d2d9f8c09843024776e7a66df)](https://sonar.us-east.devhub-cloud.cisco.com/dashboard?id=panoptica-marvin)
[![Vulnerabilities](https://sonar.us-east.devhub-cloud.cisco.com/api/project_badges/measure?project=panoptica-marvin&metric=vulnerabilities&token=sqb_aa88cc46acaf5b3d2d9f8c09843024776e7a66df)](https://sonar.us-east.devhub-cloud.cisco.com/dashboard?id=panoptica-marvin)

Marvin is intended to provide protection for LLM-driven components of software systems.

We do so by inspecting prompts, and LLM responses to these prompts, with NLP techniques to determine if 
they are suspected to malicious activity. 

# Components
* [Marvin SDK](./sdk) - Python SDK to programmatically integrate system with LLM protection.
* [Prompt Inspection Server](./prompt_inspection_server) - HTTP server to serve the requests made by Marvin SDK.
* [Demo Chat App](./test_app) - Simple streamlit-based chat app to demo Marvin capabilities.
* [Auth](./auth) - Handle authentication across Marvin SaaS.
* **Forensic** - HTTP server to serve the requests made by the UI.
* [PII Service](./pii_service) - Remove PII data from messages in the queue.
* [Attack Analytics](./attack-analytics) - An offline process that analyzes the prompts and inserts them to the database.  
The attack analytics components are:
  * **Batch Processing** - A cronjob that reads the records from Amazon Athena and insert them into Amazon Aurora. 
  * **Producer** - Responsible for taking messages from the queue and push them into AWS MSK (kafka).

# Dev Pages
Developers can find more useful information here:
- [Marvin Playbook](https://cisco-eti.atlassian.net/l/cp/mKfZJGi1)
- [Marvin Onboarding New Engineer](https://cisco-eti.atlassian.net/l/cp/vs004iqd)

# Architecture

![](img/marvin-architecture.png)
# API Code Generation
All the servers specs can be found under the [openapi](openapi) folder.

### Python
In order to generate request/response models from OpenAPI spec,
you need to install [datamodel-code-generator](https://koxudaxi.github.io/datamodel-code-generator/): 

```shell
pip install datamodel-code-generator
```

> **Note**: Currently we only generate model files and not the client/server code utilizing them. (TODO - correct?)

### Go
In order to generate the API code for the go components, need to install  `oapi-codegen`:
```shell
go install github.com/oapi-codegen/oapi-codegen/v2/cmd/oapi-codegen@latest
```

### Generate
To generate API code for all the servers, run:
```shell
make generate
```

# Run Unit Tests
```shell
make test
```

# Run Helm Chart Test and Linting
```shell
make helm-test
```

# Running Database Migrations
We use golang [migrate](https://github.com/golang-migrate/migrate) to perform DB migrations.

Our database is divided into schemes, where each scheme has its own migration files.  
- **`forensic`**: The forensic scheme migration files can be found [here](attack-analytics/cmd/forensic/migration/config).
- **`attack-analytics`**: The attack-analytics migration files can be found [here](attack-analytics/cmd/batch-processing/migration/config).

The migration main entry running command is [here](goutils/cmd/common/migration/main.go).

### Environment Variables
The type of migration to run is determined by env vars:
- **`MIGRATION_DIR_PATH`**: The path to the migration config files.
- **`MIGRATION_VERSION`**: The version that you want to migrate to.


# Local Development

### Run local DB
You can run local postgres db using `docker-compose.yaml`  
First run the db:
```shell
docker-compose -f docker-compose.yaml up db --build -d
```
Then run the migration job for attack-analytics:
```shell
docker-compose -f docker-compose.yaml up bp-migration --build -d
```
And then run the migration job for forensic:
```shell
docker-compose -f docker-compose.yaml up forensic-migration --build -d
```

> **Note**: currently not all services can run locally,
> so you can't get a full system running locally using the docker compose.
> Alternatively, you can run the servers and the migration tasks locally
> by setting the correct configuration in [goutils/pkg/db/config.go](goutils/pkg/db/config.go). 

# System Tests
System tests are running as a GitHub action on:
1. push to main branch in [ci-main.yaml](.github/workflows/ci-main.yaml).
2. every 15 minutes as part of [smoke tests](.github/workflows/smoke-tests.yaml).

### Add Test
To add a new system test that will run as part of the CI:
1. add the test name to the [system tests reusable workflow](.github/workflows/run-system-tests.yaml) under `workflow_dispatch/inputs/test_flow_name/options`.
2. add the test name to the [run matrix](.github/workflows/ci-main.yaml) under `jobs/run-system-tests/strategy/matrix/include`.

# Integration with Motific
TODO

# Python requirements
**TODO - move to some developers guide file?**  

we use poetry CLI to handle our python packages.
prerequisites: `brew install poetry`
to run poetry cd to a folder containing `pyproject.toml` file. example of poetry handling:
1. poetry install --no-root - install current dependencies into your venv
2. poetry update - update and install the latest packages with given constraints from pyproject.toml
3. poetry lock - update and checks dependencies in lock file

# Metrics - Prometheus
For information on how to see or add metrics, check [Marvin Playbook](https://cisco-eti.atlassian.net/l/cp/mKfZJGi1).