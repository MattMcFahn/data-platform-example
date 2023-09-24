# Main

resource "aws_db_instance" "transactional" {
  identifier          = "transactional"
  instance_class      = "db.t4g.micro"
  allocated_storage   = 4
  engine              = "postgres"
  engine_version      = "14.1"
  storage_encrypted   = true
  username            = "root"
  password            = random_password.rds_password.result
  publicly_accessible = false
  skip_final_snapshot = true
}

# TODO: Add in SSM to set passwords
resource "random_password" "rds_password" {
  length  = 17
  special = false
}
