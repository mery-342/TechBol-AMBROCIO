from flask import render_template, request, redirect, url_for, flash
from . import bp_clientes
from ..extensions import db
from ..models import Cliente


@bp_clientes.route("/")
def listar():
    clientes = Cliente.query.order_by(Cliente.nombre).all()
    return render_template("clientes/lista.html", clientes=clientes)


@bp_clientes.route("/nuevo", methods=["GET", "POST"])
def nuevo():
    if request.method == "POST":
        nombre = request.form.get("nombre", "").strip()
        telefono = request.form.get("telefono", "").strip()
        if not nombre:
            flash("El nombre es obligatorio.", "danger")
        else:
            db.session.add(Cliente(nombre=nombre, telefono=telefono))
            db.session.commit()
            flash("Cliente registrado.", "success")
            return redirect(url_for("clientes.listar"))
    return render_template("clientes/form.html", cliente=None)


@bp_clientes.route("/<int:id>/editar", methods=["GET", "POST"])
def editar(id):
    c = db.get_or_404(Cliente, id)
    if request.method == "POST":
        nombre = request.form.get("nombre", "").strip()
        if not nombre:
            flash("El nombre es obligatorio.", "danger")
        else:
            c.nombre = nombre
            c.telefono = request.form.get("telefono", "").strip()
            db.session.commit()
            flash("Cliente actualizado.", "success")
            return redirect(url_for("clientes.listar"))
    return render_template("clientes/form.html", cliente=c)


@bp_clientes.route("/<int:id>/eliminar", methods=["POST"])
def eliminar(id):
    c = db.get_or_404(Cliente, id)
    if c.pedidos:
        flash("No se puede eliminar: el cliente tiene pedidos.", "warning")
    else:
        db.session.delete(c)
        db.session.commit()
        flash("Cliente eliminado.", "success")
    return redirect(url_for("clientes.listar"))