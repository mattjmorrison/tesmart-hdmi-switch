
create a virtualenv
python3 -m venv .venv
install gunicorn pyserial

copy App directory to /home/mattjmorrison/App
copy hdmi.service to /etc/systemd/system
sudo systemctl daemon-reload
sudo systemctl enable hdmi
sudo systemctl start hdmi
