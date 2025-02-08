Move `.service` files to /etc/systemd/system/


## Enable and start
```sh
sudo systemctl daemon-reload
sudo systemctl enable connectaboard_[service]
sudo systemctl start connectaboard_[service]

```

## View logs
```sh
journalctl -u connectaboard_[service] -f
```

## View status
```sh
sudo systemctl status connectaboard_[service]
```
