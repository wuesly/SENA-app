from flask import Blueprint, render_template, redirect, request, url_for, session, flash, send_file
from models import Instructor, GuiaAprendizaje
from bson import ObjectId
from werkzeug.utils import secure_filename
import io

main = Blueprint('main', __name__)

@main.route('/')
def index():
    if 'usuario' in session:
        return redirect(url_for('main.subir'))
    return redirect(url_for('main.login'))

@main.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        nombre = request.form['nombre']
        correo = request.form['correo']
        regional = request.form['regional']
        usuario = correo.split('@')[0]
        contraseña = '123456'  # Generar aleatoria o fija

        if Instructor.objects(correo=correo).first():
            flash('Este correo ya está registrado.')
            return redirect(url_for('main.registro'))

        nuevo = Instructor(
            nombre=nombre,
            correo=correo,
            regional=regional,
            usuario=usuario,
            contraseña=contraseña
        ).save()
        flash(f'Registro exitoso. Tu usuario es {usuario} y contraseña {contraseña}.')
        return redirect(url_for('main.login'))

    return render_template('registro.html')

@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['usuario']
        contraseña = request.form['contraseña']
        instructor = Instructor.objects(usuario=usuario, contraseña=contraseña).first()
        if instructor:
            session['usuario'] = usuario
            return redirect(url_for('main.subir'))
        flash('Credenciales inválidas.')
    return render_template('login.html')

@main.route('/logout')
def logout():
    session.pop('usuario', None)
    return redirect(url_for('main.login'))

@main.route('/subir', methods=['GET', 'POST'])
def subir():
    if 'usuario' not in session:
        return redirect(url_for('main.login'))

    instructor = Instructor.objects(usuario=session['usuario']).first()

    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        programa = request.form['programa']
        archivo = request.files['archivo']

        if archivo and archivo.filename.endswith('.pdf'):
            guia = GuiaAprendizaje(
                nombre=nombre,
                descripcion=descripcion,
                programa=programa,
                archivo_pdf=archivo.read(),
                instructor=instructor
            ).save()
            flash('Guía subida exitosamente.')
            return redirect(url_for('main.guias'))
        else:
            flash('Debe subir un archivo PDF.')

    return render_template('subir.html')

@main.route('/guias')
def guias():
    if 'usuario' not in session:
        return redirect(url_for('main.login'))

    todas = GuiaAprendizaje.objects()
    return render_template('guias.html', guias=todas)

@main.route('/pdf/<id>')
def ver_pdf(id):
    guia = GuiaAprendizaje.objects(id=ObjectId(id)).first()
    if guia:
        return send_file(io.BytesIO(guia.archivo_pdf.read()),
                         mimetype='application/pdf',
                         as_attachment=False,
                         download_name=f'{guia.nombre}.pdf')
    return 'Archivo no encontrado', 404
