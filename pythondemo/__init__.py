import os


from flask import Flask, url_for


def create_app():
    app = Flask(__name__, static_url_path='', template_folder='templates')

    root = os.path.dirname(app.root_path)

    app.static_folder = os.path.join(root, "pythondemo", "public")

    @app.route("/")
    def hello():
        img_url = url_for('static', filename='/images/logo-small.png')

        return "<h1 style='color:blue'>Hello There!</h1><div><img " \
            + f"src=\"{img_url}\"></div>"

    @app.after_request
    def default_headers(response):
        response.headers["Cache-Control"] = "no-cache, must-revalidate"
        return response

    return app
