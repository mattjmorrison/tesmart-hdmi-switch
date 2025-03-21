# Deploy

## create a virtualenv

```
    python3 -m venv .venv
    pip install gunicorn pyserial
```

## Copy app to raspberry pi

```
    scp -r App user@pi:App
    ssh user@pi
    sudo cp App/hdmi.service /etc/systemd/system
    sudo systemctl daemon-reload
    sudo systemctl enable hdmi
    sudo systemctl start hdmi


## Troubleshooting

```
    sudo systemctl
```
