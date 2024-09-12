import os

from gql import Client, gql
from gql.transport.aiohttp import AIOHTTPTransport
from gql.transport.exceptions import TransportQueryError

from trail.exception.trail import TrailUnavailableException
from trail.libconfig import libconfig
from trail.userconfig import MainConfig
from trail.util import auth

FETCH_ALL_PROJECTS = """
    query {
        allProjects {
            id
            title
            mostRecentExperiment {
                id
            }
        }
    }
"""


def get_user_credentials():
    email = input("Email: ")
    api_key = input("API Key: ")
    return email, api_key


def get_endpoint_url():
    url = input("Overwrite Trail Endpoint URL (optional, press Enter to skip): ")
    return url if url else ""


def select_project_and_parent_experiment(auth_header: dict, user_specified_endpoint_url: str):
    try:
        transport = AIOHTTPTransport(
            libconfig.gql_endpoint_url(user_specified_endpoint_url),
            headers=auth_header
        )
        client = Client(transport=transport)
        result = client.execute(document=gql(FETCH_ALL_PROJECTS))
        projects = {
            project["id"]: project
            for project in result["allProjects"]
        }
    except TransportQueryError as e:
        raise TrailUnavailableException() from e

    print("Your projects are listed below:\n")
    print("Project ID | Project Title")
    for project in sorted(projects.values(), key=lambda x: x["id"]):
        print(f"{project['id']}     | {project['title']}")

    while True:
        project_id = input("Select a project ID: ")
        if project_id in projects:
            break

    default_experiment_id = projects[project_id].get('mostRecentExperiment', {}).get('id', 'N/A')
    # TODO: validate parent_experiment ID
    parent_experiment_id = input(
        f"Select a parent experiment ID (Default: {default_experiment_id}): ")
    if not parent_experiment_id:
        parent_experiment_id = default_experiment_id

    return project_id, parent_experiment_id


def create_config(email, api_key, project_id, parent_experiment_id, endpoint_url):
    config = MainConfig(
        os.path.join(os.getcwd(), libconfig.PRIMARY_USER_CONFIG_PATH),
        {
            'endpointUrl': endpoint_url,
            'email': email,
            'apiKey': api_key,
            'projects': {
                'id': project_id,
                'parentExperimentId': parent_experiment_id
            },
        }
    )
    config.save()


def init_environment():
    print(f"Don't have an account yet? Sign up here: {libconfig.TRAIL_SIGN_UP_URL}\n")

    print("Your configuration file will be stored in the current directory. "
          "Make sure that you are in the root directory of your project.")

    email, api_key = get_user_credentials()
    endpoint_url = get_endpoint_url()
    auth_header = auth.build_auth_header(email=email, api_key=api_key)
    project_id, parent_experiment_id = select_project_and_parent_experiment(auth_header,
                                                                            endpoint_url)
    create_config(email, api_key, project_id, parent_experiment_id, endpoint_url)

    print("Initialization completed.")
