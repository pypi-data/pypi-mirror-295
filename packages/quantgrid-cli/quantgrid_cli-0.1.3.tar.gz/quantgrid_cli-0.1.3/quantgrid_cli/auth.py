import time
import click
import jwt
import requests
import os
import yaml

AUTH_SERVER_API = "https://auth.quantgrid.net/auth"

def authenticate():
    stored_token = get_stored_token()

    if stored_token:
        response = requests.post(
            f"{AUTH_SERVER_API}/refresh",
            json={"refresh_token": stored_token['refresh_token']},
            headers={"Content-Type": "application/json"}
        )
        if response.status_code == 200:
            token = response.json()
            store_token(token)
            return token

    """Authenticate user using OTP."""
    click.echo(click.style("Let's get you authenticated.", fg='yellow'))
    
    while True:
        email = click.prompt("Enter your email")
        
        # Send OTP
        response = requests.post(f"{AUTH_SERVER_API}/sign-in-with-otp", params={"email": email})

        if response.status_code == 422:
            click.echo("Invalid email format. Please try again.")
            continue
        elif response.status_code != 200:
            click.echo(f"Failed to send OTP. Status code: {response.status_code}")
            return None

        click.echo(click.style("Login code sent to your email.", fg="green"))
        
        while True:
            otp = click.prompt("Enter the 6-digit code")

            # Verify OTP
            response = requests.post(f"{AUTH_SERVER_API}/verify-otp", json={"email": email, "otp": otp})

            if response.status_code == 200:
                break
            else:
                click.echo(f"Invalid OTP. Status code: {response.status_code}")
                click.echo("Please try again.")

        data = response.json()
        return data


def store_token(token):
    """Store the authentication token securely."""
    config_dir = os.path.expanduser('~/.quantgrid')
    os.makedirs(config_dir, exist_ok=True)
    config_file = os.path.join(config_dir, 'config.yaml')
    
    config = token
    
    with open(config_file, 'w') as f:
        yaml.dump(config, f)
    

def get_stored_token():
    """Retrieve the stored authentication token."""
    config_file = os.path.expanduser('~/.quantgrid/config.yaml')
    
    if not os.path.exists(config_file):
        return None
    
    with open(config_file, 'r') as f:
        config = yaml.safe_load(f)
    
    return config

