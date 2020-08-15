from flask import Flask, render_template, request, current_app

import os
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO
import time

from curl_client import CurlClient

app = Flask(__name__)


def default():
    msg = read('msg.txt')
    script_contents = read('scriptcopy.txt')
    return msg, script_contents


def read(file):
    with open('storage/'+file, 'r') as f:
        return f.read()


def write(file, msg):
    with open('storage/'+file, 'w') as f:
        f.write(msg)


def save(file, msg):
    with open('scripts/'+file, 'w') as f:
        f.write(msg)


def clean(file):
    with open('storage/'+file, 'w+') as f:
        f.truncate()


@app.route('/controller/connect', methods=['POST'])
def connect():
    script_filename, endpoint, msg = '', '', ''
    if request.method == 'POST':
        script_filename = request.form['script_name']
        endpoint = "controller/connect"
        body = {"controller_type": "PRO_CONTROLLER"}
        curl_request = CurlClient(endpoint, body)
        curl_request.curl_post()

    msg, script_contents = default()
    return render_template('index.html', msg=msg, script=script_contents, script_name=script_filename)


@app.route('/controller/disconnect', methods=['POST'])
def disconnect():
    script_filename, endpoint, msg = '', '', ''
    if request.method == 'POST':
        script_filename = request.form['script_name']
        endpoint = "controller/disconnect"
        curl_request = CurlClient(endpoint)
        curl_request.curl_get()

    msg, script_contents = default()
    return render_template('index.html', msg=msg, script=script_contents, script_name=script_filename)

@app.route('/controller/status', methods=['POST'])
def controller_status():
    script_filename, script_contents, endpoint, msg = '', '', '', ''
    if request.method == 'POST':
        script_filename = request.form['script_name']
        endpoint = "controller/status"
        curl_request = CurlClient(endpoint)
        curl_request.curl_get()
        msg = curl_request.response_body
        print("Response body")

    return render_template('index.html', msg=msg, script=script_contents, script_name=script_filename)


@app.route('/btn/combo', methods=['POST'])
def btn_combo():
    script_contents, script_filename, endpoint, msg = '', '', '', ''
    if request.method == 'POST':
        script_filename = request.form['script_name']
        script_contents = request.form['script']
        button_name = request.form['btn']
        buttons = button_name.split(',')
        for button in buttons:
            endpoint = "controller/button/press/" + button
            curl_request = CurlClient(endpoint)
            curl_request.curl_patch()

        time.sleep(.5)
        # TODO: await asyncio.sleep(300 / 1000)

        for button in buttons:
            endpoint = "controller/button/release/" + button
            curl_request = CurlClient(endpoint)
            curl_request.curl_patch()

    return render_template('index.html', msg=msg, script=script_contents, script_name=script_filename)


@app.route('/btn', methods=['POST'])
def btn():
    script_contents, script_filename, endpoint, msg = '', '', '', ''
    if request.method == 'POST':
        button_name = request.form['btn']
        script_contents = request.form['script']
        script_filename = request.form['script_name']
        endpoint = "controller/button/tap/" + button_name
        curl_request = CurlClient(endpoint)
        curl_request.curl_patch()

    return render_template('index.html', msg=msg, script=script_contents, script_name=script_filename)


@app.route('/btn/stick', methods=['POST'])
def btn_r_stick():
    script_contents, script_filename, endpoint, msg = '', '', '', ''
    if request.method == 'POST':
        button_name = request.form['btn']
        script_contents = request.form['script']
        script_filename = request.form['script_name']
        button, cmd = button_name.split(',')
        if button == "r_stick":
            endpoint = "controller/stick/r_stick/center"
        elif button == "l_stick":
            endpoint = "controller/stick/r_stick/center"
        elif button == "rs_right":
            endpoint = "controller/stick/r_stick/x_axis/" + cmd[0]
        elif button == "rs_left":
            endpoint = "controller/stick/r_stick/x_axis/" + cmd[0]
        elif button == "rs_up":
            endpoint = "controller/stick/r_stick/y_axis/" + cmd[0]
        elif button == "rs_down":
            endpoint = "controller/stick/r_stick/y_axis/" + cmd[0]
        elif button == "ls_right":
            endpoint = "controller/stick/l_stick/x_axis/" + cmd[0]
        elif button == "ls_left":
            endpoint = "controller/stick/l_stick/x_axis/" + cmd[0]
        elif button == "ls_up":
            endpoint = "controller/stick/l_stick/y_axis/" + cmd[0]
        elif button == "ls_down":
            endpoint = "controller/stick/l_stick/y_axis/" + cmd[0]
        else:
            print("Error on sticks")

        curl_request = CurlClient(endpoint)
        curl_request.curl_patch()

    return render_template('index.html', msg=msg, script=script_contents, script_name=script_filename)


@app.route('/')
def index():
    msg, script_contents = default()
    return render_template('index.html', msg=msg, script=script_contents)


@app.route('/script/select/load', methods=['POST'])
def load():
    script_contents, script_filename, msg = '', '', ''

    if request.method == 'POST':
        script_filename = request.form['chosen_script']
        with current_app.open_resource('scripts/' + script_filename) as f:
            script_contents = f.read().decode(encoding='UTF-8')
        write('scriptname.txt', script_filename)
        write('scriptcopy.txt', script_contents)

    return render_template('index.html', msg=msg, script=script_contents, script_name=script_filename)


@app.route('/script/run', methods=['POST'])
def run():
    script_contents, script_filename, msg = '', '', ''
    if request.method == 'POST':
        script_filename = request.form['script_name']
        script_contents = request.form['script']
        write('script.txt', script_contents)
        write('scriptcopy.txt', script_contents)
        write('command.txt', 'run')

    return render_template('index.html', msg=msg, script=script_contents, script_name=script_filename)


@app.route('/script/save', methods=['POST'])
def save_script():
    script_contents, script_filename, msg = '', '', ''
    if request.method == 'POST':
        script_filename = request.form['script_name']
        script_contents = request.form['script']
        save(script_filename, script_contents)
        write('scriptcopy.txt', script_contents)

    return render_template('index.html', msg=msg, script=script_contents, script_name=script_filename)


@app.route('/script/stop', methods=['POST'])
def stop():
    script_filename, msg = '', ''
    if request.method == 'POST':
        script_filename = request.form['script_name']
        write('command.txt', 'stop')

    msg, script_contents = default()
    return render_template('index.html', msg=msg, script=script_contents, script_name=script_filename)


def files_scanner(path):
    for file in os.listdir(path):
        if os.path.isfile(os.path.join(path, file)):
            yield file


@app.route('/script/choose', methods=['POST'])
def choose():

    files = []
    for file in files_scanner("scripts"):
        print(file)
        files.append(file)

    return render_template('files.html', files=sorted(files))


if __name__ == '__main__':
    clean('message.txt')
    clean('command.txt')
    clean('script.txt')
    app.run(debug=True, host='0.0.0.0')
