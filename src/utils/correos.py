import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def enviar(autor,clave):
    try:
        # Configuración del servidor SMTP y credenciales
        smtp_host = 'smtp.gmail.com'
        smtp_port = 587
        smtp_username = 'uno.sobre.turip@gmail.com'
        smtp_password = 'ejfcbtcutxpnmegy'

        # Crear objeto de mensaje
        mensaje = MIMEMultipart()
        mensaje['From'] = 'Remitente'
        mensaje['To'] = autor
        mensaje['Subject'] = 'Cambio de clave'

        # Cuerpo del correo
        cuerpo = 'La clave ha sido modificada correctamente.\n Nueva clave: '+ str(clave)
        mensaje.attach(MIMEText(cuerpo, 'plain'))

        # Iniciar conexión SMTP y enviar correo
        with smtplib.SMTP(smtp_host, smtp_port) as servidor:
            servidor.starttls()
            servidor.login(smtp_username, smtp_password)
            servidor.send_message(mensaje)

        print('Correo enviado exitosamente.')
    except Exception as e:
        print(str(e))
        return None