import click
import argparse
import os
import subprocess
import signal

from .static import static_analysis

@click.group()
def main():
    pass


@click.command()
@click.option('--username', '-u', help='Username for private registry')
@click.option('--password', '-p', help="Password for private registry")
@click.option('--url', '-r', help="URL for private registry")
@click.option('--aws-bucket', '-b', help="S3 upload. Specify bucket name")
@click.option('--account', '-a', help="Anchore STIG UI account. Required for S3 upload")
@click.option('--insecure', '-s', is_flag=True, default=False, help="Allow insecure registries or registries with custom certs")
@click.option('--local-image', '-l', is_flag=True, default=False, help="Run against an image stored locally")
@click.argument('image')
def static(username, password, url, insecure, local_image, image, aws_bucket, account):
    """Run static analysis"""
    aws = aws_bucket
    static_analysis(username, password, url, insecure, local_image, image, aws, account)

@click.command()
def runtime():
    print("Please contact Anchore Sales for access to Anchore's Runtime STIG offering.")

main.add_command(static)
main.add_command(runtime)

if __name__ == '__main__':
    main()
