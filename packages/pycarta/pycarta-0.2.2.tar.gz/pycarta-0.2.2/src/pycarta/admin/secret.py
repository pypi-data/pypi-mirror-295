import warnings


def put_secret(name: str, value: str):
    from pycarta import get_agent
    if "_" in name:
        warnings.warn("Secret names should not contain underscores. Replacing with hyphens.")
        name = name.replace("_", "-")
    if len(value) > 1024:
        raise ValueError("Secret values should be less than 1024 characters.")
    agent = get_agent()
    agent.put('secrets', headers={f"secret-{name}": value})

def get_secret(name: str):
    from pycarta import get_agent
    if "_" in name:
        warnings.warn("Secret names should not contain underscores. Replacing with hyphens.")
        name = name.replace("_", "-")
    agent = get_agent()
    response = agent.get('secrets', params={"name": name})
    return response.text
