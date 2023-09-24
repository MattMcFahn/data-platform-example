# Locals

locals {

  name = "${var.name}-${terraform.workspace}"

  acct_ids = {
    mgmt    = "067875642221"
    develop = "222035250253"
    #    integration = "XXX"
    #    preprod     = "XXX"
    prod = "152565093835"
  }

  #  db_connection = jsondecode(data.aws_secretsmanager_secret_version.rds_connection.secret_string)

  #  provider_profile = local.is_nonprod_env ? "develop" : "prod"

  #  is_nonprod_env = contains(local.non_prod_envs, terraform.workspace) || local.is_feature
  #  is_feature     = length(regexall("[A-Za-z0-9]+-\\d+", terraform.workspace)) > 0

  #  non_prod_envs = ["develop"]
  #  prod_envs     = ["prod"]

  tags = {
    Env     = terraform.workspace
    Project = "data-platform-example"
    Service = "mgmt" # Overridden by service specific deployment
  }

}
