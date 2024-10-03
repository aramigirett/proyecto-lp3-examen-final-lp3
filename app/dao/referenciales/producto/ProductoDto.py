class ProductoDto:

    def __init__(self, id_producto, nombre, cantidad, precio_unitario):
        self.__id_producto = id_producto
        self.__nombre = nombre
        self.__cantidad = cantidad
        self.__precio_unitario = precio_unitario

    #getters y setters de id_producto
    @property
    def id_producto(self):
        return self.id_producto
    
    @id_producto.setter
    def id_producto(self, valor):
        if not valor:
            raise("El atributo id_producto no puede estar vacio")
        self.__id_producto = valor

    #getters y setters de nombre
    @property
    def nombre(self):
        return self.__nombre
    
    @nombre.setter
    def nombre(self, valor):
        if not valor:
            raise("El atributo nombre no puede estar vacio")
        self.__nombre = valor.upper()

     #getters y setters de cantidad
     
