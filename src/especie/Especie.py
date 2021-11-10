class Especie:
    def __init__(self, id: int, nombre_especie: str, id_tipo_1: int):
        self.id = id
        self.nombre_especie = nombre_especie
        self.id_tipo_1 = id_tipo_1
        self.id_tipo_2 = None
        self.nombre_tipo_1 = None
        self.nombre_tipo_2 = None

    def __str__(self):
        if self.nombre_tipo_2 == '':
            return 'Nombre: %s\nTipo Primario: %s\nTipo Secundario: NN' \
                % (self.nombre_especie, self.nombre_tipo_1)
        return 'Nombre: %s\nTipo Primario: %s\nTipo Secundario: %s' \
            % (self.nombre_especie, self.nombre_tipo_1, self.nombre_tipo_2)