from flask import Flask
from flask import render_template,request,redirect,url_for,flash
from flask_mysqldb import MySQL
from flask import send_from_directory
from datetime import datetime
import os

#Mostrar contenido index.html
app=Flask(__name__)
app.secret_key="Develoteca"

#cONEXION bASE DE DATOS
mysql=MySQL()
app.config['MYSQL_DATABASE_HOST']='localhost'
app.config['MYSQL_DATABASE_USER']='ASUS'
app.config['MYSQL_DATABASE_PASSWORD']=''
app.config['MYSQL_DATABASE_DB']='sistema'
#Crear conexion con datos anteriores
mysql.init_app(app) 


CARPETA=os.path.join('uploads')
app.config['CARPETA']=CARPETA

#crear acceso a la carpeta
@app.route('/uploads/<nombreFoto>')
def uploads(nombreFoto):
    return send_from_directory(app.config['CARPETA'],nombreFoto)

@app.route('/')
def index():
    sql="SELECT * FROM `empleados`;" 
    conn=mysql.connection
    cursor=conn.cursor()
    cursor.execute("USE sistema")  
    cursor.execute(sql)
    empleados=cursor.fetchall()
    #print(empleados)
    
    conn.commit()
    return render_template('empleados/index.html', empleados=empleados)

@app.route('/destroy/<int:id>')
def destroy(id):
    print(id)
    conn=mysql.connection
    cursor=conn.cursor()
    cursor.execute("USE sistema")
    cursor.execute("SELECT foto FROM empleados WHERE id=%s", (id,))
    fila=cursor.fetchall()
    os.remove(os.path.join(app.config['CARPETA'],fila[0][0]))
    
    cursor.execute("DELETE FROM empleados WHERE id=%s",(id,))
    conn.commit()
    return redirect('/')

@app.route('/create')
def create():
    return render_template('empleados/create.html')

@app.route('/store', methods=['POST'])
def storage():
    _nombre=request.form['txtNombre']
    _correo=request.form['txtCorreo']
    _foto=request.files['txtFoto']

    #Validacion
    if _nombre =='' or _correo =='' or _foto =='':
        flash('Recuerda llenar los datos de los campos')
        return redirect(url_for('create'))
    
    now=datetime.now()
    tiempo=now.strftime("%Y%H%M%S")
    if _foto.filename!='':
        nuevoNombreFoto=tiempo+_foto.filename
        _foto.save("uploads/"+nuevoNombreFoto)
    
    sql="INSERT INTO `empleados` (`id`, `nombre`, `correo`, `foto`) VALUES (NULL, %s, %s, %s);" 
    datos=(_nombre,_correo,nuevoNombreFoto)
    
    conn=mysql.connection
    cursor=conn.cursor()
    cursor.execute("USE sistema")  
    cursor.execute(sql,datos)
    conn.commit()
    
    return redirect('/')
    #return render_template('empleados/index.html')
    
@app.route('/edit/<int:id>')
def edit(id):
    conn=mysql.connection
    cursor=conn.cursor()
    cursor.execute("USE sistema")  
    cursor.execute("SELECT * FROM empleados WHERE id=%s",(id,))
    empleados=cursor.fetchall()
    conn.commit()
    print(empleados)
    return render_template('empleados/edit.html', empleados=empleados)

@app.route('/update', methods=['POST'])
def update():
    _nombre=request.form['txtNombre']
    _correo=request.form['txtCorreo']
    _foto=request.files['txtFoto']
    id=request.form['txtID']

    sql="UPDATE empleados SET nombre=%s, correo=%s WHERE id=%s;" 
    datos=(_nombre,_correo,id)
    
    conn=mysql.connection
    cursor=conn.cursor()
    
    now=datetime.now()
    tiempo=now.strftime("%Y%H%M%S")
    if _foto.filename!='':
        nuevoNombreFoto=tiempo+_foto.filename
        _foto.save("uploads/"+nuevoNombreFoto)
        cursor.execute("USE sistema") 
        cursor.execute("SELECT foto FROM empleados WHERE id=%s", (id,))
        fila=cursor.fetchall()
        
        os.remove(os.path.join(app.config['CARPETA'],fila[0][0]))
        cursor.execute("UPDATE empleados SET foto=%s WHERE id=%s",(nuevoNombreFoto,id))
        conn.commit()
        

    cursor.execute("USE sistema")  
    cursor.execute(sql,datos)
    conn.commit()
    
    
    return redirect('/')



if __name__=='__main__':
    app.run(debug=True)