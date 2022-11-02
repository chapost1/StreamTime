![Termux Logo](./assets/logo/streamtime-logo-white-colorful.png#gh-dark-mode-only)
![Termux Logo](./assets/logo/streamtime-logo-black-colorful.png#gh-light-mode-only)

<hr>

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

First, navigate to the deployment directory and run:

```bash
# will download necessary plugins
foo@bar:~ (main) $ terraform init
```

Next, from the root directory, to deploy:

```bash
# During future deployments of an existing cluster,
# You can use the db_mode patch (or none),
# And fill the dll file with the relevant SQL commands.
foo@bar:~ (main) $ ./deployment/terraform.sh --command apply \
--aws_access_key <AWS_ACCESS_KEY> \
--aws_secret_key <AWS_SECRET_KEY> \
--db_mode init
```

> Note: Provision of resources on AWS with this command can result in invoicing.
