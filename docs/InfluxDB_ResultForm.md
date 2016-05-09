# Form result gửi đến InfluxDB - Ví dụ
  
  ```
  results = [
    {
        "measurement": "download_speed",
        "tags": {
            "snode": <source_node_ip>,
            "dnode": <destination_node_ip>
        },
        "time": "2009-11-10T23:00:00Z",
        "fields": {
            "speed": <speed_value>,
            "mean_deviation": <mean_deviation_value>,
            "acceleration": <acceleration_value>
        }
    }
  ]

  ```