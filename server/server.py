from flask import Flask, request
import ssl

app = Flask(__name__)

@app.route("/telemetry", methods=["POST"])
def telemetry():
    data = request.get_json(silent=True) or {}
    print("Recieved", data)
    return {"Status": "ok"}

if __name__=="__main__":
    
    ctx=ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)

    ctx.verify_mode=ssl.CERT_REQUIRED

    ctx.load_cert_chain("../certs/server.crt", "../certs/server.key")

    ctx.load_verify_locations("../certs/rootCA.pem")


    app.run(host="0.0.0.0", port=5001, ssl_context=ctx)