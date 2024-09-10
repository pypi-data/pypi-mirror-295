from .exceptions import ServiceException
from threading import Thread

import re

class BaseService:
    modelo = None
    objeto = None

    create_fields = []
    update_fields = []
    serialize_fields = []
    foreign_fields = []
    unique_fields = []
    filter_fields = []

    def __init__(self, id=None):
        if id is not None:
            self.set_objeto(id)
            
    def set_objeto(self, id):
        try:
            self.objeto = self.modelo.objects.get(id=id)

        except self.modelo.DoesNotExist:
            raise ServiceException(f"El {self.modelo.__name__} con id '{id}' no existe.")
            
    def asincrono(self, funcion, *args):
        thread = Thread(target=funcion, args=args)
        thread.start()

    def check_objeto(self):
        if self.objeto is None:
            raise ServiceException(f"El {self.modelo.MODELO_SINGULAR.lower()} no ha sido definido.")

    def is_campo_image(self, campo):
        tipo = self.modelo._meta.get_field(campo).get_internal_type()
        return tipo == 'ImageField' or tipo == 'FileField'

    def get_valor_by_campo(self, campo):
        valor = None

        if campo in list(map(lambda x: x['campo'], self.foreign_fields)):
            foreign_field = list(filter(lambda x: x['campo'] == campo, self.foreign_fields))[0]

            service = BaseService()
            service.modelo = getattr(self.objeto, campo)._meta.model
            service.objeto = getattr(self.objeto, campo)
            service.serialize_fields = foreign_field['serialize_fields']

            service.objeto = getattr(self.objeto, campo)
            valor = service.get_serializado()

        elif self.is_campo_image(campo):
            valor = getattr(self.objeto, campo).url

        else:
            valor = getattr(self.objeto, campo)

        return valor

    def get_serializado(self):
        self.check_objeto()

        data = {}

        for campo in self.serialize_fields:
            valor = self.get_valor_by_campo(campo)
            data[campo] = valor

        return data
    
    def get_filtro_by_campo(self, campo, valor):
        valor = valor.lower()

        if campo in self.foreign_fields:
            campo = campo + '_id'

        filtro_icontains = f'{campo}__icontains'

        return {filtro_icontains: valor}

    def listar(self, **kwargs):
        data = []

        filtros = {}

        for campo, valor in kwargs.items():
            if campo not in self.filter_fields:
                raise ServiceException(f"El campo '{campo}' no es un campo válido para filtrar.")
            
            filtro = self.get_filtro_by_campo(campo, valor)
            filtros.update(filtro)
       
        objetos = self.modelo.objects.filter(**filtros)

        for objeto in objetos:
            service = self.__class__()
            service.objeto = objeto

            data.append(service.get_serializado())

        return data
    
                    
    def validar_unicidad(self, campo, valor):
        if campo in self.unique_fields:
            if self.modelo.objects.filter(**{campo: valor}).exists():
                raise ServiceException(f"El campo '{campo}' con valor '{valor}' ya existe.")
            

    def crear(self, **kwargs):
        objeto = self.modelo()

        for campo in self.create_fields:
            if campo not in kwargs:
                raise ServiceException(f"El campo '{campo}' es requerido para crear.")
            
            valor = kwargs[campo]
            
            self.validar_unicidad(campo, valor)

            if campo in self.foreign_fields:
                campo = campo + '_id'

            setattr(objeto, campo, valor)

        objeto.save()
        self.objeto = objeto


    def actualizar(self, **kwargs):
        self.check_objeto()

        for campo, valor in kwargs.items():
            if campo not in self.update_fields:
                raise ServiceException(f"El campo '{campo}' no es un campo válido para actualizar.")
            
            self.validar_unicidad(campo, valor)
            setattr(self.objeto, campo, valor)

        self.objeto.save()

    def eliminar(self):
        self.check_objeto()

        self.objeto.delete()
        self.objeto = None

        