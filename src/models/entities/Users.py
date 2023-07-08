class Users():
    def __init__(self,cedula,nombres,apellidos,correo,telefono,texto,clave,rol):
        self.cedula=cedula
        self.nombres=nombres
        self.apellidos=apellidos
        self.correo=correo
        self.telefono=telefono
        self.texto=texto
        self.clave=clave
        self.rol=rol

    def to_JSON(self):
        return {
            'nombres':self.nombres,
            'apellidos':self.apellidos,
            'telefono':self.telefono,
            'correo':self.correo,
            'cedula':self.cedula,
            'texto':self.texto
        }