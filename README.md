# Datadog Agent Setup on Minikube with Log Forwarding

This guide will walk you through setting up the Datadog Agent on a Minikube cluster and forwarding logs to `datadoghq.eu`.

## Prerequisites

- Minikube installed on your local machine
- Kubernetes configured
- Docker container
- A valid Datadog account (`datadoghq.eu`)
- Your Datadog API and App keys
- Splunk instance with HTTP Event Collector (HEC) enabled
- Sufficient system resources for Minikube (CPU and Memory)
- **Azure DevOps Project**: Ensure you have an Azure DevOps project set up.
- **Self-Hosted Agent**: The pipeline can use either Microsoft-hosted agents or self-hosted agents. If using a self-hosted agent, ensure it's configured properly.
- **SonarQube**: Set up SonarQube and provide the following variables:

  - `SONAR_PROJECT_KEY`: The unique key of the SonarQube project.
  - `SONAR_LINK`: The URL of your SonarQube instance.
  - `SONAR_TOKEN`: Authentication token for accessing SonarQube.

## Steps

1. To ensure your cluster has enough CPU and memory, start Minikube with at least 4 CPUs and 8GB of RAM: `minikube start --cpus=4 --memory=8192 --driver=hyperkit`
2. Install Splunk Connect for Kubernetes

First, download the **Splunk Connect for Kubernetes** Helm chart:

`helm pull https://splunk.github.io/splunk-connect-for-kubernetes/ --destination minikube/helm`

3. Install the Helm Chart

Run the following Helm command to install Splunk Connect for Kubernetes. Ensure you replace the following placeholders:

* `global.splunk.hec.host`: Your Splunk HEC URL (e.g., `http://<splunk-host>:8088`)
* `global.splunk.hec.token`: Your HEC token (e.g., `d7fb1a06-5ae5-4461-b6ff-233bb7212d89`)
* `splunk.adminPassword`: The admin password for the Splunk web interface
* `global.splunk.hec.indexName`: The index name where logs and objects are sent
* `splunk-kubernetes-metrics.splunk.hec.indexName`: The index name for metrics data

### Datadog Agent Deployment

Here’s the sample `deployment.yaml` file for deploying the Datadog agent

#### Enable Log Collection

In the `minikube/k8s/datadog-configmap.yaml` file, ensure logs are enabled and being collected from containers:

#### Forward Logs to Datadog

To forward logs to `datadoghq.eu`, ensure the following environment variables are configured in your Datadog Agent:

* `DD_API_KEY`
* `DD_APP_KEY`
* `DD_SITE=datadoghq.eu`

The logs collected from the Minikube cluster should now appear in the Datadog Logs section.

#### Create a `datadog-secrets` Kubernetes Secret

You need to create a Kubernetes secret to store your Datadog API key and app key.

```bash
kubectl create secret generic datadog-secrets \
  --from-literal=api-key='<YOUR_DD_API_KEY>' \
  --from-literal=app-key='<YOUR_DD_APP_KEY>' \
  --namespace=datadog
```

### Verify Log Collection

You can check if logs are being forwarded by logging into your Datadog dashboard and navigating to the **Logs** section at [Datadog Logs]().

### Key Highlights:

- The **prerequisites** section lists the required tools and API keys.
- Step-by-step **deployment** guide including secret creation, deployment, log collection, and verification.
- A **troubleshooting** section helps identify common issues.

## Azure DevOps CI/CD Pipeline

This repository contains an Azure DevOps pipeline that automates the build, test, SonarQube analysis, and deployment stages for a .NET project, along with approval and artifact publishing steps.

## Pipeline Overview

The pipeline is structured into the following stages:

1. **Approval Request**

   - The `ApproveRelease_Build` stage triggers a manual approval process before proceeding to the build stage.
2. **Build Stage**

   - Restores project dependencies using `.NET SDK`.
   - Builds the project and generates a release build.
3. **SonarQube Analysis**

   - Runs static code analysis with SonarQube.
   - Requires SonarQube project key, host URL, and authentication token to be passed as parameters.
4. **Test Stage**

   - Executes unit tests using the `.NET SDK` and outputs the results in `.trx` format.
5. **Deploy Stage**

   - Placeholder for deploying the application to your environment. (Add your deployment logic here.)
6. **Publish Artifacts**

   - Archives and publishes all pipeline logs as an artifact for future reference.

## Templates

The pipeline reuses two templates to keep the main pipeline clean and maintainable:

1. **SonarQube Template (`sonarqube.yml`)**

   - This template installs SonarQube tools and runs static analysis on the code.
2. **Approval Template (`approval.yml`)**

   - Manages the approval workflow before moving to the build stage.

## Prerequisites

- **Azure DevOps Project**: Ensure you have an Azure DevOps project set up.
- **Self-Hosted Agent**: The pipeline can use either Microsoft-hosted agents or self-hosted agents. If using a self-hosted agent, ensure it's configured properly.
- **SonarQube**: Set up SonarQube and provide the following variables:
  - `SONAR_PROJECT_KEY`: The unique key of the SonarQube project.
  - `SONAR_LINK`: The URL of your SonarQube instance.
  - `SONAR_TOKEN`: Authentication token for accessing SonarQube.

## Usage

1. Clone this repository.
2. Set up your Azure DevOps pipeline:
   - Create a new pipeline in Azure DevOps.
   - Point to the `azure-pipelines.yml` file located in the root of this repository.
3. Modify the following parameters in your pipeline:
   - `SONAR_PROJECT_KEY`
   - `SONAR_LINK`
   - `SONAR_TOKEN`
4. Optionally, adjust the stages and jobs as per your needs (e.g., add deployment steps).

## File Structure

- **application/azure-pipelines/pipeline-file.yaml**: Main pipeline file that defines all the stages.
- **application/templates-pipelines/sonarqube.yml**: Template for running SonarQube analysis (example).
- **application/templates-pipelines/approval.yml**: Template for managing manual approval before the build stage(example).

## Logs & Artifacts

All pipeline logs are archived and published as an artifact at the end of each pipeline run. These logs can be downloaded and reviewed from the Azure DevOps UI.

### Other files:

These files are supporting files for the project.

## Contributing

If you wish to contribute to this project, feel free to fork the repository and submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
