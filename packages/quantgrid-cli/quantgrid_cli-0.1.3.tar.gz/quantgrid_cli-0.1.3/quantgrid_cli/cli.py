import click
import os
import shutil
import requests
import logging
import re
import time
import threading
from quantgrid_cli.auth import authenticate, store_token
import jwt

logging.basicConfig(level=logging.INFO)

AUTH_SERVER_API = 'https://auth.quantgrid.net/auth'  # Make sure this matches your actual auth server URL
QUANTGRID_DEV_MODE=''
# Add this near the top of the file, after imports
DEV_MODE = os.environ.get('QUANTGRID_DEV_MODE', QUANTGRID_DEV_MODE).lower() == 'true'

# Get the absolute path to the directory containing the script
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))


def display_welcome():
    """Display ASCII art and welcome message."""
    ascii_art = """
    ██████╗ ██╗   ██╗ █████╗ ███╗   ██╗████████╗ ██████╗ ██████╗ ██╗██████╗ 
    ██╔═══██╗██║   ██║██╔══██╗████╗  ██║╚══██╔══╝██╔════╝ ██╔══██╗██║██╔══██╗
    ██║   ██║██║   ██║███████║██╔██╗ ██║   ██║   ██║  ███╗██████╔╝██║██║  ██║
    ██║▄▄ ██║██║   ██║██╔══██║██║╚██╗██║   ██║   ██║   ██║██╔══██╗██║██║  ██║
    ╚██████╔╝╚██████╔╝██║  ██║██║ ╚████║   ██║   ╚██████╔╝██║  ██║██║██████╔╝
     ╚══▀▀═╝  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝╚═╝╚═════╝ 
    """
    click.echo(click.style(ascii_art, fg='cyan', bold=True))
    click.echo(click.style("Welcome to QuantGrid CLI!", fg='green', bold=True))

def copy_boilerplate(project_name):
    boilerplate_dir = os.path.join(SCRIPT_DIR, 'boilerplate')
    target_dir = os.path.join(os.getcwd(), project_name)
    if not os.path.exists(boilerplate_dir):
        logging.error('Boilerplate directory not found.')
        click.echo('Error: Boilerplate directory not found.')
        return False
    try:
        shutil.copytree(boilerplate_dir, target_dir)
        return True
    except Exception as e:
        logging.error(f'Error copying boilerplate files: {str(e)}')
        click.echo(f'Error copying boilerplate files: {str(e)}')
        return False

@click.group()
def cli():
    """QuantGrid CLI for managing data science and machine learning workflows."""
    pass

def progress_bar_animation(stop_event):
    with click.progressbar(length=100, label='Creating deployment') as bar:
        while not stop_event.is_set():
            time.sleep(0.1)
            bar.update(0.25)
        bar.update(100)  # Set to 100% when stop_event is set

