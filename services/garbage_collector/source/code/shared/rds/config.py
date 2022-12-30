import common.environment as environment

# Postgres DSN congirations
config = {
    "host": environment.RDS_HOST,
    "port": environment.RDS_PORT,
    "user": environment.RDS_USER,
    "password": environment.RDS_PASSWORD,
    "database": environment.RDS_DB,
}
