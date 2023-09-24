# Example AWS data platform

A repo set up for an example data platform on AWS. Infrastructure is managed in Terraform, and some data processing
applications in python.

See the [infrastructure README](README-infrastructure.md) for details on the platform.

## TODO: Setup guide

Setup guide, and refine/expand the GitHub workflows.

## Validate Terraform

Format
```bash
terraform fmt -recursive
```

Validate
```bash
terraform validate
```

Static Code Analysis
```bash
checkov -s -d .
```

Lint
```bash
tflint --init --loglevel=info
tflint --module --loglevel=info
```

Terraform-Docs
```bash
terraform-docs .
```

Pre-commit
```bash
pre-commit install
pre-commit run --all-files
```

### Deploy from local machine

Initialise the Terraform to install any modules and providers.

```bash
terraform init
```

Select the appropriate Terraform Workspace

Workspaces:
* develop
* prod

```bash
terraform workspace select <Workspace>
```

Run terraform plan to check if any changes will be made to infrastructure.

```bash
terraform plan
```

Run terraform apply to deploy any changes to infrastructure.

```bash
terraform apply --auto-approve
```
