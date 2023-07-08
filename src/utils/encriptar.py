from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
import hashlib
import hmac

def generar_clave(clave_personalizada):
    clave_personalizada = clave_personalizada.encode()
    clave = clave_personalizada.ljust(32, b'\0')[:32]
    return clave

def cifrar_mensaje(mensaje, clave):
    backend = default_backend()
    iv = b"0123456789abcdef" 
    cifrador = Cipher(algorithms.AES(clave), modes.CBC(iv), backend=backend).encryptor()
    padder = padding.PKCS7(128).padder()
    mensaje_pad = padder.update(mensaje.encode()) + padder.finalize()
    mensaje_cifrado = cifrador.update(mensaje_pad) + cifrador.finalize()
    return mensaje_cifrado

def descifrar_mensaje(mensaje_cifrado, clave):
    try:
        backend = default_backend()
        iv = b"0123456789abcdef"
        descifrador = Cipher(algorithms.AES(clave), modes.CBC(iv), backend=backend).decryptor()
        mensaje_pad = descifrador.update(mensaje_cifrado) + descifrador.finalize()
        unpadder = padding.PKCS7(128).unpadder()
        mensaje_descifrado = unpadder.update(mensaje_pad) + unpadder.finalize()
        return mensaje_descifrado.decode()
    except Exception as e:
        print("Error al desencriptar")
        return None

def cifrar_contrasena(contrasena):
    # Cifra la contraseña en SHA256
    cifrado = hashlib.sha256(contrasena.encode()).hexdigest()
    return cifrado

def comparar_contrasenas(contrasena_ingresada, contrasena_guardada):
    # Cifra la contraseña ingresada en SHA256
    contrasena_cifrada = cifrar_contrasena(contrasena_ingresada)
    
    # Compara las contraseñas cifradas de manera segura
    return hmac.compare_digest(contrasena_cifrada, contrasena_guardada)


# Obtener el mensaje y la clave personalizada del usuario
# mensaje = input("Ingrese el mensaje: ")
# clave_personalizada = input("Ingrese la clave personalizada: ")

# # Generar una clave a partir de la clave personalizada
# clave = generar_clave(clave_personalizada)

# # Encriptar el mensaje
# mensaje_cifrado = cifrar_mensaje(mensaje, clave)
# print("Mensaje cifrado:", mensaje_cifrado)

# # Solicitar la clave nuevamente al usuario para descifrar el mensaje
# clave_descifrar = input("Ingrese la clave para descifrar el mensaje: ")

# # Generar la clave para descifrar el mensaje
# clave_descifrar = generar_clave(clave_descifrar)

# # Descifrar el mensaje
# mensaje_descifrado = descifrar_mensaje(mensaje_cifrado, clave_descifrar)
# print("Mensaje descifrado:", mensaje_descifrado)

# texto = "\\x0f75d16542fe209df66105cc42d6b405"
# bytes_texto = bytes.fromhex(texto[2:])
# clave_descifrar = generar_clave("aaaa")

# # Descifrar el mensaje
# mensaje_descifrado = descifrar_mensaje(bytes_texto, clave_descifrar)
# print("Mensaje descifrado:", mensaje_descifrado)

