import os
import click
import requests
import json
from tabulate import tabulate
from loguru import logger
import shlex
import sys

# Configure loguru
logger.remove()  # Remove the default handler
logger.add("memos_debug.log", level="DEBUG", rotation="10 MB")

BASE_URL = os.environ.get('MEMOS_BASE_URL')
TOKEN = os.environ.get('MEMOS_ACCESS_TOKEN')

def check_config():
    if not BASE_URL:
        raise click.UsageError("MEMOS_BASE_URL environment variable is not set")
    if not TOKEN:
        raise click.UsageError("MEMOS_ACCESS_TOKEN environment variable is not set")

@click.group()
@click.option('--debug', is_flag=True, help="Enable debug output to console")
def cli(debug):
    """CLI tool for interacting with Memos API"""
    check_config()
    if debug:
        logger.add(sys.stderr, level="DEBUG")

def generate_curl_command(method, url, headers, params, data):
    command = ["curl", "-X", method.upper(), shlex.quote(url)]
    
    for key, value in headers.items():
        command.extend(["-H", shlex.quote(f"{key}: {value}")])
    
    if params:
        query_string = "&".join(f"{key}={value}" for key, value in params.items())
        command[-1] = shlex.quote(f"{url}?{query_string}")
    
    if data:
        command.extend(["-d", shlex.quote(json.dumps(data))])
    
    return " ".join(command)

def api_request(method, endpoint, data=None, params=None):
    headers = {"Authorization": f"Bearer {TOKEN}"} if TOKEN else {}
    data = data or {}
    params = params or {}

    url = f"{BASE_URL}/{endpoint}"
    try:
        logger.debug(f"API Request: {method} {url}")
        logger.debug(f"Headers: {headers}")
        logger.debug(f"Params: {params}")
        logger.debug(f"Data: {data}")

        curl_command = generate_curl_command(method, url, headers, params, data)
        logger.debug(f"Curl command: {curl_command}")

        response = requests.request(method, url, json=data, params=params, headers=headers)
        
        logger.debug(f"API Response Status: {response.status_code}")
        logger.debug(f"API Response Headers: {response.headers}")
        logger.debug(f"API Response Content: {response.text}")

        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        error_message = str(e)
        if e.response is not None:
            try:
                error_data = e.response.json()
                error_message = f"Error {error_data.get('code')}: {error_data.get('message')}"
            except ValueError:
                pass
        click.echo(f"API request failed: {error_message}", err=True)
        logger.exception(f"API request failed: {error_message}")
        raise click.Abort()
    except json.JSONDecodeError:
        click.echo("Invalid JSON response from server", err=True)
        logger.exception("Invalid JSON response from server")
        raise click.Abort()

def check_base_url():
    if not BASE_URL:
        raise click.UsageError("MEMOS_BASE_URL environment variable is not set")

@cli.command()
@click.option('--content', prompt=True)
@click.option('--visibility', type=click.Choice(['PRIVATE', 'PROTECTED', 'PUBLIC']), default='PRIVATE')
def create(content, visibility):
    """Create a new memo"""
    data = {'content': content, 'visibility': visibility}
    response = api_request('POST', 'api/v1/memos', data=data)
    click.echo(f"Memo created with UID: {response['uid']}")

@cli.command()
@click.option('--page-size', default=10, help='Number of memos to retrieve')
def list(page_size):
    """List memos"""
    params = {'pageSize': page_size}
    response = api_request('GET', 'api/v1/memos', params=params)
    memos = response.get('memos', [])
    table = [[memo['uid'], memo['content'][:50], memo['createTime']] for memo in memos]
    click.echo(tabulate(table, headers=['UID', 'Content', 'Created At']))

@cli.command()
@click.argument('memo_uid')
def get(memo_uid):
    """Get a specific memo"""
    response = api_request('GET', f'api/v1/memos/{memo_uid}')
    click.echo(json.dumps(response, indent=2))

@cli.command()
@click.argument('memo_uid')
@click.option('--content', prompt=True)
def update(memo_uid, content):
    """Update a memo"""
    data = {'content': content}
    response = api_request('PATCH', f'api/v1/memos/{memo_uid}', data=data)
    click.echo("Memo updated successfully")

@cli.command()
@click.argument('memo_uid')
def delete(memo_uid):
    """Delete a memo"""
    api_request('DELETE', f'api/v1/memos/{memo_uid}')
    click.echo("Memo deleted successfully")

@cli.command()
@click.option('--force', is_flag=True, help="Skip confirmation prompt")
def delete_all(force):
    """Delete all memos"""
    if not force:
        click.confirm("Are you sure you want to delete all memos? This action cannot be undone.", abort=True)
    
    page_size = 100  # Adjust this value based on API limitations
    deleted_count = 0
    total_memos = 0

    while True:
        params = {'pageSize': page_size}
        response = api_request('GET', 'api/v1/memos', params=params)
        memos = response.get('memos', [])
        
        if not memos:
            break

        total_memos += len(memos)
        
        with click.progressbar(memos, label=f"Deleting memos (batch of {len(memos)})") as bar:
            for memo in bar:
                try:
                    memo_name = memo['name']
                    api_request('DELETE', 'api/v1/'+memo_name)
                    deleted_count += 1
                except Exception as e:
                    logger.error(f"Failed to delete memo {memo_name}: {str(e)}")
                    click.echo(f"Failed to delete memo {memo_name}: {str(e)}", err=True)
                    breakpoint()

    click.echo(f"Deletion complete. {deleted_count} out of {total_memos} memos were successfully deleted.")

if __name__ == '__main__':
    cli()