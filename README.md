### Documents
[**Introduction - Why this project was born**](https://github.com/PiScale/god-eye/blob/agent/docs/Introduction.md)

[**Technology & Architecture Design**](https://github.com/PiScale/god-eye/blob/agent/docs/Architecture.md)

[Agent changelog](https://github.com/PiScale/god-eye/blob/agent/docs/Agent.md)

[Agent-proposal](https://github.com/PiScale/god-eye/blob/agent/docs/Agent-proposal.md)


### How to run?
        
`python3 g_agent.py`

#### Install python3.5:
Deprecated since version 0.0.3.
```
sudo add-apt-repository ppa:fkrull/deadsnakes
sudo apt-get update
sudo apt-get install python3.5
```

### Serf:
#### Install:
1. Download serf: https://www.serfdom.io/downloads.html
2. Coppy to `/usr/local/bin`

#### Run serf:
- Master Node: `serf agent`
- Cluster Node: `serf join $IP` with: `$IP` is ip of Master Node.

- Yêu cầu khi cài đặt: tên của các Node phải khác nhau nếu không sẽ bị lỗi:

```bash
serf: Node name conflicts with another node at 192.168.145.152:7946. Names must be unique! (Resolution enabled: true)
```
=>>Đề xuất ban đầu là đặt hostname của các node khác nhau.