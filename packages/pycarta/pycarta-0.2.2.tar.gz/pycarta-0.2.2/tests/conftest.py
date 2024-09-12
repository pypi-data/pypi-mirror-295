"""
    Dummy conftest.py for pycarta.

    If you don't know what this is for, just leave it empty.
    Read more about conftest.py under:
    - https://docs.pytest.org/en/stable/fixture.html
    - https://docs.pytest.org/en/stable/writing_plugins.html
"""

import pytest

@pytest.fixture(scope="session", autouse=True)
def carta_profile():
    """Creates a test profile."""
    import os
    from pycarta.auth import Profile, CartaConfig
    from pycarta.auth.ui import UsernamePasswordDialog
    # Prompt the user for Carta login credentials
    profile = Profile(profile_name="pycarta_pytest_profile")
    profile.username = os.environ.get("CARTA_USER", None)
    profile.password = os.environ.get("CARTA_PASS", None)
    if profile.username is None or profile.password is None:
        credentials = UsernamePasswordDialog("Carta Sandbox Credentials")
        profile.username = credentials.username
        profile.password = credentials.password
    profile.environment = "development"
    CartaConfig().save_profile(profile.profile_name, profile)
    # return the profile
    yield profile
    # Clean up the profiles file
    CartaConfig().delete_profile(profile.profile_name)


@pytest.fixture(scope="session", autouse=True)
def carta_init(carta_profile):
    import pycarta
    pycarta.login(profile=carta_profile.profile_name)
