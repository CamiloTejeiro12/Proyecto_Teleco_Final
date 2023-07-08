from database.db import get_connection
from .entities.Users import Users
from utils.encriptar import descifrar_mensaje,generar_clave,cifrar_mensaje,cifrar_contrasena,comparar_contrasenas
from utils.correos import enviar


class UsersModel():
    @classmethod
    def login(self,cedula,contrasena):
        try:
            connection = get_connection()

            with connection.cursor() as cursor:
                cursor.execute("SELECT clave FROM Users WHERE cedula = %s",(cedula,))
                row = cursor.fetchone()
            
                user = None
                if row != None:
                    contrasena_guardada = row[0]

                    user = comparar_contrasenas(contrasena, contrasena_guardada)
            connection.close()
            return user
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def get_users(self):
        try:
            connection = get_connection()
            users = []

            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM Users")
                resultset = cursor.fetchall()

                for row in resultset:
                    user = Users(row[0], row[1], row[2], row[3],row[4],row[5],row[6],row[7])
                    users.append(user.to_JSON())

            connection.close()
            return users
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def get_user(self,cedula):
        try:
            connection = get_connection()

            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM Users WHERE cedula = %s",(cedula,))
                row = cursor.fetchone()

                user = False
                if row != None:
                    user = Users(row[0], row[1], row[2], row[3],row[4],row[5],row[6],row[7])
                    user = user.to_JSON()
    
            connection.close()
            return user
        except Exception as ex:
            raise Exception(ex)
    
    @classmethod
    def get_rol(self,cedula):
        try:
            connection = get_connection()

            with connection.cursor() as cursor:
                cursor.execute("SELECT rol FROM Users WHERE cedula = %s",(cedula,))
                row = cursor.fetchone()

                rol = (row[0] == 'admin' and row != None)

            connection.close()
            return rol
        except Exception as ex:
            raise Exception(ex)
    
    @classmethod
    def add_user(self,user,cedula,u_clave):
        if not self.login(cedula,u_clave):
            return False
        if not self.get_rol(cedula):
            return False
        
        try:
            connection = get_connection()

            clave = cifrar_contrasena(user.clave)
            with connection.cursor() as cursor:
                cursor.execute("""INSERT INTO Users VALUES (%s, %s, %s, %s, %s, %s, %s,%s)""",
                                (user.cedula, user.nombres, user.apellidos, user.correo,user.telefono,user.texto, clave,user.rol))
                affected_rows = cursor.rowcount

            

                connection.commit()
    
            connection.close()
            return affected_rows
        
        except Exception as ex:
            raise Exception(ex)
        
    @classmethod
    def deleter_user(self,cedula,u_clave,cedula_borrar):
        if not self.login(cedula,u_clave):
            return False
        if not self.get_rol(cedula):
            if cedula_borrar != cedula:
                return False
            
        
        try:
            connection = get_connection()

            with connection.cursor() as cursor:
                cursor.execute("""DELETE FROM Users WHERE cedula=%s""",
                                (cedula_borrar,))
                affected_rows = cursor.rowcount
                connection.commit()
    
            connection.close()
            return affected_rows
        
        except Exception as ex:
            raise Exception(ex)
        
    @classmethod
    def get_text(self,cedula,clave):
        try:
            connection = get_connection()

            with connection.cursor() as cursor:
                cursor.execute("SELECT cedula,texto FROM Users WHERE cedula = %s",(cedula,))
                row = cursor.fetchone()

                user = None
                if row != None:
                    
                    user = {
                        'cedula':row[0],
                        'texto':row[1]
                    }

            clave_n = generar_clave(clave)
            texto = user['texto']
            bytes_texto = bytes.fromhex(texto[2:])
            user['texto'] = descifrar_mensaje(bytes_texto,clave_n)
            connection.close()
            if user['texto'] == None:
                return None
            return user
        except Exception as ex:
            raise Exception(ex)
    
    @classmethod
    def edit_pass(self,cedula,clave,clave_nueva):
        try:
            connection = get_connection()

            with connection.cursor() as cursor:
                cursor.execute("SELECT cedula,texto,correo FROM Users WHERE cedula = %s",(cedula,))
                row = cursor.fetchone()

                user = None
                if row != None:
                    
                    user = {
                        'cedula':row[0],
                        'texto':row[1],
                        'correo':row[2]
                    }

                clave_n = generar_clave(clave)
                texto = user['texto']
                bytes_texto = bytes.fromhex(texto[2:])
                user['texto'] = descifrar_mensaje(bytes_texto,clave_n)
                if user['texto'] == None:
                    return None
                
                clave = generar_clave(clave_nueva)
                texto = cifrar_mensaje(user['texto'],clave)

                cursor.execute("""UPDATE Users SET texto = %s 
                                    WHERE cedula = %s""", (texto,cedula))
                
                enviar(user['correo'],clave_nueva)
                connection.commit()
            connection.close()
            return "Clave editada correctamente"
        except Exception as ex:
            raise Exception(ex)
    
    @classmethod
    def edit_text(self,cedula,texto,clave):
        try:
            connection = get_connection()

            with connection.cursor() as cursor:
                cursor.execute("SELECT cedula,texto FROM Users WHERE cedula = %s",(cedula,))
                row = cursor.fetchone()

                user = None
                if row != None:
                    
                    user = {
                        'cedula':row[0],
                        'texto':row[1],
                    }

                clave_n = generar_clave(clave)
                texto_n = user['texto']
                bytes_texto = bytes.fromhex(texto_n[2:])
                user['texto'] = descifrar_mensaje(bytes_texto,clave_n)
                if user['texto'] == None:
                    return None
                
                texto = cifrar_mensaje(texto,clave_n)

                cursor.execute("""UPDATE Users SET texto = %s 
                                    WHERE cedula = %s""", (texto,cedula))
                
                
                connection.commit()
            connection.close()
            return "Texto editado correctamente"
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def edit_telephone(self,cedula,telefono,u_clave,cedula_editar):
        if not self.login(cedula,u_clave):
            return False
        if not self.get_rol(cedula):
            if cedula_editar != cedula:
                return False

        try:
            connection = get_connection()

            with connection.cursor() as cursor:
                cursor.execute("""UPDATE Users SET telefono = %s 
                                    WHERE cedula = %s""", (telefono,cedula_editar))
                
                connection.commit()
            connection.close()
            return "Telefono editado correctamente"
        except Exception as ex:
            return False
        
    @classmethod
    def edit_email(self,cedula,correo,u_clave,cedula_editar):
        if not self.login(cedula,u_clave):
            return False
        if not self.get_rol(cedula):
            if cedula_editar != cedula:
                return False
        try:
            connection = get_connection()

            with connection.cursor() as cursor:
                cursor.execute("""UPDATE Users SET correo = %s 
                                    WHERE cedula = %s""", (correo,cedula_editar))
                
                connection.commit()
            connection.close()
            return "Correo editado correctamente"
        except Exception as ex:
            raise False
        
    @classmethod
    def edit_nombres(self,cedula,nombres,u_clave,cedula_editar):
        if not self.login(cedula,u_clave):
            return False
        if not self.get_rol(cedula):
            if cedula_editar != cedula:
                return False
        try:
            connection = get_connection()

            with connection.cursor() as cursor:
                cursor.execute("""UPDATE Users SET nombres = %s 
                                    WHERE cedula = %s""", (nombres,cedula_editar))
                
                connection.commit()
            connection.close()
            return "Nombres editados correctamente"
        except Exception as ex:
            raise False
    
    @classmethod
    def edit_apellidos(self,cedula,apellidos,u_clave,cedula_editar):
        if not self.login(cedula,u_clave):
            return False
        if not self.get_rol(cedula):
            if cedula_editar != cedula:
                return False
        try:
            connection = get_connection()

            with connection.cursor() as cursor:
                cursor.execute("""UPDATE Users SET apellidos = %s 
                                    WHERE cedula = %s""", (apellidos,cedula_editar))
                
                connection.commit()
            connection.close()
            return "Apellidos editados correctamente"
        except Exception as ex:
            raise False