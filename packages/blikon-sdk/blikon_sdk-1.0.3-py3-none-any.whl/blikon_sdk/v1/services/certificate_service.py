import os
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from datetime import datetime, timedelta

class CertificateService:
    def __init__(self):
        self.output_dir = 'certificates'
        os.makedirs(self.output_dir, exist_ok=True)  # Crear el directorio al inicio

    def generate_ca_certificate(self):
        try:
            ca_key = rsa.generate_private_key(
                public_exponent=65537,
                key_size=2048,
                backend=default_backend()
            )
            ca_subject = x509.Name([
                x509.NameAttribute(NameOID.COUNTRY_NAME, u"MX"),
                x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, u"Puebla"),
                x509.NameAttribute(NameOID.LOCALITY_NAME, u"Puebla"),
                x509.NameAttribute(NameOID.ORGANIZATION_NAME, u"Blikon"),
                x509.NameAttribute(NameOID.COMMON_NAME, u"blikon.com.blog"),
            ])

            ca_certificate = x509.CertificateBuilder().subject_name(
                ca_subject
            ).issuer_name(
                ca_subject
            ).public_key(
                ca_key.public_key()
            ).serial_number(
                x509.random_serial_number()
            ).not_valid_before(
                datetime.utcnow()
            ).not_valid_after(
                datetime.utcnow() + timedelta(days=3650)
            ).add_extension(
                x509.BasicConstraints(ca=True, path_length=None), critical=True
            ).sign(ca_key, hashes.SHA256(), default_backend())

            with open(os.path.join(self.output_dir, "ca.key"), "wb") as f:
                f.write(ca_key.private_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PrivateFormat.TraditionalOpenSSL,
                    encryption_algorithm=serialization.NoEncryption()
                ))

            with open(os.path.join(self.output_dir, "ca.pem"), "wb") as f:
                f.write(ca_certificate.public_bytes(serialization.Encoding.PEM))

            return ca_key, ca_certificate

        except Exception as e:
            print(f"An error occurred while generating CA certificate: {e}")
            raise

    def generate_server_certificate(self, ca_key, ca_cert):
        try:
            server_key = rsa.generate_private_key(
                public_exponent=65537,
                key_size=2048,
                backend=default_backend()
            )

            server_subject = x509.Name([
                x509.NameAttribute(NameOID.COUNTRY_NAME, u"MX"),
                x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, u"Puebla"),
                x509.NameAttribute(NameOID.LOCALITY_NAME, u"Puebla"),
                x509.NameAttribute(NameOID.ORGANIZATION_NAME, u"Blikon Python Server"),
                x509.NameAttribute(NameOID.COMMON_NAME, u"blikondev.com"),
            ])

            server_certificate = x509.CertificateBuilder().subject_name(
                server_subject
            ).issuer_name(
                ca_cert.subject
            ).public_key(
                server_key.public_key()
            ).serial_number(
                x509.random_serial_number()
            ).not_valid_before(
                datetime.utcnow()
            ).not_valid_after(
                datetime.utcnow() + timedelta(days=365)
            ).add_extension(
                x509.SubjectAlternativeName([x509.DNSName(u"miservidor.com")]),
                critical=False
            ).sign(ca_key, hashes.SHA256(), default_backend())

            with open(os.path.join(self.output_dir, "server.key"), "wb") as f:
                f.write(server_key.private_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PrivateFormat.TraditionalOpenSSL,
                    encryption_algorithm=serialization.NoEncryption()
                ))

            with open(os.path.join(self.output_dir, "server.crt"), "wb") as f:
                f.write(server_certificate.public_bytes(serialization.Encoding.PEM))

            return server_key, server_certificate

        except Exception as e:
            print(f"An error occurred while generating server certificate: {e}")
            raise

    def generate_client_certificate(self, ca_key, ca_cert):
        try:
            client_key = rsa.generate_private_key(
                public_exponent=65537,
                key_size=2048,
                backend=default_backend()
            )

            client_subject = x509.Name([
                x509.NameAttribute(NameOID.COUNTRY_NAME, u"MX"),
                x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, u"Puebla"),
                x509.NameAttribute(NameOID.LOCALITY_NAME, u"Puebla"),
                x509.NameAttribute(NameOID.ORGANIZATION_NAME, u"Blikon Python Client"),
                x509.NameAttribute(NameOID.COMMON_NAME, u"client.blkon.com"),
            ])

            client_certificate = x509.CertificateBuilder().subject_name(
                client_subject
            ).issuer_name(
                ca_cert.subject
            ).public_key(
                client_key.public_key()
            ).serial_number(
                x509.random_serial_number()
            ).not_valid_before(
                datetime.utcnow()
            ).not_valid_after(
                datetime.utcnow() + timedelta(days=365)
            ).sign(ca_key, hashes.SHA256(), default_backend())

            with open(os.path.join(self.output_dir, "client.key"), "wb") as f:
                f.write(client_key.private_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PrivateFormat.TraditionalOpenSSL,
                    encryption_algorithm=serialization.NoEncryption()
                ))

            with open(os.path.join(self.output_dir, "client.crt"), "wb") as f:
                f.write(client_certificate.public_bytes(serialization.Encoding.PEM))

            return client_key, client_certificate

        except Exception as e:
            print(f"An error occurred while generating client certificate: {e}")
            raise

    def generate_certificates(self):
        try:
            ca_key, ca_cert = self.generate_ca_certificate()
            server_key, server_cert = self.generate_server_certificate(ca_key, ca_cert)
            client_key, client_cert = self.generate_client_certificate(ca_key, ca_cert)
            self.save_and_print_certificates(ca_key, ca_cert, server_key, server_cert, client_key, client_cert)
        except Exception as e:
            print(f"An error occurred while generating certificates: {e}")

    def save_and_print_certificates(self, ca_key, ca_cert, server_key, server_cert, client_key, client_cert):
        try:
            ca_key_pem = ca_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption()
            )
            print("CA Private Key:\n", ca_key_pem.decode())
            # El archivo ya se guarda en certificates al generar el CA

            ca_cert_pem = ca_cert.public_bytes(serialization.Encoding.PEM)
            print("CA Certificate:\n", ca_cert_pem.decode())
            # El archivo ya se guarda en certificates al generar el CA

            server_key_pem = server_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption()
            )
            print("Server Private Key:\n", server_key_pem.decode())
            # El archivo ya se guarda en certificates al generar el servidor

            server_cert_pem = server_cert.public_bytes(serialization.Encoding.PEM)
            print("Server Certificate:\n", server_cert_pem.decode())
            # El archivo ya se guarda en certificates al generar el servidor

            client_key_pem = client_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption()
            )
            print("Client Private Key:\n", client_key_pem.decode())
            # El archivo ya se guarda en certificates al generar el cliente

            client_cert_pem = client_cert.public_bytes(serialization.Encoding.PEM)
            print("Client Certificate:\n", client_cert_pem.decode())
            # El archivo ya se guarda en certificates al generar el cliente

        except Exception as e:
            print(f"An error occurred while saving and printing certificates: {e}")
            raise
