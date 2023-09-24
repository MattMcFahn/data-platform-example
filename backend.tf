# Backend

terraform {
  #  backend "s3" {
  #    bucket         = "loading-data"
  #    key            = "tf_state"
  #    region         = "eu-west-2"
  #    dynamodb_table = "backend-state"
  #    profile        = "mgmt"
  #  }
  # TODO: Remote state
  backend "local" {

  }
}
