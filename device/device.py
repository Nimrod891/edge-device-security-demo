import requests

URL = "https://localhost://5001/telemetry"

payload = {"temperature":27.8, "status":"OK"}

DEVICE_CERT = "../certs/device.crt"
DEVICE_KEY="../certs/device.key"
ROOT_CA="../certs/rootCA.pem"

def main():
    resp = requests.post(
        URL,
        json=payload,
        cert=(DEVICE_CERT,DEVICE_KEY),
        verify=ROOT_CA,
        timeout=5,

    )

    print("Status:", resp.status_code)
    print("Body:",resp.text)

if __name__ == "__main__":
    main()