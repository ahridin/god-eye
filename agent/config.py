rpc_server_url = None  # địa chỉ rpc_server
db_url = None  # địa chỉ của MetricDB
check_timeout = 5
upload_timeout = None  # timeout of sending result to DB
check_interval = 10  # option which APScheduler need


enable_plugin = [
    {
        'name': 'Ping',
        'path': 'check_plugins.ping'
    }
]

# InfluxDB connect configuration
INFLUXDB_HOST = '127.0.0.1'  # InfluxDB Server
INFLUXDB_PORT = 8086
INFLUXDB_USERNAME = 'root'
INFLUXDB_PASSWORD = 'secret_password'
INFLUXDB_DBNAME = 'database_name'
INFLUXDB_DBPASSWORD = 'database_secret_password'
