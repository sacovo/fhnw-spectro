from flask import Flask, jsonify, request

from .image import extract_patch, find_patch_position, load_image_from_bytes

app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello, World!"


@app.route("/extract", methods=["POST"])
def extract():
    image = request.files["image"]
    image = load_image_from_bytes(image)
    position = find_patch_position(image)
    patch = extract_patch(image, position)

    return jsonify({"position": position, "patch": patch})


def main():
    app.run(debug=True)


if __name__ == "__main__":
    main()
