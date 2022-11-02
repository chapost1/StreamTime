# SVN - Stream Video Now

AWS based solution of simple video drive.

Part of a CS degree course <strong>(EASS)</strong> final project.

## Design:

![Architecture Diagram](./assets/architecture_diagram.jpg)

## Prerequisites

Ensure the following are installed:

- <strong>Terraform</strong> - is being used for provisioning.
https://registry.terraform.io/

- <strong>AWS CLI</strong> - is required for PG Schema creation as part of deployment.
https://aws.amazon.com/cli/

### Example Deployment Usage

For the first time, navigate to the deployment folder and run:

```sh
# will download necessary plugins
terraform init
```

Next, from the root directory, to deploy:

```sh
 # on future deployments of an existing cluster, \
 # you may want to use patch db_mode (or none), \
 # and populate the ddl file with relevant sql commands
./deployment/terraform.sh --command apply \
--aws_access_key <AWS_ACCESS_KEY> \
--aws_secret_key <AWS_SECRET_KEY> \
--db_mode init
```

> Note: Provision of resources on AWS with this command can result in invoicing.
