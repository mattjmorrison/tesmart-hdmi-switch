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
```

## Deploying Changes to raspberry pi

```
    scp -r App/app.py user@pi:App
    sudo systemctl restart hdmi
```

## Troubleshooting

```
    sudo systemctl status hdmi
    sudo journalctl -u hdmi
```
