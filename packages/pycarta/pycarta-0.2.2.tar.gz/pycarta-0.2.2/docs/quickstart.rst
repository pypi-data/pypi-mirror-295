.. _quickstart:

Quick Start
===========

.. contents::


Authentication
--------------

Authentication is central to ``pycarta`` operation. This is handled on a session
basis to free the user from having to explicitly pass around an Authorization
Agent. There are several ways to authenticate:

Username and Password
^^^^^^^^^^^^^^^^^^^^^

A call to ``pycarta.login(username=<Carta username>, password=<Carta password>)``
will authenticate into the default environment. Alternatively, a user can be
prompted for their username and password using a pop-up interactive dialogue,
``pycarta.login(interactive=True)``.

.. note::

    By default, Carta will attempt to login to the Carta production host. If
    you need to log into the Carta development host you must specify the
    environment, e.g. ``pycarta.login(environment="development")`` or set an
    environment variable ``CARTA_ENV=development``.
    
    For special Carta deployments or for testing, an explicit host may be
    specified that supercedes the ``environment`` keyword, e.g.
    ``pycarta.login(host="https://...")``. However, this is a very rare use
    case and hardly worth mentioning.

Profiles
^^^^^^^^

A single user may hold several roles and need to pivot between Carta accounts.
While this is possible through repeated username/password challenges, such
challenges can be inconvenient. To accommodate this, users may setup a profile
file that stores usernames, passwords, and environments that are used
regularly. ``pycarta`` will look in ``$HOME/.carta/admin_tools/profiles.ini``
for profiles. These use a standard config format, e.g.,::

    [sandbox]
    username = <USERNAME>
    environment = development
    password = <PASSWORD>

    [production]
    username = <USERNAME>
    environment = production
    password = <PASSWORD>

Once you log in, this file will also contain the Carta API token for this
account, which will be updated as needed and should not be specified
explicitly.

Profiles may be managed programmatically, e.g. using basic CRUD (Create,
Retrieve, Update, and Delete) operations

.. code:: python

    from pycarta.auth import CartaConfig, Profile, ProfileNotFoundException

    config = CartaConfig()

    # Get a list of available profiles
    profiles = config.get_profiles()

    # Create a new profile
    profile = Profile(
        username="test_user",
        environment="production",  # or "development"
        password="your_secure_password",
        profile_name="test_profile",
    )
    config.save_profile("test_profile", profile)

    # Retrieve an existing profile
    try:
        profile = config.get_profile("test_profile")
    exception ProfileNotFoundException:
        # If not found, a ProfileNotFoundException is raised.
        profile = None

    # Update an existing profile
    profile = config.get_profile("test_profile")
    profile.password = "new_password"
    config.save_profile("test_profile", profile)

    # Delete a profile
    config.delete_profile("test_profile")

Profiles may also be managed interactively using the Carta profile UI,

.. code:: python

    from pycarta.auth import CartaProfileUI

    CartaProfileUI()  # A GUI for viewing, adding, or modifying profiles.


Automatic Authentication
^^^^^^^^^^^^^^^^^^^^^^^^

Any action that requires login will attempt to login using information from the
environment. To enable automatic login, set the following environment variables::

    CARTA_USER=<Carta username>
    
    CARTA_PASS=<Carta password>

    CARTA_PROFILE=<Carta profile>

    CARTA_ENV=<Carta environment>  # optional

    CARTA_HOST=<Carta host URL>  # optional

If ``CARTA_PROFILE`` is set, then ``CARTA_USER`` and ``CARTA_PASS`` are
unnecessary. The environment, ``CARTA_ENV``, and host, ``CARTA_HOST``,
variables need only be set if both of the following are true: you are using
username/password authentication and you are not using the production Carta
environment.


Require Authorization
^^^^^^^^^^^^^^^^^^^^^

If you want to ensure that only a select group of people can access a function
you can decorate your function with ``@pycarta.authorize(...)``. This
decorator will check if the authenticated user is part of the list of users or
a member of at least one of the listed groups before the decorated function
will run. For example,

.. code:: python

    import pycarta

    @pycarta.authorize()
    def requires_carta_account():
        print("This will only run if the user is authorized.")

    @pycarta.authorize(users=["Andy", "Beth", "Charlie"])
    def specific_users():
        print("This will only run for Andy, Beth, or Charlie.")

    @pycarta.authorize(groups=["MyOrg:All"])
    def users_in_group():
        print("This will only run for users who are members of 'MyOrg:All'.")


.. _administrative_tasks:

Administrative Tasks
--------------------

The reason to authenticate is to verify identify, and the reason to verify
identity is to exercise some control over who has access to what resources.

Users
^^^^^

``pycarta`` provides create and retrieve operations.

.. code:: python

    from pycarta.admin.user import (
        create_user,
        get_current_user,
        get_user,
        list_users,
        reset_user_password,
    )
    from pycarta.admin.types import User

    # Get the current user
    current_user = get_current_user()

    # Reset the current user's password
    reset_user_password(current_user.username)
    
    # List all users
    user_list = list_users()

    # Create a new user
    new_user = User(
        name="test_user",
        email="test@user.com",
        lastName="Babbott",
        firstName="Alice"
    )
    create_user(new_user)  # Raises an error if user exists.

    # Retrieve a user by email. Can also search by username, first_name
    # last_name and find those that are partial matches. Multiple matches are
    # returned as a list
    alice = get_user(email="alice@myorg.com")

Working with users provides the ultimate fine-grained control over who can
run your function(s), but listing everyone is tedious -- and fragile. The onus
is on you, the developer, to maintain an up-to-date list of users, so it's
often easier to work with groups.

Groups
^^^^^^

``pycarta`` provides create, retrieve, and update operations for groups.
These functions allows the developer to create new groups and to add users to
that group.

.. attention::

    Group names must be unique across the Carta platform. To reduce the risk of
    name conflicts, it is generally good to develop a naming convention that
    narrows the namespace, e.g. "MyCompany:MyGroup". Now your group name must
    only be unique within your company.

    The ``pycarta`` groups API makes this an easy convention to follow. See
    below for an example.

.. code:: python

    from pycarta.admin.types import Group
    from pycarta.admin.user import get_current_user
    from pycarta.admin.group import (
        add_user_to_group,
        create_group,
        list_members as list_group_members,
    )

    user = get_current_user()

    # Create a new group. Raises an exception if the group exists
    group = Group(name="MyGroup", organization="MyCompany")
    create_group(self.group)

    # Add the current user to this group
    add_user_to_group(user, group)

    # List the members of the group
    members = list_group_members(group)


Secrets
^^^^^^^

In addition to management, it can also be helpful to store sensitive
information, such as database usernames and passwords, so they are readily
accessible anywhere you run your code.

``pycarta`` provides secrets management to help store small content like this.

.. note::

    ``pycarta`` secrets cannot be shared between users, so your secret name
    need only be unique to you. This also allows you, the developer, to specify
    a secret name and oblige your users to store their own credentials to
    respect whether they have been given access to a particular resource, such
    as a database.

.. code:: python

    from pycarta.admin.secret import put_secret, get_secret

    put_secret(name="db-username", value="joe")
    put_secret(name="db-password", value="abc123def")

    username = get_secret("db-username")
    password = get_secret("db-password")

Normally, of course, you would want to prompt your user for their
password -- or other sensitive information -- using ``getpass`` or similar.

.. important::

    You may wish to prompt your users to provide their credentials as part of
    your code's execution if those credentials are needed for the code to
    execute properly.
