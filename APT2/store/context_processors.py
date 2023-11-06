def total_carrito(request):
    total = 0
    cantidad_productos = 0
    if request.user.is_authenticated:
        if "carrito" in request.session.keys():
            for key, value in request.session["carrito"].items():
                total += int(value["acumulado"])
                cantidad_productos += int(value["cantidad"])
    return {"total_carrito": total, "cantidad_productos": cantidad_productos}
