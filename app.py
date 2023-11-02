from flask import Flask, redirect, render_template, request, send_file, send_from_directory, session
from waitress import serve
from io import BytesIO
from zipfile import ZipFile
import utility
import ntpath
import logging
import os
import socket
import webbrowser
import magic


app = Flask(__name__)
app.secret_key = 'WiPi'


logger = logging.getLogger('waitress')
logger.setLevel(logging.INFO)


@app.route('/')
def index():
    return render_template('layout_main.html', Sections=utility.Sections)


@app.route('/layout')
def layout():
    return render_template('layout.html', names=utility.get_file_names())


@app.route('/<section_name>')
def layout_item(section_name):
    sections = [section.name for section in utility.Sections]
    for section in utility.Sections:
        if section.name == section_name:

            if len(section.item_list) > 0:
                return render_template('layout_items.html', section_name=section_name,
                                       item_list=section.item_list, sections=sections, get_name=ntpath.basename)
            else:
                return render_template('layout_error.html', sections=sections, message='This Section Is Empty')
    return render_template('layout_error.html', sections=sections,  message='No Such Section')


@app.route('/select', methods=['GET', 'POST'])
def select():
    if request.method == 'POST':
        session['item'] = request.form.getlist('item')
        if session['item']:
            return render_template('layout_download_open.html')
        else:
            return render_template('layout_error.html',  message='Error')

    else:
        return render_template('layout_error.html',  message='Error')


@app.route('/download_open/<download_open>')
def download_play(download_open):
    items = session['item']
    if download_open == 'download':
        if len(items) == 1:
            item = items[0]
            return send_file(item, as_attachment=True)
        else:
            stream = BytesIO()
            with ZipFile(stream, 'w') as zipfile:
                for item in items:
                    zipfile.write(item, ntpath.basename(item))
            stream.seek(0)
            return send_file(stream, as_attachment=True, download_name='items.zip')
    elif download_open == 'open':
        return redirect('/open')
    else:
        return render_template('layout_error.html', message='Error')


@app.route('/open')
def open():
    items = session['item']
    mime = magic.Magic(mime=True)
    sections = [section.name for section in utility.Sections]
    return render_template('layout_open.html', items=items, mime_from_file=mime.from_file,
                           sections=sections,  get_name=ntpath.basename,
                           get_text=utility.get_text, get_text_pdf=utility.get_text_pdf)


@app.route('/item_image/<path:item_name>')
def get_item(item_name):
    return send_from_directory(utility.PATH, item_name, as_attachment=True)


@app.route('/close')
def close_app():
    os._exit(0)


if __name__ == '__main__':
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    port = 8080
    url = f'http://{local_ip}:{port}/'

    webbrowser.open_new(url)
    serve(app, host='0.0.0.0', port=port)
