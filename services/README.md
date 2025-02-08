Move `connectaboard.service` to /etc/systemd/system/

## udpate
```sh
sudo cp services/connectaboard.service /etc/systemd/system/connectaboard.service
sudo systemctl daemon-reload
sudo systemctl enable connectaboard

```


## Enable and start
```sh
sudo systemctl daemon-reload
sudo systemctl enable connectaboard
sudo systemctl start connectaboard

```

## View logs
```sh
[service] -f
```

## View status
```sh
sudo systemctl status connectaboard
```
