class Carrito:
    def __init__(self, request):
        self.request = request
        self.session = request.session
        carrito = self.session.get("carrito")
        if not carrito:
            self.session["carrito"] = {}
            self.carrito = self.session["carrito"]
        else:
            self.carrito = carrito

    def agregar(self, producto):
        id = str(producto.id)
        if id not in self.carrito.keys():
<<<<<<< Updated upstream
            self.carrito[id]={
                 "producto_id":producto.id,
                 "nombre": producto.titulo,
                 "precio total": producto.precio,
                 "cantidad": 1,
=======
            self.carrito[id] = {
                "producto_id": producto.id,
                "nombre": producto.titulo,  # Cambiar a "titulo" si ese es el campo correcto
                "precio total": producto.precio,  # Cambiar a "precio" si ese es el campo correcto
                "cantidad": 1,
>>>>>>> Stashed changes
            }
        else:
            self.carrito[id]["cantidad"] += 1
            self.carrito[id]["precio total"] += producto.precio
        self.guardar_carrito()

    def guardar_carrito(self):
        self.session["carrito"] = self.carrito
        self.session.modified = True

    def eliminar(self, producto):
        id = str(producto.id)
        if id in self.carrito:
            del self.carrito[id]
            self.guardar_carrito()

<<<<<<< Updated upstream
    def restar(self, producto):
=======
    def restar(self, producto):  # Cambiar "resar" a "restar"
>>>>>>> Stashed changes
        id = str(producto.id)
        if id in self.carrito.keys():
            self.carrito[id]["cantidad"] -= 1
            self.carrito[id]["precio total"] -= producto.precio
            if self.carrito[id]["cantidad"] <= 0:
                self.eliminar(producto)
            self.guardar_carrito()

    def limpiar(self):
        self.session["carrito"] = {}
        self.session.modified = True
