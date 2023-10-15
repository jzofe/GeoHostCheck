# Geohostcheck
 
### Geohostcheck is a powerful host status checker with proxy support.
 
FREE and OPEN-SOURCE!
 
## Features 
 
- Check the status of hosts with different protocols.
- Use proxy servers for checking.
- Highly customizable with user agents.
 * Instant automatic user agent changes if proxy or request is banned
- Easy to use and robust.
- If you don't have a proxy list, geohc will automatically search and download it from the internet.


 
### Protocols 

```python

if protocol == "ICMP":
#imcp proxy ping code...

            elif protocol == "UDP":
                send_udp_packet(target_ip, udp_port, protocol, proxy_address)
            elif protocol == "DNS":
                send_tls_request_to_dns(target_ip, tls_port, protocol, proxy_address, user_agent)
            elif protocol == "TCP":
                send_tcp_request(target_ip, tcp_port, protocol, proxy_address, user_agent)
            elif protocol == "TLS":
                send_tls_request(target_ip, tls_port, protocol, proxy_address, user_agent)
```

## Screenshots
 
![Header](https://github.com/scriptkidsensei/GeoHostCheck/assets/55909183/fea0a2eb-905e-4858-b2a7-17d3d8222ea1)
 
#### Protocol Choice
 
![Screenshot 1](https://github.com/scriptkidsensei/GeoHostCheck/assets/55909183/03ed5f0f-b5e7-4d6f-9139-afe86e4c6a36)
 
![Screenshot 2](https://github.com/scriptkidsensei/GeoHostCheck/assets/55909183/a78db6dd-6a6a-47d7-9dd2-cf8df0f505e9)
 
#### User-agent
 
![Screenshot 3](https://github.com/scriptkidsensei/GeoHostCheck/assets/55909183/f64187de-c789-4cd8-9824-20e79b3dc024)
 
#### Otomatic proxy list installer!
 
![Screenshot 4](https://github.com/scriptkidsensei/GeoHostCheck/assets/55909183/523e67ac-26a0-473e-bb1d-70e734ef3976)
 
## Installation
 
You can install Geohostcheck by cloning this repository:
 
```shell
git clone https://github.com/scriptkidsensei/GeoHostCheck.git
 
```
 
```shell
pip3 install -r requirements.txt
sudo python3 geohc.py
```
 
 
It took me a lot of effort to make this python script. Please star this repo :D
