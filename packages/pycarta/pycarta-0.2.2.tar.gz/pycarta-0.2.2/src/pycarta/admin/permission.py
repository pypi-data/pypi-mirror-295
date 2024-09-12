from .types import (
    ResourceType,
    PermissionsRole,
    UserType,
    Item,
    PermissionEntity,
    get_resource_class,
)
from .types.permissions import convert_permissions_from_str


def resource_types() -> list[ResourceType]:
    from pycarta import get_agent
    agent = get_agent()
    response = agent.get('permissions/resources')
    return [ResourceType(resource) for resource in response.json()]

def get_user_resources(
    resource_type: str | ResourceType,
) -> list[Item]:
    from pycarta import get_agent
    agent = get_agent()
    if isinstance(resource_type, str):
        resource_type = ResourceType(resource_type)
    response = agent.get(f'permissions/resources/{resource_type.value}',
                         params={"userId": None})
    resource_class = get_resource_class(resource_type)
    try:
        return [resource_class(**resource) for resource in response.json()]
    except Exception as e:  # pragma: no cover
        raise ValueError(response.content)

def get_resource(resource_type: str | ResourceType, resource_id: str) -> Item:
    from pycarta import get_agent
    agent = get_agent()
    if isinstance(resource_type, str):
        resource_type = ResourceType(resource_type)
    response = agent.get(f'permissions/resources/{resource_type.value}/{resource_id}')
    return get_resource_class(resource_type)(**response.json())

def get_user_permission(
    resource_id: str,
    user_id: str,
    user_type: str | UserType,
):
    from pycarta import get_agent
    agent = get_agent()
    if isinstance(user_type, str):
        user_type = UserType(user_type)
    response = agent.get(f'permissions/{resource_id}/{user_id}',
                         params={"userType": user_type.value})
    return convert_permissions_from_str(response.text)

def set_user_permission(
    resource_id: str,
    user_id: str,
    user_type: str | UserType,
    role: str | PermissionsRole
):
    from pycarta import get_agent
    agent = get_agent()
    if isinstance(user_type, str):
        user_type = UserType(user_type)
    if isinstance(role, str):
        role = PermissionsRole(role)
    response = agent.put(f'permissions/{resource_id}/{user_id}',
                         params={
                             "userType": user_type.value,
                             "role": role.value, })
    return response.json()

def remove_user_permission(
    resource_id: str,
    user_id: str,
    user_type: str | UserType
):
    from pycarta import get_agent
    agent = get_agent()
    if isinstance(user_type, str):
        user_type = UserType(user_type)
    response = agent.delete(f'permissions/{resource_id}/{user_id}',
                            params={"userType": user_type.value})
    return response.json()

def list_resource_permissions(
    resource_id: str,
    user_type: str | UserType
) -> list[PermissionEntity]:
    from pycarta import get_agent
    agent = get_agent()
    if isinstance(user_type, str):
        user_type = UserType(user_type)
    response = agent.get(f'permissions/{resource_id}/users',
                         params={"userType": user_type.value})
    return [PermissionEntity(**user) for user in response.json()]
