import io
import os
import signal
import argparse
from PIL import Image
from zipfile import ZipFile

from flask import Flask, render_template, send_file, redirect, request, send_from_directory, url_for, abort
from flask_httpauth import HTTPBasicAuth
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.serving import run_simple

from updog2.utils.path import is_valid_subpath, is_valid_upload_path, get_parent_directory, process_files
from updog2.utils.output import error, info, warn, success
from updog2.utils.images import get_images, reduce_image, generate_zip, clean_zip
import updog2.utils.qr as qr
from updog2 import version as VERSION


def read_write_directory(directory):
    if os.path.exists(directory):
        if os.access(directory, os.W_OK and os.R_OK):
            return directory
        else:
            error('The output is not readable and/or writable')
    else:
        error('The specified directory does not exist')


def parse_arguments():
    parser = argparse.ArgumentParser(prog='updog')
    cwd = os.getcwd()
    parser.add_argument('directory', metavar='DIRECTORY', nargs='?', default=cwd,
                        type=read_write_directory,
                        help='Root directory (optional)\n'
                             '[Default=current working directory]')
    parser.add_argument('-d', '--directory', metavar='DIRECTORY', type=read_write_directory,
                        help='Root directory (optional, overrides positional argument)')
    parser.add_argument('-p', '--port', type=int, default=9090,
                        help='Port to serve [Default=9090]')
    parser.add_argument('-qr', '--qr', action='store_true',
                        help='Generate QR code for the server URL')
    parser.add_argument('-q', '--quiet', action='store_true',
                        help='Do not display the QR code in the webpage')
    parser.add_argument('-i', '--images', action='store_true',
                        help='Display just image files')
    parser.add_argument('--password', type=str, default='',
                        help='Use a password to access the page. (No username)')
    parser.add_argument('--ssl', action='store_true',
                        help='Use an encrypted connection')
    parser.add_argument('--version', action='version',
                        version='%(prog)s v'+VERSION)

    args = parser.parse_args()

    if args.directory:
        args.directory = os.path.abspath(args.directory)

    return args


def main():
    args = parse_arguments()

    app = Flask(__name__)
    auth = HTTPBasicAuth()

    global base_directory
    base_directory = args.directory

    # Deal with Favicon requests
    @app.route('/favicon.ico')
    def favicon():
        return send_from_directory(os.path.join(app.root_path, 'static'),
                                   'images/favicon.ico', mimetype='image/vnd.microsoft.icon')

    ############################################
    # File Browsing and Download Functionality #
    ############################################
    @app.route('/', defaults={'path': None})
    @app.route('/<path:path>')
    @auth.login_required
    def home(path):
        # If there is a path parameter and it is valid
        if path and is_valid_subpath(path, base_directory):
            # Take off the trailing '/'
            path = os.path.normpath(path)
            requested_path = os.path.join(base_directory, path)

            # If directory
            if os.path.isdir(requested_path):
                back = get_parent_directory(requested_path, base_directory)
                is_subdirectory = True

            # If file
            elif os.path.isfile(requested_path):

                # Check if the view flag is set
                if request.args.get('view') is None:
                    send_as_attachment = True
                else:
                    send_as_attachment = False

                # Check if file extension
                (filename, extension) = os.path.splitext(requested_path)
                if extension == '':
                    mimetype = 'text/plain'
                else:
                    mimetype = None

                try:
                    return send_file(requested_path, mimetype=mimetype, as_attachment=send_as_attachment)
                except PermissionError:
                    abort(403, 'Read Permission Denied: ' + requested_path)

        else:
            # Root home configuration
            is_subdirectory = False
            requested_path = base_directory
            back = ''

        if os.path.exists(requested_path):
            qrImage = qr.generate(
                args.port, args.ssl) if not args.quiet else None

            if args.images:
                images = get_images(args.directory, requested_path)
                images_names = [img['filename'] for img in images]
                return render_template('images.html', directory=requested_path, images=images, images_names=images_names, qrImage=qrImage, version=VERSION)

            # Read the files
            try:
                directory_files = process_files(
                    os.scandir(requested_path), base_directory)
            except PermissionError:
                abort(403, 'Read Permission Denied: ' + requested_path)

            return render_template('home.html', files=directory_files, back=back,
                                   directory=requested_path, is_subdirectory=is_subdirectory, qrImage=qrImage, version=VERSION)
        else:
            return redirect('/')

    #############################
    # File Upload Functionality #
    #############################
    @app.route('/upload', methods=['POST'])
    @auth.login_required
    def upload():
        if request.method == 'POST':

            # No file part - needs to check before accessing the files['file']
            if 'file' not in request.files:
                return redirect(request.referrer)

            path = request.form['path']
            # Prevent file upload to paths outside of base directory
            if not is_valid_upload_path(path, base_directory):
                return redirect(request.referrer)

            for file in request.files.getlist('file'):

                # No filename attached
                if file.filename == '':
                    return redirect(request.referrer)

                # Assuming all is good, process and save out the file
                # TODO:
                # - Add support for overwriting
                if file:
                    filename = secure_filename(file.filename)
                    full_path = os.path.join(path, filename)
                    try:
                        file.save(full_path)
                    except PermissionError:
                        abort(403, 'Write Permission Denied: ' + full_path)

            return redirect(request.referrer)

    #############################
    # Image Serve Functionality #
    #############################
    @app.route('/images/<path:path>')
    def serve_image(path):
        if not args.images or not is_valid_subpath(path, base_directory):
            return redirect('/')

        requested_path = os.path.normpath(os.path.join(base_directory, path))
        if not os.path.exists(requested_path):
            abort(404)

        reducedImage = reduce_image(requested_path)
        return send_file(reducedImage, mimetype='image/jpeg')

    # Download image urls
    @app.route('/images/download', defaults={'path': ''})
    @app.route('/images/download/<path:path>')
    def download_image(path):
        if not args.images and not is_valid_subpath(path, base_directory):
            return redirect('/')
        path = os.path.normpath(path)

        return send_from_directory(args.directory, path, as_attachment=True)

    # Download all images in a zip file
    @app.route('/images/download/all', methods=['POST'])
    def download_all_images():
        if not args.images and request.method != 'POST':
            return redirect('/')

        path = request.form['path'] if len(request.form['path']) > 0 else '.'
        if not is_valid_subpath(path, base_directory):
            return redirect('/')

        requested_path = os.path.normpath(os.path.join(base_directory, path))
        zip_path = generate_zip(requested_path)

        return send_file(zip_path, as_attachment=True)

    #############################
    # Switch mode functionality #
    #############################

    @app.route('/mode/<mode>', defaults={'path': ''})
    @app.route('/mode/<mode>/<path:path>')
    def switch_mode(mode, path):
        args.images = True if mode == 'images' else False

        return redirect('/' + os.path.normpath(path))

    # Password functionality is without username
    users = {
        '': generate_password_hash(args.password)
    }

    @auth.verify_password
    def verify_password(username, password):
        if args.password:
            if username in users:
                return check_password_hash(users.get(username), password)
            return False
        else:
            return True

    # Inform user before server goes up
    success('Serving {}...'.format(args.directory, args.port))

    def handler(signal, frame):
        print()
        error('Exiting!')
    signal.signal(signal.SIGINT, handler)

    ssl_context = None
    if args.ssl:
        ssl_context = 'adhoc'

    if args.qr:
        qr.show(args.port, args.ssl)

    run_simple("0.0.0.0", int(args.port), app, ssl_context=ssl_context)


if __name__ == '__main__':
    try:
        main()
    finally:
        clean_zip()
