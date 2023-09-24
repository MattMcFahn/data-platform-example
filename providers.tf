# Providers

terraform {
  required_version = "~> 1.3"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.0"
    }
  }
}

provider "aws" {
  region = "eu-west-1"
  alias  = "mgmt"
  assume_role {
    role_arn = "arn:aws:iam::${local.acct_ids["mgmt"]}:role/TerraformRole"
  }
  default_tags {
    tags = local.tags
  }
}
