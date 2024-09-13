""" Core module with cli """
import click
import os
import time
import datetime
import hvac
from pprint import pprint as pp

@click.group()
def main():
    """
    This is a cli for monitoring Vault lockouts

    Example:

    "$> vault-monitor read-locks $VAULT_ADDR $USERNAME $PASSWORD"

    """


@main.command("read-locks", short_help="Read the current locks")
@click.argument("vault-address")
@click.argument("ldap-username")
@click.argument("ldap-password")
def read_locks(vault_address, ldap_username, ldap_password):
    """ Reads the locks in /sys/locked-users in Vault"""
    sleep_delay = 10
    print(f"This will check for locked users every {sleep_delay} seconds.")
    vault_url = vault_address
    client = hvac.Client(url=vault_url)
    login_response = client.auth.ldap.login(
        username=ldap_username,
        password=ldap_password,
    )
    #auth_result = client.is_authenticated()
    #print(f"The result of the call to is_authenticateed is {auth_result}")
    #token = login_response['auth']['client_token']
    #print(f'The client token returned from the LDAP auth method is: {token}')

    while True:
        locked = (client.read('sys/locked-users')['data'])['by_namespace']
        now = datetime.datetime.now()
        stamp = now.strftime("%Y-%m-%d %H:%M:%S")
        print(f"{stamp} --- timestamp")
        if len(locked) > 0:
            print("The following users are locked.")
            pp(locked)
            time.sleep(sleep_delay)
        else:
            print("No users are locked out at the moment")
            time.sleep(sleep_delay)


@main.command("unlock-user", short_help="Send an unlock to the API")
@click.argument("vault-address")
@click.argument("ldap-username")
@click.argument("ldap-password")
@click.argument("mount-accessor")
@click.argument("alias-id")
def read_locks(vault_address, ldap_username, ldap_password, mount_accessor, alias_id):
    """ Sends an unlock request to the API """
    vault_url = vault_address
    client = hvac.Client(url=vault_url)
    login_response = client.auth.ldap.login(
        username=ldap_username,
        password=ldap_password,
    )
    #auth_result = client.is_authenticated()
    #print(f"The result of the call to is_authenticateed is {auth_result}")
    #token = login_response['auth']['client_token']
    #print(f'The client token returned from the LDAP auth method is: {token}')

    url = "sys/locked-users/" + mount_accessor + "/unlock/" + alias_id
    print(f"Sending a POST to this endpoint: {url}")
    result = (client.write(url))
    print(f"Received this response: {result}")
