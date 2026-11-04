from app import create_app
from app.extensions import db
from app.models import Producto, Cliente, Pedido

app = create_app()

with app.app_context():
    if Producto.query.first():
        print("Ya existen datos. No se cargó nada.")
    else:
        productos = [
            Producto(nombre="Laptop Lenovo IdeaPad", precio=4500.00, stock=10),
            Producto(nombre="Mouse inalámbrico", precio=85.50, stock=50),
            Producto(nombre="Teclado mecánico", precio=320.00, stock=25),
            Producto(nombre="Monitor 24 pulgadas", precio=1200.00, stock=15),
            Producto(nombre="Disco SSD 500GB", precio=450.00, stock=30),
        ]
        clientes = [
            Cliente(nombre="Juan Pérez", telefono="70123456"),
            Cliente(nombre="María Gómez", telefono="71234567"),
            Cliente(nombre="Carlos Mamani", telefono="72345678"),
        ]
        db.session.add_all(productos + clientes)
        db.session.commit()

        pedidos = [
            (clientes[0], productos[0], 1),
            (clientes[1], productos[1], 2),
            (clientes[2], productos[3], 1),
            (clientes[0], productos[4], 2),
        ]
        for cli, prod, cant in pedidos:
            prod.stock -= cant
            db.session.add(Pedido(cliente_id=cli.id, producto_id=prod.id,
                                  monto=prod.precio * cant))
        db.session.commit()
        print("Datos de prueba cargados.")