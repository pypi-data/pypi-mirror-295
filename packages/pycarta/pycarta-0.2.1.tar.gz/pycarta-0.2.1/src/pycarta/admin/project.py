from .types import (
    Connection,
    Project,
)


def create_project(name: str, bucket: str) -> Project:
    from pycarta import get_agent
    agent = get_agent()
    response = agent.post('project',
                          json={
                              "name": name,
                              "bucketName": bucket
                          })
    return Project(**response.json())

def delete_project(project_id: str):
    from pycarta import get_agent
    agent = get_agent()
    agent.delete(f'project/{project_id}')
    return True

def create_connection(project_id: str, connection: Connection) -> Connection:
    from pycarta import get_agent
    agent = get_agent()
    response = agent.post(f'project/connection/{project_id}',
                          json=connection.model_dump(
                              exclude_defaults=True,
                              by_alias=True))
    return Connection(**response.json())

def delete_connection(connection_id: str):
    from pycarta import get_agent
    agent = get_agent()
    agent.delete(f'project/connection/{connection_id}')
    return True