@cli.command()
@click.argument('project_name')
def deploy(project_name):
    """Deploy a new Quantgrid project."""
    try:
        display_welcome()
        # Authenticate user
        token = authenticate()
        if not token:
            click.echo('Authentication failed. Please try again.')
            return

        # Store token
        store_token(token)

        if not DEV_MODE:
            # Create payment link and check subscription status
            subscription_status = check_subscription_status(token, "mlflow")
            if not subscription_status['subscription_active']:

                payment_link = create_payment_link(token)
                if not payment_link:
                    click.echo('Failed to create payment link. Please try again.')
                    return

                click.echo(click.style(f"\n To complete your free trial, please visit:", fg='green', bold=True))
                click.echo(click.style(f"{payment_link}", fg='blue', bold=True))
                click.echo(click.style("Press Enter when you've completed the subscription process.",  bold=False))
                input()

                # Check subscription status using the new endpoint
                max_retries = 5
                for attempt in range(max_retries):
                    subscription_status = check_subscription_status(token, "mlflow")
                    if subscription_status['subscription_active']:
                        break
                    if attempt < max_retries - 1:
                        click.echo('Subscription not found or inactive. Waiting a few seconds before trying again...')
                        time.sleep(5)  # Wait for 5 seconds before retrying
                    else:
                        click.echo('Subscription not found or inactive after multiple attempts. Please complete the subscription process and try again.')
                        return
        else:
            click.echo(click.style("DEV MODE: Skipping subscription check", fg="yellow", bold=True))

        subscription = check_subscription_status(token, "mlflow")
        
        if has_active_deployment(token, "mlflow"):
            click.echo(click.style("You already have an active deployment.", fg="yellow", bold=True))
            return
        # Create deployment
        deployment_data = create_deployment(token, subscription['stripe_subscription_id'])

        if not deployment_data:
            raise click.ClickException("Failed to create deployment. Please try again.")

        username = deployment_data['mlflow_username']
        password = deployment_data['mlflow_password']
        tracking_uri = deployment_data['url']

        try:
            if copy_boilerplate(project_name):
                # Set URL and MLFlow credentials in .env file
                add_env_variables(project_name, tracking_uri, username, password)
                
                run_experiment = click.confirm(click.style("Do you want to run the first experiment?", fg="cyan", bold=True), default=True)
                if run_experiment:
                    # Change directory to the new project
                    project_dir = os.path.join(os.getcwd(), project_name)
                    os.chdir(project_dir)
                    
                    # Install requirements
                    click.echo('Installing requirements...')
                    os.system('pip install -r requirements.txt')
                    
                    # Run the main.py file
                    click.echo('Running your first experiment...')
                    os.system('python main.py')
                    
                    # Change back to the original directory
                    os.chdir('..')
                else:
                    click.echo('No problem, you can run it later with `quantgrid run`')
                    click.echo(click.style(f"You can find your project in the {project_name} directory.", fg="yellow"))
            else:
                click.echo('Failed to initialize project.')
        except Exception as e:
            logging.error(f'Failed to copy boilerplate files: {str(e)}')
            click.echo(f'Failed to initialize project: {str(e)}')
    except Exception as e:
        logging.error(f'An unexpected error occurred: {str(e)}')
        click.echo(f'An unexpected error occurred: {str(e)}')

def add_env_variables(project_name, tracking_uri, username, password):
    """Set URL and MLFlow credentials in .env file."""
    env_path = os.path.join(os.getcwd(), project_name, '.env')
    try:
        with open(env_path, 'w') as f:
            f.write(f"MLFLOW_TRACKING_URI={tracking_uri}\n")
            f.write(f"MLFLOW_TRACKING_USERNAME={username}\n")
            f.write(f"MLFLOW_TRACKING_PASSWORD={password}\n")
    except IOError as e:
        logging.error(f"Failed to write environment variables: {str(e)}")

def create_payment_link(token, product="mlflow", plan="starter", cycle="monthly"):
    """Create a payment link for the user."""
    headers = {
        'Authorization': f'Bearer {token["access_token"]}',
        'Content-Type': 'application/json'
    }
    payload = {
        'product': product,
        'plan': plan,
        'cycle': cycle
    }
    response = requests.post('https://payments.quantgrid.net/create-payment-link', 
                             headers=headers, 
                             json=payload)
    if response.status_code == 200:
        data = response.json()
        return data['payment_link']
    else:
        logging.error(f'Failed to create payment link: {response.text}')
        return None

def check_subscription_status(token, service):
    """Check the user's subscription status using the new endpoint."""
    headers = {'Authorization': f'Bearer {token["access_token"]}', 'credentials': 'include'}
    
    response = requests.get(f'{AUTH_SERVER_API}/subscription-status', headers=headers)
    if response.status_code == 200:
         subscriptions = response.json()['subscriptions']
         for subscription in subscriptions:
            if service in subscription['product']:
                return { 'subscription_active': subscription['status'] in ['active', 'trialing'], **subscription }
        
         return {'subscription_active': False}
    else:
        logging.error(f'Failed to check subscription status: {response.text}')
        return {'subscription_active': False}


def has_active_deployment(token, service):
    """Check the user's subscription status using the new endpoint."""
    headers = {'Authorization': f'Bearer {token["access_token"]}', 'credentials': 'include'}
    
    response = requests.get(f'{AUTH_SERVER_API}/subscription-status', headers=headers)
    if response.status_code == 200:
         subscriptions = response.json()['subscriptions']
         for subscription in subscriptions:
            if service in subscription['product']:
                if subscription['deployment_id']:
                    return True
        
    else:
        logging.error(f'Failed to check subscription status: {response.text}')
    
    return False


