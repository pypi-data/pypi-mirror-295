import click
import yaml
import os
import openai
from openai import OpenAI

client = OpenAI(api_key=os.getenv('AI_API_KEY'))
import subprocess
from typing import Dict
from dotenv import load_dotenv, set_key

VERSION = "1.0.1"
CONFIG_FILE = os.path.expanduser('~/.ola_config.yaml')
ENV_FILE = os.path.expanduser('~/.ola_env')

def load_config() -> Dict[str, str]:
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
          config = yaml.safe_load(f) or {}
    else:
        config = {}

    if 'sh' not in config:
        config['sh'] = "You are a shell script expert, create terminal command for user's request. it is critical that you send response without any prefix of suffix or ```ssh or ```bash or ```."
        save_config(config)

    return config


def save_config(config: Dict[str, str]):
    with open(CONFIG_FILE, 'w') as f:
        yaml.dump(config, f)

def load_env():
    load_dotenv(ENV_FILE)
    # TODO: The 'openai.api_base' option isn't read in the client API. You will need to pass it when you instantiate the client, e.g. 'OpenAI(base_url=os.getenv('AI_API_BASE', 'https://api.openai.com/v1'))'
    # openai.api_base = os.getenv('AI_API_BASE', 'https://api.openai.com/v1')
    return os.getenv('AI_MODEL', 'gpt-4o-mini')

@click.group()
@click.version_option(version=VERSION)
def cli():
    """OLA - AI Assistant CLI"""
    pass

@cli.command()
@click.argument('user_input')
@click.option('-r', '--run', is_flag=True, help="Run the generated command")
def sh(user_input: str, run: bool):
    """Generate shell commands based on user input."""
    config = load_config()
    prompt = config['sh']
    full_prompt = f"{prompt}\n\nCommand: {user_input}"

    model = load_env()

    try:
        response = client.chat.completions.create(model=model,
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": user_input}
        ])
        generated_command = response.choices[0].message.content.strip()
        click.echo(f"Generated command: {generated_command}")

        if run:
            click.echo("Executing command...")
            try:
                result = subprocess.run(generated_command, shell=True, check=True, text=True, capture_output=True)
                click.echo(result.stdout)
                if result.stderr:
                    click.echo(f"Errors: {result.stderr}", err=True)
            except subprocess.CalledProcessError as e:
                click.echo(f"Command execution failed: {e}", err=True)
                if e.output:
                    click.echo(f"Output: {e.output}")
                if e.stderr:
                    click.echo(f"Errors: {e.stderr}", err=True)
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)

@cli.command()
@click.argument('name')
@click.argument('prompt')
def create(name: str, prompt: str):
    """Create a new prompt and save it to the config file."""
    config = load_config()
    config[name] = prompt
    save_config(config)
    click.echo(f"Prompt '{name}' created successfully.")

@cli.command()
@click.argument('name')
@click.argument('user_input')
def run(name: str, user_input: str):
    """Run a saved prompt with user input."""
    config = load_config()
    if name not in config:
        click.echo(f"Prompt '{name}' not found.")
        return

    prompt = config[name]
    full_prompt = f"{prompt}\n\nUser: {user_input}"

    model = load_env()

    try:
        response = client.chat.completions.create(model=model,
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": user_input}
        ])
        click.echo(response.choices[0].message.content)
    except Exception as e:
        click.echo(f"Error: {str(e)}")

@cli.command()
def list():
    """List all saved prompts."""
    config = load_config()
    if not config:
        click.echo("No prompts saved.")
    else:
        click.echo("Saved prompts:")
        for name, prompt in config.items():
            click.echo(f"  {name}: {prompt}")

@cli.command()
@click.argument('name')
def delete(name: str):
    """Delete a saved prompt."""
    config = load_config()
    if name not in config:
        click.echo(f"Prompt '{name}' not found.")
    else:
        del config[name]
        save_config(config)
        click.echo(f"Prompt '{name}' deleted successfully.")

@cli.command()
@click.option('--key', help='AI API Key')
@click.option('--model', help='AI Model to use')
@click.option('--url', help='AI API base URL')
def update_env(key, model, url):
    """Update environment variables."""
    if key:
        set_key(ENV_FILE, 'AI_API_KEY', key)
        click.echo("API Key updated.")
    if model:
        set_key(ENV_FILE, 'AI_MODEL', model)
        click.echo("Model updated.")
    if url:
        set_key(ENV_FILE, 'AI_API_BASE', url)
        click.echo("API base URL updated.")
    if not any([key, model, url]):
        click.echo("No updates provided. Use --key, --model, or --url to update values.")

@cli.command()
def list_env():
    """List current environment variables."""
    load_dotenv(ENV_FILE)
    click.echo("Current environment settings:")
    click.echo(f"API Key: {'*' * 8}{os.getenv('AI_API_KEY')[-4:] if os.getenv('AI_API_KEY') else 'Not set'}")
    click.echo(f"Model: {os.getenv('AI_MODEL', 'Not set')}")
    click.echo(f"API Base URL: {os.getenv('AI_API_BASE', 'Not set')}")

def main():
    cli()

if __name__ == '__main__':
    main()
