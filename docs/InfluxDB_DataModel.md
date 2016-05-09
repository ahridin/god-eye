# InfluxDB Data Model.

## Tổ chức Data Model.

| Measurement                  | Tag1  | Tag2  | Field1 | Field2         | Field3       |Time |
|------------------------------|-------|-------|--------|----------------|--------------|-----|
| download_speed               | snode | dnode | speed  | mean_deviation | acceleration |     |
| tcp_three_way_handshake_time | snode | dnode | value  |                |              |     |
| time_to_first_byte           | snode | dnode | value  |                |              |     |
| round_trip_time              | snode | dnode | value  |                |              |     |

  Chú thích:
  ```
    - Measurements:
      + download_speed: tốc độ download các file.
      + tcp_three_way_handshake_time: 
      + time_to_first_byte: 
      + round_trip_time: khoảng thời gian tính từ lúc client bắt đầu gửi request tới lúc nó nhận gói dữ liệu đầu tiên trả về không bao gồm thời gian nhận đầy đủ dữ liệu.
    - Tags:
      + snode: địa chỉ ip source node.
      + snode: địa chỉ ip destination node.
      + region: khu vực địa lý của các node.
    - Fields:
      + mean_deviation: độ biến động của tốc độ download.
      + acceleration: gia tốc của tốc độ download.
      + speed: gía trị tốc độ download.
      + value: giá trị thông số measurement.
    - Time: thời điểm ghi thông tin measuremen (nanosecond).
  ```
## [InfluxDB-Python](https://github.com/influxdata/influxdb-python)

1. Cài đặt.
  
  ```
  $ sudo apt-get install python3-pip
  $ sudo pip install influxdb
  ```

2. Sử dụng.(Đọc [docs](http://influxdb-python.readthedocs.org/en/latest/))

3. Form result gửi đến InfluxDB - Ví dụ
  
  ```
  results = [
    {
        "measurement": "download_speed",
        "tags": {
            "snode": "<source_node_ip>",
            "dnode": "<destination_node_ip>"
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

  
## Các rule trong Kapacitor.
  
  - Kapacitor sử dụng file TICKScripts để định nghĩa các *task*, các task cho biết measurement sẽ xử lý và cách thức xử lý.
  - File TICKScripts cơ bản để xử lý(sample_alert.tick), trong đó, data sẽ được lấy ra từ *sample_measurement*.
    
    ```
    stream
    |from()
        .measurement('sample_measurement')
    |window()
        .period(1m)
        .every(1m)
    |alert()
        .id('{{ .Name }}/{{ index .Tags "snode" }}-{{ index .Tags "dnode"}}')
        .message('[{{ .Time }}] - {{ .ID }} - {{ .Level }} msg: {{ index .Tags "snode" }} to {{ index .Tags "dnode" }} - {{  index .Fields "value"}}')
        // Compare values to running mean and standard deviation
        .ok(lambda: "value" > minimum_ok_threshold and "value" < maximum_ok_threshold)
        .info(lambda: "value" > minimum_info_threshold and "value" < maximum_info_threshold)
        .warn(lambda: "value" > minimum_warn_threshold and "value" < maximum_warn_threshold)
        .crit(lambda: "value" > minimum_crit_threshold and "value" < maximum_crit_threshold)
        .log('/tmp/alerts.log')

        // Post data to custom endpoint
        .post('https://endpoint_to_present_to_dashboard')

        // Execute custom alert handler script
        .exec('/bin/custom_alert_handler.sh')

        // Send alerts to slack
        .slack()
        .channel('#alerts')
        
        // Send alerts to email
        .email().to('oncall@example.com')
    
  
