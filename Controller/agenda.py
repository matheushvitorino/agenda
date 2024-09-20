from flask import request,render_template, Blueprint, Response,url_for,jsonify,redirect,flash, session
from Models.models import db, Agenda
import json
from datetime import time
from functools import wraps
app = Blueprint('agenda',__name__)


@app.route('/')
def index():
    if 'usuario' in session:
        usuario = session.get('usuario')
        agenda = Agenda.query.all() 
        return render_template('/index.html', agenda = agenda, usuario = usuario)
    return render_template('/login.html')

@app.route('/adicionar', methods=['POST'])
def adicionar():
    if request.headers.get('content-type') == 'application/json':
        try:
            tarefa = request.form['tarefa']
            horario_str = request.form['horario']
            horario = time.fromisoformat(horario_str)
            novaTarefa = Agenda(tarefa,horario)                
            db.session.add(novaTarefa)
            db.session.commit()
            return Response(response=json.dumps(novaTarefa.to_dict()), status= 200, content_type='application/json')
        except Exception as e:
            flash(f'Ocorreu um erro: {str(e)}', 'error')
        return redirect(url_for('agenda.index'))
    else:
        tarefa = request.form['tarefa']
        horario_str = request.form['horario']
        
        if not tarefa or not horario_str:
            if not tarefa:
                flash('Erro: Tarefa vazia.', 'error')
                return redirect(url_for('agenda.index'))
            
            if not horario_str:
                flash('Erro: Horario vazio')
                return redirect(url_for('agenda.index'))
                

        try:
            horario = time.fromisoformat(horario_str)
        except ValueError:
            flash('Formato de horário inválido. Use o formato HH:MM.')
            return redirect(url_for('agenda.index'))
    novaTarefa = Agenda(tarefa,horario)
    db.session.add(novaTarefa)
    db.session.commit()
    flash('Concluido', 'success')
    return redirect(url_for('agenda.index'))




@app.route('/viewall', methods=['GET'])
def viewall():  
    tarefas = Agenda.query.all()
    tarefas_dict = [tarefa.to_dict() for tarefa in tarefas]
    return Response(response=json.dumps(tarefas_dict), status= 200, content_type='application/json')

@app.route('/view/<int:id>', methods=['GET'])
def view(id):
    tarefas = Agenda.query.get(id)
    return Response(response=json.dumps(tarefas.to_dict()), status= 200, content_type='application/json')


    
@app.route('/deletar/<int:id>', methods=['POST'])
def deletar(id):
    if request.headers.get('content-type') == 'application/json':
        tarefa = Agenda.query.get(id)
        if tarefa is None:
            return jsonify({'error': 'Registro não encontrado'}), 404

        try:
            db.session.delete(tarefa)
            db.session.commit()
            return jsonify({'message': 'Registro deletado com sucesso'})
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500
    else:
        tarefa = Agenda.query.get(id)
        if tarefa is None:
            return jsonify({'error': 'Registro não encontrado'}), 404

        try:
            db.session.delete(tarefa)
            db.session.commit()
            return redirect(url_for('agenda.index'))
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500


@app.route('/login', methods=['POST','GET'])
def login():
    if request.method == 'POST':
        usuario = request.form['usuario']
        senha =  request.form['senha']
        resultado = autenticar_usuarios(usuario,senha)
        autenticado, mensagem_erro = resultado

        if autenticado:
            session['usuario'] = usuario
            return redirect(url_for('agenda.index'))
        else:
            flash(mensagem_erro, 'error')
    return render_template('/login.html')

@app.route('/logout')
def logout():
    session.pop('usuario', None)
    return redirect(url_for('agenda.index'))


def autenticar_usuarios(usuario,senha):
    if not usuario or not senha:
        if not usuario:
            return False,'Erro usuario vazio'
            
        if not senha:
            return False, 'Erro: senha vazio'
    if usuario =='admin' and senha =='12345':
        return True, ''
    else:
        return False, 'Erro: Login ou senha incorretos'
    

    
    
