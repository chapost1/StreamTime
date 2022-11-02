# SVN - Strem Video Now

AWS based solution of simple video drive.

Part of a CS degree course <strong>(EASS)</strong> final project.

## Design:

![Architecture Diagram](./assets/architecture_diagram.jpg)

## Prerequisites

please make sure you install the following:

- <strong>Terraform</strong> is being used for provisioning.
https://registry.terraform.io/

- <strong>AWS CLI</strong> is required for PG Schema creation as part of deployment.
https://aws.amazon.com/cli/

### Example Deployment Usage

For the first time, go into deployment directory and execute:
```sh
terraform init # will download necessary plugins
```

And then, from root directory, to deploy:

```sh
./deployment/terraform.sh --command apply \
--aws_access_key <AWS_ACCESS_KEY> \
--aws_secret_key <AWS_SECRET_KEY> \
--db_mode init
 # on future deployments of an existing cluster, you may use patch mode (or none), and populate the ddl file with relevant sql commands
```

> Note: provisining Resources on AWS using this command may lead to financial expenses.
