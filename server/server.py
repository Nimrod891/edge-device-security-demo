from flask import Flask, request
import ssl
import os

app = Flask(__name__)

@app.route("/telemetry", methods=["POST"])
def telemetry():
    data = request.get_json(silent=True) or {}
    print("Recieved", data)
    return {"Status": "ok"}

if __name__=="__main__":
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    ctx=ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)

    ctx.verify_mode=ssl.CERT_REQUIRED

    ctx.load_cert_chain(
        os.path.join(base_dir, "certs", "server.crt"),
        os.path.join(base_dir,"certs","server.key")
    )

    ctx.load_verify_locations(os.path.join(base_dir, "certs", "rootCA.pem"))


    app.run(host="0.0.0.0", port=5001, ssl_context=ctx)