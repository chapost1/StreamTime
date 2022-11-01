## providers
i.e: AWS/github/netlify/k8s/etc...
you need to define provider so tf will include all needed code to talk with provider.
https://registry.terraform.io/browse/providers



commands:
- terraform init - will download necessary plugins and stuff

- terraform plan - will perform a dry run to check which resources are going to be created/modified/added and etc

- terraform apply - will perform an actual execution to provision the resources

- terraform destroy - will get rid all of the infrastructure (may be dangerous, and therefore should include appropriate parameters in order to specify what to destroy)


