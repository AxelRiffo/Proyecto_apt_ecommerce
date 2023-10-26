def total_carrito(request):
    total = 0
    cantidad_productos = 0  # Variable para almacenar la cantidad de productos
    if request.user.is_authenticated:
        if "carrito" in request.session.keys():
            for key, value in request.session["carrito"].items():
                total += int(value["acumulado"])
                cantidad_productos += int(value["cantidad"])  # Suma la cantidad de productos
    return {"total_carrito": total, "cantidad_productos": cantidad_productos}
