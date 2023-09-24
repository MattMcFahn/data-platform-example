# Main

# Define main modules from local dir
# https://developer.hashicorp.com/terraform/tutorials/modules/module-use

# Main

module "postgres" {
  source = "./terraform/modules/postgres"
  secret_environment_variables = {
    db_password = "${terraform.workspace}/data-platform-example/rds-connection:password"
  }
}

module "code_s3" {
  source      = "./terraform/modules/s3"
  bucket_name = "${local.name}-code-bucket"
}
