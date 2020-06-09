import os
from flask import Flask, render_template, request, redirect, url_for, send_file, flash
import pyAesCrypt
import shutil



app= Flask(__name__)
app.config['UPLOAD_FOLDER']='uploaded'
app.config['SECRET_KEY']='377959898262d5bd73edcd7992e8ca35'
bufferSize = 64 * 1024
password = "3edcp7992ezca3k"
buf='temp'


def get_files_info():
	file_list={}
	total_size=0
	start_path=app.config['UPLOAD_FOLDER']
	i=1
	
	for path,dirs,files in os.walk(start_path):
		for file in files:
			unit='MB'
			f_path=os.path.join(path,file)
			size=os.path.getsize(f_path)/1000000
			total_size+=size
			if size<1:
				size=round(size*1000,2)
				unit='KB'
			file_list[i]=[file,size,unit]
			i+=1

	total_size = round(total_size,2)
	percent_full = round((total_size/400)*100,2)

	return (file_list,total_size,percent_full)


@app.route("/uploader",methods=['GET','POST'])
def save_file():
	if(request.method == 'POST'):
		f=request.files['fl1']
		f_path=os.path.join(app.config['UPLOAD_FOLDER'],f.filename)
		f.save(f_path)
		pyAesCrypt.encryptFile(f_path, f"{f_path}.aes", password, bufferSize)
		flash(f'{f.filename} is uploaded ',category='success')
		os.remove(f_path)
	return redirect(url_for('home'))
	

@app.route("/delete_file/<string:fname>")
def delete_file(fname):
	f_path=os.path.join(app.config['UPLOAD_FOLDER'],fname)
	os.remove(f_path)
	flash(f'{fname} is deleted ',category='danger')
	return redirect(url_for('home'))
	

@app.route("/view_file/<int:task>/<string:fname>")
def view_file(task,fname):
	if not os.path.isdir(buf):
		os.mkdir(buf)
	f_path=os.path.join(app.config['UPLOAD_FOLDER'],fname)
	buf_path=os.path.join(buf,fname[:-4])
	pyAesCrypt.decryptFile(f_path,buf_path, password, bufferSize)
	return send_file(buf_path,as_attachment=task)
	
	

	
@app.route("/")
@app.route("/home")
def home():
	if os.path.isdir(buf):
		shutil.rmtree(buf)
	file_list,total_size,percent_full=get_files_info()
	return render_template('display.html',file_list=file_list,total_size=total_size,percent_full=percent_full)




if __name__ == '__main__':
	app.run(debug=True)
