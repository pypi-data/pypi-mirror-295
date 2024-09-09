# Python CLI app to deploy Fusion 5 on Lucidworks GKE labs.
# It will not install Prometheus/Grafana those need to be installed separately.
# It assumes you have gcloud installed.

# Usage: python fusion_deploy.py -cra michael.sanchez@lucidworks.com -cn support -ns testing -prid lw-support-team -zn us-west1 -apw adminPassword

# Author: Michael Sanchez (michael.sanchez@lucidworks.com)

import argparse
import subprocess
import os

def run_command(command):
    print(f"Running: {command}")
    result = subprocess.run(command, shell=True, check=True, text=True)
    return result

def deploy_fusion(args):
    BLUE = '\033[0;34m'
    NC = '\033[0m'

    print(f"\n{BLUE}Setting gcloud core account and project{NC}\n")
    run_command(f"gcloud config set core/account {args.core_account}")
    run_command(f"gcloud config set project {args.project_id}")
    run_command(f"gcloud config set compute/region {args.zone}")

    print(f"\n{BLUE}Getting GKE cluster credentials{NC}\n")
    try:
        run_command(f"gcloud container clusters get-credentials {args.cluster_name} --region {args.zone}")
    except subprocess.CalledProcessError:
        print(f"{BLUE}Error: Could not find cluster {args.cluster_name} in region {args.zone}. Please check the cluster name and region.{NC}")
        return

    print(f"\n{BLUE}Pulling the current fusion-cloud-native git repository{NC}\n")
    run_command("git clone https://github.com/lucidworks/fusion-cloud-native.git")

    os.chdir('fusion-cloud-native')

    print(f"\n{BLUE}Setting kubectl context{NC}\n")
    try:
        context_name = subprocess.check_output(f"kubectl config get-contexts | grep {args.cluster_name} | awk '{{print $2}}'", shell=True, text=True).strip()
        if context_name:
            run_command(f"kubectl config use-context {context_name}")
        else:
            print(f"{BLUE}Error: Could not find context for cluster {args.cluster_name}.{NC}")
            return
    except subprocess.CalledProcessError:
        print(f"{BLUE}Error: Failed to set the correct kubectl context.{NC}")
        return

    print(f"\n{BLUE}Creating the namespace: {args.namespace}{NC}\n")
    run_command(f"kubectl create namespace {args.namespace}")

    print(f"\n{BLUE}Setting namespace as default{NC}\n")
    run_command(f"kubectl config set-context --current --namespace={args.namespace}")

    print(f"\n{BLUE}Running Customize Fusion Values script{NC}\n")
    run_command(f"./customize_fusion_values.sh -c {args.cluster_name} -n {args.namespace} --num-solr 1 --solr-disk-gb 20 --with-resource-limits --with-affinity-rules --skip-crds")

    print(f"\n{BLUE}Making changes to Seldon in fusion values file{NC}\n")
    run_command(f"sed -i '' 's/create: true/create: false/g' gke_{args.cluster_name}_{args.namespace}_fusion_values.yaml")

    print(f"\n{BLUE}Running the upgrade script{NC}\n")
    run_command(f"./gke_{args.cluster_name}_{args.namespace}_upgrade_fusion.sh")

    print(f"\n{BLUE}Setting the admin password{NC}\n")
    if args.admin_password:
        run_command(f"./set_initial_admin_pass.sh {args.admin_password}")
    else:
        run_command("./set_initial_admin_pass.sh")

    print(f"\n{BLUE}Deployment of Fusion 5 to GKE cluster '{args.cluster_name}' completed!{NC}\n")

def main():
    parser = argparse.ArgumentParser(description="Deploy Fusion 5 to a GKE cluster using Python CLI.")
    parser.add_argument('-cra', '--core_account', type=str, required=True, help="Your gcloud core account (e.g., michael.sanchez@lucidworks.com)")
    parser.add_argument('-cn', '--cluster_name', type=str, required=True, help="Name of the GKE cluster")
    parser.add_argument('-ns', '--namespace', type=str, required=True, help="Kubernetes namespace for deployment")
    parser.add_argument('-prid', '--project_id', type=str, required=True, help="GCP Project ID")
    parser.add_argument('-zn', '--zone', type=str, required=True, help="GKE zone or region (e.g., us-west1-b or us-west1)")
    parser.add_argument('-apw', '--admin_password', type=str, required=False, help="Set admin password for Fusion deployment")

    args = parser.parse_args()
    deploy_fusion(args)

if __name__ == "__main__":
    main()