@cli.command()
@click.option('--after-init', is_flag=True, default=False, hidden=True)
def run(after_init=False):
    """Run the current project's main.py file."""
    if not after_init and not os.path.exists('main.py'):
        click.echo('Error: main.py not found in the current directory.')
        return
    
    try:
        os.system('python main.py')
    except Exception as e:
        click.echo(f'An error occurred while running the experiment: {str(e)}')



@cli.command()
def update():
    """Update QuantGrid CLI to the latest version."""
    click.echo('Checking for updates...')
    try:
        # This is a placeholder URL. Replace with the actual URL for your package.
        response = requests.get('https://get.quantgrid.net/cli/latest-version')
        latest_version = response.json()['version']
        current_version = '0.1.0'  # Replace with actual version tracking
        
        if latest_version > current_version:
            click.echo(f'New version available: {latest_version}')
            click.echo('To update, run: pip install --upgrade quantgrid-cli')
        else:
            click.echo('You are already using the latest version.')
    except Exception as e:
        click.echo(f'Failed to check for updates: {str(e)}')

def validate_deployment_name(name):
    return bool(re.match('^[a-zA-Z0-9-]+$', name))

# Add this function to decode the token
def decode_token(token):
    try:
        # This assumes you're using PyJWT. If not, adjust accordingly.
        return jwt.decode(token['access_token'], options={"verify_signature": False})
    except jwt.PyJWTError:
        logging.error('Failed to decode token')
        return {}

def create_deployment(token, subscription_id):
    """Create a new deployment and return the deployment data."""
    while True:
        deployment_name = click.prompt(click.style("Enter a name for your deployment", fg="cyan", bold=True))
        if validate_deployment_name(deployment_name):
            break
        click.echo(click.style("Invalid deployment name. Use only alphanumeric characters and hyphens.", fg="red"))

    click.echo(click.style("Your deployment is being prepared, this can take about 1 minute. Thanks for your patience!", fg="yellow"))
    
    headers = {'Authorization': f'Bearer {token["access_token"]}', 'Connection': 'keep-alive', 'credentials': 'include'}
    max_retries = 3
    retry_delay = 5

    for attempt in range(max_retries):
        stop_event = threading.Event()
        progress_thread = threading.Thread(target=progress_bar_animation, args=(stop_event,))
        progress_thread.start()

        try:
            response = requests.post(
                f"{AUTH_SERVER_API}/create-deployment",
                headers=headers,
                params={"name": deployment_name, "stripe_subscription_id": subscription_id},
                timeout=(10, 60)
            )
            
            # Stop the progress bar animation
            stop_event.set()
            progress_thread.join()

            # Handle 400 error without retrying
            if response.status_code == 400:
                click.echo(click.style(f"\nError: {response.json()['detail']}", fg="red"))
                return None
            
            response.raise_for_status()  # Raise an exception for other non-200 status codes

            if response.status_code == 200:
                deployment_data = response.json()
                click.echo("\n")
                click.echo(click.style("Deployment created successfully!", fg="green"))
                click.echo(click.style("----------------------------------------", fg="green"))
                click.echo(click.style(f"Deployment URL: {deployment_data['url']}", fg="green"))
                click.echo(click.style(f"Username: {deployment_data['mlflow_username']}", fg="green"))
                click.echo(click.style(f"Password: {deployment_data['mlflow_password']}", fg="green"))
                click.echo(click.style("----------------------------------------", fg="green"))
                click.echo("")
                click.echo(click.style("Please save this information for future reference.", fg="yellow"))
                click.echo(click.style("You can also find this information in the .env file in your project directory.", fg="yellow"))
                click.echo("")
                return deployment_data
            
        except requests.exceptions.RequestException as e:
            stop_event.set()
            progress_thread.join()
            
            if attempt < max_retries - 1:
                click.echo(click.style(f"\nError creating deployment (attempt {attempt + 1}/{max_retries}): {str(e)}", fg="yellow"))
                click.echo(click.style(f"Retrying in {retry_delay} seconds...", fg="yellow"))
                time.sleep(retry_delay)
            else:
                click.echo(click.style(f"\nFailed to create deployment after {max_retries} attempts: {str(e)}", fg="red"))
                return None

    return None

if __name__ == '__main__':
    cli()