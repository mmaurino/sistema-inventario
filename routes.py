from flask import render_template, redirect, url_for, flash
from app import app
from models import db, Producto
from forms import ProductoForm
from flask import request


@app.route('/')
def home():
    return render_template('inicio.html')

@app.route('/agregar', methods=['GET', 'POST'])
def agregar_producto():
    form = ProductoForm()
    if form.validate_on_submit():
        nuevo_producto = Producto(
            nombre=form.nombre.data,
            descripcion=form.descripcion.data,
            stock=form.stock.data,
            precio=form.precio.data
        )
        db.session.add(nuevo_producto)
        db.session.commit()
        flash('Producto agregado exitosamente', 'success')
        return redirect(url_for('agregar_producto'))
    return render_template('agregar.html', form=form)


@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar_producto(id):
    producto = Producto.query.get_or_404(id)  # Obtiene el producto por id
    form = ProductoForm(obj=producto)  # Crea un formulario con los datos del producto

    if form.validate_on_submit():
        producto.nombre = form.nombre.data
        producto.descripcion = form.descripcion.data
        producto.stock = form.stock.data
        producto.precio = form.precio.data
        db.session.commit()  # Guarda los cambios en la base de datos
        flash('Producto actualizado exitosamente', 'success')
        return redirect(url_for('inventario'))  # Redirige a la lista de inventario

    return render_template('editar.html', form=form, producto=producto)

@app.route('/eliminar/<int:id>', methods=['POST'])
def eliminar_producto(id):
    producto = Producto.query.get_or_404(id)  # Obtiene el producto por id
    db.session.delete(producto)  # Elimina el producto de la base de datos
    db.session.commit()
    flash('Producto eliminado exitosamente', 'danger')
    return redirect(url_for('inventario'))  # Redirige a la lista de inventario

@app.route('/inventario', methods=['GET'])
def inventario():
    query = request.args.get('q', '')  # Obtener el parámetro de búsqueda
    if query:
        productos = Producto.query.filter(Producto.nombre.like(f'%{query}%') | Producto.descripcion.like(f'%{query}%')).all()
    else:
        productos = Producto.query.all()  # Si no hay búsqueda, mostrar todos los productos
    return render_template('inventario.html', productos=productos)

@app.route('/reportes')
def reportes():
    # Obtener datos del inventario
    productos = Producto.query.all()

    # Calcular métricas
    total_productos = len(productos)
    stock_bajo = [p for p in productos if p.stock < 5]
    producto_mas_caro = max(productos, key=lambda p: p.precio, default=None)
    producto_mas_barato = min(productos, key=lambda p: p.precio, default=None)
    valor_total_inventario = sum(p.precio * p.stock for p in productos)

    return render_template("reportes.html", 
                           total_productos=total_productos, 
                           stock_bajo=stock_bajo,
                           producto_mas_caro=producto_mas_caro, 
                           producto_mas_barato=producto_mas_barato, 
                           valor_total_inventario=valor_total_inventario)
