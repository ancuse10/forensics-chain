import datetime
import sys
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.hashes import SHA256
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.serialization import pkcs12
from getpass import getpass

def validate():
	# Cargar el archivo de certificado PFX
	ruta_cert = input("Introduce the path to the certificate: ")

	try:
		with open(f"{ruta_cert}", "rb") as f:
			pfx_data = f.read()
	except:
		print("Error obtaining certificate")
		sys.exit()

	# Descifrar el archivo PFX para obtener el certificado y la clave privada
	contrasena_cert = getpass("Introduce the certificate's password: ")
	password = f"{contrasena_cert}".encode()
	try:
		pfx = pkcs12.load_key_and_certificates(pfx_data, password, default_backend())
	except:
		print("Password error\n")
		sys.exit()
	# Obtener el certificado del archivo PFX
	cert = pfx[1]

	comprueba_cert = pfx[2][0]

	# Verificar la validez del certificado
	if cert.not_valid_after < datetime.datetime.now(cert.not_valid_after.tzinfo):
		print("\nCertificate expired")
		sys.exit()
	else:
		print("\nValid certificate")

	# Verificar la firma del certificado
	try:
		comprueba_cert.public_key().verify(comprueba_cert.signature,
                comprueba_cert.tbs_certificate_bytes,
                padding.PKCS1v15(),comprueba_cert.signature_hash_algorithm)
		print("\nCertificate's signature is valid\n")
	except:
		print("\nCertificate's signature is not valid")
		sys.exit()

	cert_id = cert.serial_number

	cert_public = pfx[2][0].public_key().public_bytes(encoding=serialization.Encoding.DER, format=serialization.PublicFormat.SubjectPublicKeyInfo)

	# Obtener el nombre del propietario del certificado
	subject = cert.subject
	name = subject.rfc4514_string()

	return cert_id, cert_public, name
