![Termux Logo](./assets/logo/streamtime-logo-white.png#gh-dark-mode-only)
![Termux Logo](./assets/logo/streamtime-logo-black.png#gh-light-mode-only)

<hr>

AWS based solution of simple video drive.

Part of a CS degree course <strong>(EASS)</strong> final project.

You can find more of this course porjects <a href="https://github.com/EASS-HIT-PART-A-2022-CLASS-II">here.</a>

## Features:

The user functionalities which are currently supported include:

:gem: Upload / Delete your videos

:gem: Mark your videos as private so only you can see them, or public and share it with friends

:gem: Watch yours / others public videos

:gem: Explore videos of other users


## Status:

POC :soon: MVP

Quick demonstration of video upload directly to S3 using presigned upload under the hood, it triggers processing steps which also creates thumbnail.
At start, S3 bucket is shown to be empty to demonstrate the upload process.


https://user-images.githubusercontent.com/39523779/203442739-e2baa0b1-eb5a-4318-8889-e265aa7fcdb2.mp4


## Design:

### High Level Diagram

![HL Diagram](./assets/diagrams/hl_architecture_diagram.jpg)

### Video Upload Use Case Sequence Diagram

This diagram is intended to show the relationship between the system components in the case of system-wide usage.

> Note: In order to better understand the diagram below, the async operations are synchronized.
>
> As a result, the time intervals on the diagram are out of true proportions.

![Video Upload Use Case Sequence Diagram](./assets/diagrams/video_upload_use_case_seq_diagram.jpg)

### Web Api Service Diagram

#### Heavily influenced by Robert C. Martin (Uncle Bob), <a href="https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html">The Clean Architecture</a>

This Diagram should explain the relation between the app layers.

![Web Api Service Diagram](./services/api/abstract_web_api_architecture_diagram.jpg)

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


## Contact

Project owner:
> <a href="https://github.com/chapost1"><kbd><img src="https://avatars.githubusercontent.com/u/39523779?s=25"/></kbd></a> &nbsp; Shahar Tal
>
> [Github](https://github.com/chapost1) | [LinkedIn](https://www.linkedin.com/in/shahar-tal-4aa887166/) 

