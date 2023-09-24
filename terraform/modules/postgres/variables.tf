variable "region" {
  default     = "eu-west-2"
  description = "AWS region"
}

variable "secret_environment_variables" {
  description = "Env vars for the RDS passed from secret manager"
  type        = map(string)
}
