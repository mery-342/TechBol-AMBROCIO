from flask import render_template, request, redirect, url_for, flash
from . import bp_productos
from ..extensions import db
from ..models import Producto


def _guardar(p):
    nombre = request.form.get("nombre", "").strip()
    precio = request.form.get("precio", type=float)
    stock = request.form.get("stock", type=int)
    if not nombre or precio is None or stock is None or precio < 0 or stock < 0:
        flash("Completa todos los campos con valores válidos.", "danger")
        return False
    p.nombre, p.precio, p.stock = nombre, precio, stock
    return True


@bp_productos.route("/")
def listar():
    productos = Producto.query.order_by(Producto.nombre).all()
    return render_template("productos/lista.html", productos=productos)


@bp_productos.route("/nuevo", methods=["GET", "POST"])
def nuevo():
    if request.method == "POST":
        p = Producto()
        if _guardar(p):
            db.session.add(p)
            db.session.commit()
            flash("Producto registrado.", "success")
            return redirect(url_for("productos.listar"))
    return render_template("productos/form.html", producto=None)


@bp_productos.route("/<int:id>/editar", methods=["GET", "POST"])
def editar(id):
    p = db.get_or_404(Producto, id)
    if request.method == "POST":
        if _guardar(p):
            db.session.commit()
            flash("Producto actualizado.", "success")
            return redirect(url_for("productos.listar"))
    return render_template("productos/form.html", producto=p)


@bp_productos.route("/<int:id>/eliminar", methods=["POST"])
def eliminar(id):
    p = db.get_or_404(Producto, id)
    if p.pedidos:
        flash("No se puede eliminar: el producto tiene pedidos.", "warning")
    else:
        db.session.delete(p)
        db.session.commit()
        flash("Producto eliminado.", "success")
    return redirect(url_for("productos.listar"))