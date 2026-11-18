#!/usr/bin/env python3
"""Client HTTPS de test : valide l'authentification du serveur, puis recupere la page."""
import socket, ssl, sys

host = sys.argv[1]
port = int(sys.argv[2]) if len(sys.argv) > 2 else 443

# contexte par defaut = verification complete : chaine de certification + nom d'hote
ctx = ssl.create_default_context()

try:
    with socket.create_connection((host, port), timeout=5) as sock:
        with ctx.wrap_socket(sock, server_hostname=host) as tls:
            cert = tls.getpeercert()
            print("handshake OK :", tls.version(), tls.cipher()[0])
            print("sujet      :", dict(x[0] for x in cert["subject"]))
            print("emetteur   :", dict(x[0] for x in cert["issuer"]))
            print("validite   :", cert["notBefore"], "->", cert["notAfter"])
            print("SAN        :", cert.get("subjectAltName"))
            tls.sendall(b"GET / HTTP/1.0\r\nHost: " + host.encode() + b"\r\n\r\n")
            data = b""
            while True:
                chunk = tls.recv(4096)
                if not chunk:
                    break
                data += chunk
except ssl.SSLCertVerificationError as e:
    print("ECHEC de la verification :", e.verify_message)
    sys.exit(1)

print("--- reponse ---")
print(data.decode(errors="replace").split("\r\n\r\n", 1)[-1].strip())
