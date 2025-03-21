import json
import time
from wsgiref.simple_server import make_server
from pathlib import Path, PurePath
import serial


device = '/dev/ttyUSB0'
baud = 9600


ports = {
	8: 'google-tv',
	6: 'apple-tv',
	4: 'ps4',
	2: 'ps3',
	3: 'switch',
}


hex_map = {
	'google-tv': b'\x08',
	'apple-tv': b'\x06',
	'ps4': b'\x04',
	'ps3': b'\x02',
	'switch': b'\x03',
}


def get_current_input():
	s = serial.Serial(device, baud, timeout=1)
	s.write(b'\xAA\xBB\x03\x10\x00\xEE')
	time.sleep(0.5)
	response = s.read(size=8)
	return int(response[4]) + 1


def update_current_input(new):
	s = serial.Serial(device, baud, timeout=1)
	s.write(b'\xAA\xBB\x03\x01' + hex_map[new] + b'\xEE')
	time.sleep(0.5)
	response = s.read(size=8)
	return int(response[4]) + 1


def page(start_response):
	current = get_current_input()
	selected = ports.get(current)
	options = {name: 'current' if name == selected else '' for name in ports.values()}
	status = '200 OK'
	headers = [('Content-type', 'text/html; charset=utf-8')]
	start_response(status, headers)
	return [HTML.format(CSS=CSS, JAVASCRIPT=JAVASCRIPT, **options).encode("utf-8")]


def static(start_response, path):
	status = '200 OK'
	headers = [('Content-type', 'image/png; charset=utf-8')]
	start_response(status, headers)
	with open(Path(__file__).parent / path[1:], 'rb') as f:
		return [f.read()]


def update(start_response, data):
	selected = json.loads(data)['selected']
	update_current_input(selected)
	status = '204 No Content'
	headers = [('Content-type', 'text/plain; charset=utf-8')]
	start_response(status, headers)
	return [''.encode("utf-8")]
	

def app(environ, start_response):
	path = environ['PATH_INFO']
	method = environ['REQUEST_METHOD']
	
	if path == '/' and method == 'GET':
		return page(start_response)
	if path.startswith('/assets') and path.endswith('.png'):
		return static(start_response, path)
	if path == '/update' and method == 'POST':
		return update(start_response, environ['wsgi.input'].read(int(environ['CONTENT_LENGTH'])))

	status = '404 Not Found'
	headers = [('Content-type', 'text/plain; charset=utf-8')]
	start_response(status, headers)
	return ['404'.encode("utf-8")]



CSS = """
body {
	background-color: black;
}
.grid {
	display: grid;
	grid-row-gap: 20px;
}
button {
	background-color: darkgray;
}
button.current {
	background-color: white;
}
button {
	height: 200px;
	padding: 50px;
	background-size: contain;
	background-repeat: no-repeat;
	background-position: center;
}
#google-tv {
	background-image: url('./assets/google-tv.png');
}
#apple-tv {
	background-image: url('./assets/apple-tv.png');
}
#ps4 {
	background-image: url('./assets/ps4.png');
}
#ps3 {
	background-image: url('./assets/ps3.png');
}
#switch {
	background-image: url('./assets/switch.png');
}
"""


JAVASCRIPT = """
document.querySelector(".grid").addEventListener("click", (event) => {
	fetch("/update", {
		method: 'POST',
		body: JSON.stringify({selected: event.target.id})
	})
	document.querySelectorAll('.component').forEach(component => {
		if(component.id == event.target.id) {
			component.classList.add('current');
		}
		else {
			component.classList.remove('current');
		}
	})
});
"""


HTML = """
<!DOCTYPE html>
<html>
    <title>HDMI Switch</title>
    <head>
        <style>{CSS}</style>
    </head>
    <body>
        <div class="grid">
            <button class="component {google-tv}" id="google-tv"></button>
            <button class="component {apple-tv}" id="apple-tv"></button>
            <button class="component {ps4}" id="ps4"></button>
            <button class="component {ps3}" id="ps3"></button>
            <button class="component {switch}" id="switch"></button>
        </div>
    </body>
    <script>{JAVASCRIPT}</script>
</html>
"""

if __name__ == '__main__':
	with make_server('', 8000, app) as httpd:
	    httpd.serve_forever()
