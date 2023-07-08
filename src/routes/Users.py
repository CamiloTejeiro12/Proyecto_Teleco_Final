from flask import Blueprint, jsonify,request

from models.UsersModel import UsersModel
from models.entities.Users import Users

main = Blueprint('users_blueprint', __name__)

from utils.encriptar import cifrar_mensaje,generar_clave,comparar_contrasenas,cifrar_contrasena

@main.route('/')
def get_users():
    try:
        users = UsersModel.get_users()
        return jsonify(users)
    except Exception as e:
        return jsonify({'message':str(e)}),500
    
@main.route('/<cedula>')
def get_user(cedula):
    try:
        user = UsersModel.get_user(cedula)
        if user != None:
            return jsonify(user)
        else:
            return jsonify({'message':'No existe usuario con esa cedula'}),404
    except Exception as e:
        return jsonify({'message':str(e)}),500
    
@main.route('/add', methods=['POST'])
def add_user():
    try:
        cedula = request.json['data']['cedula']
        nombres = request.json['data']['nombres']
        apellidos = request.json['data']['apellidos']
        correo = request.json['data']['correo']
        telefono = request.json['data']['telefono']
        texto = request.json['data']['texto']
        clave = request.json['data']['clave']
        rol = request.json['data']['rol']

        user_cedula = request.json['user']['cedula']
        user_clave = request.json['user']['clave']

        clave_c = generar_clave(clave)
        texto = cifrar_mensaje(texto,clave_c)
        
        user = Users(cedula,nombres,apellidos,correo,telefono,texto,clave,rol)

        affected_rows = UsersModel.add_user(user,user_cedula,user_clave)
        
        if affected_rows == 1:
            message = "Usuario agregado! " + user.cedula
            return jsonify({"message": message})
        elif not affected_rows:
            return jsonify({"message": "Error al validar credenciales"}), 403
        else:
            return jsonify({'message': "Error al agregar"}), 500

    except Exception as ex:
        return jsonify({'message': str(ex)}), 500
    
@main.route('/delete', methods=['DELETE'])
def delete_user():
    try:
        cedula = request.json['user']['cedula']
        clave = request.json['user']['clave']
        cedula_borrar = request.json['data']['cedula']


        affected_rows = UsersModel.deleter_user(cedula,clave,cedula_borrar)

        if affected_rows == 1:
            message = "Usuario con cedula " + cedula + " eliminado"
            return jsonify({"message": message})
        elif not affected_rows:
            return jsonify({"message": "Error al validar credenciales"}), 403
        else:
            return jsonify({'message': "Error al eliminar"}), 500

    except Exception as ex:
        return jsonify({'message': str(ex)}), 500

@main.route('/text', methods=['GET'])
def get_text():
    try:
        cedula = request.json['cedula']
        clave = request.json['clave']

        message = UsersModel.get_text(cedula,clave)

        if message != None:
            return jsonify(message)
        else:
            return jsonify({'message': "Error al desencriptar mensaje"}), 500

    except Exception as ex:
        return jsonify({'message': str(ex)}), 500
    
@main.route('/edit/clave', methods=['PUT'])
def edit_pass():
    try:
        cedula = request.json['cedula']
        clave = request.json['clave']
        nueva_clave = request.json['nueva_clave']

        message = UsersModel.edit_pass(cedula,clave,nueva_clave)

        if message != None:
            return jsonify(message)
        else:
            return jsonify({'message': "Error al verificar los datos suministrados"}), 500

    except Exception as ex:
        return jsonify({'message': str(ex)}), 500
    
@main.route('/edit/texto', methods=['PUT'])
def edit_text():
    try:
        cedula = request.json['cedula']
        texto = request.json['texto']
        clave = request.json['clave']

        message = UsersModel.edit_text(cedula,texto,clave)

        if message != None:
            return jsonify(message)
        else:
            return jsonify({'message': "Error al editar texto, verifique los datos suministrados"}), 500

    except Exception as ex:
        return jsonify({'message': str(ex)}), 500
    
@main.route('/edit/telefono', methods=['PUT'])
def edit_telephone():
    try:
        
        cedula = request.json['user']['cedula']
        clave = request.json['user']['clave']
        cedula_editar = request.json['data']['cedula']
        telefono = request.json['data']['telefono']


        message = UsersModel.edit_telephone(cedula,telefono,clave,cedula_editar)

        if message != False:
            return jsonify(message)
        elif not message:
            return jsonify({"message": "Error al validar credenciales"}), 403
        else:
            return jsonify({'message': "Error al editar telefono"}), 500

    except Exception as ex:
        return jsonify({'message': str(ex)}), 500
    
@main.route('/edit/correo', methods=['PUT'])
def edit_email():
    try:
        cedula = request.json['user']['cedula']
        clave = request.json['user']['clave']
        cedula_editar = request.json['data']['cedula']
        correo = request.json['data']['correo']

        message = UsersModel.edit_email(cedula,correo,clave,cedula_editar)

        if message != False:
            return jsonify(message)
        elif not message:
            return jsonify({"message": "Error al validar credenciales"}), 403
        else:
            return jsonify({'message': "Error al editar correo"}), 500
        

    except Exception as ex:
        return jsonify({'message': str(ex)}), 500

@main.route('/edit/nombres', methods=['PUT'])
def edit_names():
    try:
        cedula = request.json['user']['cedula']
        clave = request.json['user']['clave']
        cedula_editar = request.json['data']['cedula']
        nombres = request.json['data']['nombres']

        message = UsersModel.edit_nombres(cedula,nombres,clave,cedula_editar)

        if message != False:
            return jsonify(message)
        elif not message:
            return jsonify({"message": "Error al validar credenciales"}), 403
        else:
            return jsonify({'message': "Error al editar nombres"}), 500
        

    except Exception as ex:
        return jsonify({'message': str(ex)}), 500
    
@main.route('/edit/apellidos', methods=['PUT'])
def edit_apellidos():
    try:
        cedula = request.json['user']['cedula']
        clave = request.json['user']['clave']
        cedula_editar = request.json['data']['cedula']
        apellidos = request.json['data']['apellidos']

        message = UsersModel.edit_nombres(cedula,apellidos,clave,cedula_editar)

        if message != False:
            return jsonify(message)
        elif not message:
            return jsonify({"message": "Error al validar credenciales"}), 403
        else:
            return jsonify({'message': "Error al editar apellidos"}), 500
        

    except Exception as ex:
        return jsonify({'message': str(ex)}), 500
    