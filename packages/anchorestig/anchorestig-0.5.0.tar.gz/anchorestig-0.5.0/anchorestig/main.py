import click
import argparse
import os
import subprocess
import signal

from .static import static_analysis
from .runtime import runtime_analysis, sync_policies
from .inputs import collect_inputs, runtime_get_image_digest, get_runtime_cluster
from .provision import install_cinc, install_train_plugin

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
@click.option("--image", "-i", help="Specify profile to use. Available options are ubuntu-20.04, ubi8, postgres9, apache-tomcat9, crunchy-postgresql, jboss, jre7, mongodb, nginx")
@click.option("--pod", "-p", help="Any running pod running an image that runs one of the specififed profile's software")
@click.option("--container", "-c", help="Container in the pod to run against")
@click.option("--outfile", "-o", help="Output file name. Only JSON output filetype is supported (include the '.json' extension with the output file name in CLI)")
@click.option("--namespace", "-n", help="Namespace the pod is located in")
@click.option("--usecontext", "-u", help="Specify the kubernetes context to use")
@click.option("--aws-bucket", "-b", help="Specify the S3 bucket to upload results to. Omit to skip upload")
@click.option("--account", "-a", help="Specify the Anchore STIG UI account to associate the S3 upload with. Omit to skip upload")
@click.option('--interactive', '-t', is_flag=True, default=False, help="Run in interactive mode")
@click.option('--sync', '-s', is_flag=True, default=False, help="Sync policies from Anchore")
def runtime(image, pod, container, outfile, namespace, usecontext, aws_bucket, account, interactive, sync):
    """Run runtime analysis"""
    print("Runtime Analysis")
    aws = aws_bucket
    if sync:
        sync_policies()
        print("Policies successfully downloaded.")
        if not interactive or not pod or not container:
            return
    if interactive == True:
        input_image, input_pod, input_container, input_namespace, input_usecontext, input_cluster, input_outfile, input_aws_s3_bucket_upload, input_account, input_image_digest, input_image_name = collect_inputs()
        runtime_analysis(input_image, input_pod, input_container, input_namespace, input_usecontext, input_cluster, input_outfile, input_aws_s3_bucket_upload, input_account, input_image_digest, input_image_name)
    else:
        input_image_digest, input_image_name = runtime_get_image_digest(pod, namespace, container)
        input_cluster = get_runtime_cluster(usecontext)
        input_image, input_pod, input_container, input_namespace, input_usecontext, input_outfile, input_aws_s3_bucket_upload, input_account = image, pod, container, namespace, usecontext, outfile, aws, account
        runtime_analysis(input_image, input_pod, input_container, input_namespace, input_usecontext, input_cluster, input_outfile, input_aws_s3_bucket_upload, input_account, input_image_digest, input_image_name)

@click.command()
@click.option('--install', '-i', is_flag=True, default=False, help="Install the necessary version of CINC")
@click.option("--privileged", "-s", is_flag=True, default=False, help="Install CINC with sudo.")
@click.option("--plugin", "-p", is_flag=True, default=False, help="Install the CINC Train K8S Plugin")
def provision(install, privileged, plugin):
    if install:
        install_cinc(privileged)
    if plugin:
        install_train_plugin()

main.add_command(static)
main.add_command(runtime)
main.add_command(provision)

if __name__ == '__main__':
    main()
