# ReadMe extension

This is just a fork of [@hrbolek's](https://github.com/hrbolek) repository allowing development in devcontainers.

Step to launch devcontainer:

1. Install [*Dev Containers*](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers) extension for vscode ([documentation](https://code.visualstudio.com/docs/devcontainers/containers))
2. In command palette (<kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>P</kbd>) in the popup enter *"Dev Containers: Open Folder in Container"* and select *gql_empty* folder
3. Devcontaier building proces should start (it may take a while to compose all cotainers)

TODO:

- git repository is curently not recognized inside container
- life reloading is not working / restarting gunicorn server manually is necessary
- Appolo container sometimes stops without a reason

# Original ReadME

## What is going on

This is a project for students. Students are cooperating on this project under suspicion of teacher.
It is also a model of an information systems which could be used for some administrative task in university life.

## Used technologies

- Python
  - SQLAlchemy for modelling the database entitied (async queries)
  - FastAPI for API definition and run
  - Uvicorn as executor of FastAPI
  - Strawberry for GraphQL endpoint (federated GraphQL)
  - Appolo federation for GraphQL federation queries

- Javascript
  - ReactJS as a library for building bricks of user interface
  - fetch for fetching the data from endpoints

- Docker
  - containerization of applications
  - inner connection of containers

- Postgres
  - and its compatible replacements

## Base concept

The project has several docker containers

- `apollo` master of federation
- `gql_*` apollo federation member
- `nginx` is hardwired router
- `prostgres` is database server
- `pgadmin` is an interface for database server administration

## Who participated on this project

| Person | Role | Project Job | Period |
|:------:|:----:|:-----------:|:------:|
| AS     |Teacher|                          | 2022/9 - 2023/2 |
| AS     |Teacher| gql_ug                   | 2022/9 - 2023/2 |
| AS     |Teacher| gql_workflows            | 2022/9 - 2023/2 |

## Current Notes

To run this docker stack in some alpha mode you can run the docker-compose.yml. Be careful as it uses host volumes.
