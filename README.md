![Termux Logo](./assets/logo/streamtime-logo-white-colorful-clean.png#gh-dark-mode-only)
![Termux Logo](./assets/logo/streamtime-logo-black-colorful-clean-2nd.png#gh-light-mode-only)

<hr>

AWS based solution of simple video drive.

Part of a CS degree course <strong>(EASS)</strong> final project.

## Design:

![Architecture Diagram](./assets/architecture_diagram.jpg)

## Prerequisites

#### Ensure the following are installed:

- <b>Docker</b> - is needed to build images.

    https://www.docker.com/

- <b>Terraform</b> - is being used for provisioning.

    https://registry.terraform.io/

- <b>AWS CLI</b> - is required for RDS Schema creation as part of deployment.

    https://aws.amazon.com/cli/

#### Ensure the following are already exist:

- <b>AWS Account</b> - deployment is going to request for cloud resources from AWS and therefore, an account is required.

    https://aws.amazon.com/

- <b>AWS Route53 Hosted zone /w Domain</b> - deployment step includes:
  - Certificate creation for Cloudfront and domain for frontend.
  - Certificate creation for HTTPS connection to the Web server's Load balancer.

  Thus, to create & validate this certificate automatically, first, a valid domain should be registered.

    Route53 Domain registration step-by-step guide (zone will be created automatically):

    https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/domain-register.html

## Deployment

First, navigate to the deployment directory and run:

```bash
# will download necessary plugins
foo@bar:~ (main) $ terraform init
```

Next, from the root directory, to deploy:

> Make sure the length of your app name does not exceed 18 bytes, as it is used as an identifier in some resources that restrict the length of their identifier.

```bash
# During future deployments of an existing cluster,
# You can use the db_mode patch (or none),
# And fill the dll file with the relevant SQL commands.
foo@bar:~ (main) $ ./deployment/terraform.sh --command apply \
--aws_access_key <AWS_ACCESS_KEY> \
--aws_secret_key <AWS_SECRET_KEY> \
--app_name <APP_NAME> \
--domain <REGISTERED ROUTE53 DOMAIN> \
--db_mode init
```

> ### Note: Provision of resources on AWS with this command can result in invoicing.

## Baseline Roadmap

### Provisioning

&nbsp;&nbsp; :white_check_mark: Network

&nbsp;&nbsp; :white_check_mark: RDS provisioning

&nbsp;&nbsp; :white_check_mark: Serverless processing Lambda workers

&nbsp;&nbsp; :white_check_mark: SNS between processing updates and WSS

&nbsp;&nbsp; :white_check_mark: Websocket communication mamagement via API GW

&nbsp;&nbsp; :white_check_mark: Webserver CF serve Web app

&nbsp;&nbsp; :white_check_mark: RDS DDL init script

&nbsp;&nbsp; :white_check_mark: Web Api Tasks Execution

&nbsp;&nbsp; :white_check_mark: Buckets lifecycle def

&nbsp;&nbsp; :white_check_mark: TLS

&nbsp;&nbsp; :black_square_button: Provision Videos deleter service as a scheduled operation


### Software

&nbsp;&nbsp; :white_check_mark: New video processing Lambda worker

&nbsp;&nbsp; :white_check_mark: Image resizer Lambda worker (for thumbnail)

&nbsp;&nbsp; :white_check_mark: RDS records update Lambda worker

&nbsp;&nbsp; :white_check_mark: WSS Connections store Lambda worker

&nbsp;&nbsp; :white_check_mark: Web api videos management

&nbsp;&nbsp; :black_square_button: Web app videos UI

&nbsp;&nbsp; :black_square_button: Web api mark as delete for later handling

&nbsp;&nbsp; :black_square_button: Videos deleter service logic

&nbsp;&nbsp; :black_square_button: Web api users management

&nbsp;&nbsp; :black_square_button: Web api authentication management

&nbsp;&nbsp; :black_square_button: Web app authentication UI
