from flask import render_template, request, redirect, url_for, flash
from . import bp_pedidos
from ..extensions import db
from ..models import Pedido, Cliente, Producto


def _form(pedido):
    return render_template(
        "pedidos/form.html",
        pedido=pedido,
        clientes=Cliente.query.order_by(Cliente.nombre).all(),
        productos=Producto.query.order_by(Producto.nombre).all(),
    )


@bp_pedidos.route("/")
def listar():
    pedidos = Pedido.query.order_by(Pedido.fecha.desc()).all()
    return render_template("pedidos/lista.html", pedidos=pedidos)


@bp_pedidos.route("/nuevo", methods=["GET", "POST"])
def nuevo():
    if request.method == "POST":
        cliente_id = request.form.get("cliente_id", type=int)
        producto_id = request.form.get("producto_id", type=int)
        cantidad = request.form.get("cantidad", default=1, type=int)
        producto = db.session.get(Producto, producto_id) if producto_id else None
        if not cliente_id or not producto or cantidad < 1:
            flash("Completa todos los campos correctamente.", "danger")
        elif producto.stock < cantidad:
            flash(f"Stock insuficiente. Disponible: {producto.stock}.", "warning")
        else:
            producto.stock -= cantidad
            db.session.add(Pedido(
                cliente_id=cliente_id,
                producto_id=producto_id,
                monto=producto.precio * cantidad,
            ))
            db.session.commit()
            flash("Pedido registrado.", "success")
            return redirect(url_for("pedidos.listar"))
    return _form(None)


@bp_pedidos.route("/<int:id>/editar", methods=["GET", "POST"])
def editar(id):
    p = db.get_or_404(Pedido, id)
    if request.method == "POST":
        cliente_id = request.form.get("cliente_id", type=int)
        producto_id = request.form.get("producto_id", type=int)
        monto = request.form.get("monto", type=float)
        if not (cliente_id and producto_id and monto is not None):
            flash("Completa todos los campos.", "danger")
        else:
            p.cliente_id, p.producto_id, p.monto = cliente_id, producto_id, monto
            db.session.commit()
            flash("Pedido actualizado.", "success")
            return redirect(url_for("pedidos.listar"))
    return _form(p)


@bp_pedidos.route("/<int:id>/eliminar", methods=["POST"])
def eliminar(id):
    p = db.get_or_404(Pedido, id)
    db.session.delete(p)
    db.session.commit()
    flash("Pedido eliminado.", "success")
    return redirect(url_for("pedidos.listar"))