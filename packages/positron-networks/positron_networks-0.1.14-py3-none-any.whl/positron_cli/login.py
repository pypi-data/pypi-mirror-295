import typer
from typing_extensions import Annotated
import requests
import time
import os
import webbrowser
from positron_common.env_config import env
from positron_common.cli_args import args
from positron_common.utils import debug as print_d
from positron_common.user_config import user_config

def login(
  debug: Annotated[bool, typer.Option(help='Enable debug logging')] = False,
):
    """
    Logs you in to your Positron account
    """
    args.init(debug=debug)

    # Get device code
    print('Requesting device code')
    device_code_payload = {
        'client_id': env.AUTH0_CLIENT_ID,
        'scope': 'openid profile',
        'audience': env.AUTH0_AUDIENCE
    }
    device_code_response = requests.post(f'https://{env.AUTH0_DOMAIN}/oauth/device/code', data=device_code_payload)
    if device_code_response.status_code != 200:
        print('Error generating device code')
        raise typer.Exit(code=1)

    device_code_data = device_code_response.json()

    # Redirect to login
    print('1. On your computer or mobile device navigate to: ', device_code_data['verification_uri_complete'])
    print('2. Enter the following code: ', device_code_data['user_code'])
    print('3. Complete the login process')
    print('')
    webbrowser.open(url=device_code_data['verification_uri_complete'], new=2, autoraise=True)

    # Wait for authentication
    access_token = wait_for_access_token(device_code_data)
    print_d(f'Access Token: {access_token}')

    # Get user token
    print('Requesting User Auth Token')
    auth_header = {
        'Authorization': f'Bearer {access_token}'
    }
    user_token_response = requests.get(f'{env.API_BASE}/get-user-auth-token', headers=auth_header)

    if user_token_response.status_code != 200:
        print(user_token_response.json())
        print('Error getting User Auth Token')
        raise typer.Exit(code=1)
    user_token_response_data = user_token_response.json()

    # Save user token
    print(f'Creating positron configuration at: {os.path.expanduser("~/.positron")}')
    save_user_token(user_token_response_data['userAuthToken'])

def wait_for_access_token(device_code_data):
    token_payload = {
        'grant_type': 'urn:ietf:params:oauth:grant-type:device_code',
        'device_code': device_code_data['device_code'],
        'client_id': env.AUTH0_CLIENT_ID
    }
    authenticated = False
    while not authenticated:
        print('Checking if the user completed the flow...')
        token_response = requests.post(f'https://{env.AUTH0_DOMAIN}/oauth/token', data=token_payload)

        token_data = token_response.json()
        if token_response.status_code == 200:
            print('Authenticated!')
            authenticated = True
            return token_data['access_token']
        elif token_data['error'] not in ('authorization_pending', 'slow_down'):
            print(token_data['error_description'])
            raise typer.Exit(code=1)
        else:
            time.sleep(device_code_data['interval'])

def save_user_token(user_token):
    user_config.user_auth_token = user_token
    user_config.write()
    
