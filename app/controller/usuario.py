from app.models.usuario import db, Usuario
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user

user_bp = Blueprint("usuarios", __name__)

@user_bp.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        if Usuario.query.filter_by(nome=request.form['nome']).first():
            flash('Nome de usuário já existe. Escolha outro.', 'error')
            return redirect(url_for('usuarios.cadastro'))
        if request.form['senha'] == request.form['confirmar-senha']:
            usuario = Usuario(request.form['nome'], request.form['senha'])
            db.session.add(usuario)
            db.session.commit()
            # criar time vazio padrão para o novo usuário (associado por id)
            try:
                rows = _read_teams()
            except Exception:
                rows = []
            usuario_id = str(usuario.id)
            if not any(r.get('usuario_id') == usuario_id for r in rows):
                rows.append({'usuario_id': usuario_id, 'nome_time': f'Meu Time', 'pokemons': ''})
                try:
                    _write_teams(rows)
                except Exception:
                    pass
            flash('Cadastro realizado com sucesso! Faça login.', 'success')
            return redirect(url_for('usuarios.login')) 
        else:
            flash('Senhas divergentes.', 'error')
        
    return render_template('cadastro.html')

@user_bp.route('/login', methods=['GET', 'POST'])
def login():

    if current_user.is_authenticated:
        return redirect(url_for('home.home'))
    
    if request.method == 'POST':
        nome = request.form['nome']
        senha = request.form['senha']
        usuario = Usuario.query.filter_by(nome=nome).first()
        if usuario and usuario.check_password(senha):
            login_user(usuario) 
            next_page = request.args.get('next')
            flash(f'Bem vindo, {nome}!', 'success')
            return redirect(next_page or url_for('home.home'))
        else:
            flash('Nome de usuário ou senha inválidos.', 'error')
            return redirect(url_for('usuarios.login'))

    return render_template('login.html') 

@user_bp.route('/logout')
@login_required 
def logout():
    logout_user()
    flash('Você saiu da sua conta.', 'error')
    return redirect(url_for('home.home'))

# 4. ROTA DE DELETE
@user_bp.route('/delete/<int:id>', methods=['GET'])
@login_required
def delete(id):
    usuario = Usuario.query.get(id)
    logout_user()
    db.session.delete(usuario)
    db.session.commit()
    flash('Sua conta foi deletada com sucesso.', 'error')
    return redirect(url_for('home.home'))

import csv
import os


def _ler_pokemons_csv():
    caminho = os.path.join('app', 'data', 'pokemons.csv')
    pokemons = []
    if not os.path.exists(caminho):
        return pokemons
    with open(caminho, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            pokemons.append({
                'id': row.get('id'),
                'nome': row.get('nome'),
                'tipo1': row.get('tipo1'),
                'tipo2': row.get('tipo2'),
                'imagem': row.get('imagem')
            })
    return pokemons

def _read_teams():
    caminho = os.path.join('app', 'data', 'teams.csv')
    rows = []
    if not os.path.exists(caminho):
        return rows
    with open(caminho, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # suportar antigas entradas com 'usuario' ou novas com 'usuario_id'
            if 'usuario_id' not in row and 'usuario' in row:
                row['usuario_id'] = row.get('usuario')
            rows.append(row)
    return rows


def _write_teams(rows):
    caminho = os.path.join('app', 'data', 'teams.csv')
    os.makedirs(os.path.dirname(caminho), exist_ok=True)
    header = ['usuario_id', 'nome_time', 'pokemons']
    with open(caminho, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=header)
        writer.writeheader()
        for r in rows:
            writer.writerow({
                'usuario_id': r.get('usuario_id'),
                'nome_time': r.get('nome_time', ''),
                'pokemons': r.get('pokemons', '')
            })

@user_bp.route('/time')
@login_required
def time():
    rows = _read_teams()
    usuario_id = str(current_user.id)
    team_row = None
    for row in rows:
        if row.get('usuario_id') == usuario_id:
            team_row = row
            break

    pokemons_all = _ler_pokemons_csv()
    id_to_pokemon = {p['id']: p for p in pokemons_all}

    team_pokemons = []
    team_name = 'Meu Time'
    if team_row:
        team_name = team_row.get('nome_time') or team_name
        poks = team_row.get('pokemons', '')
        pids = [p for p in poks.split(';') if p] if poks else []
        for pid in pids:
            p = id_to_pokemon.get(pid)
            if p:
                team_pokemons.append(p)
            else:
                # fallback para caso não encontre no CSV
                team_pokemons.append({'id': pid, 'nome': pid, 'tipo1': '', 'tipo2': '', 'imagem': ''})

    return render_template('team.html', team_pokemons=team_pokemons, team_name=team_name)


@user_bp.route('/time/adicionar', methods=['POST'])
@login_required
def add_to_team():
    pokemon_id = request.form.get('pokemon_id')
    if not pokemon_id:
        flash('Pokémon inválido.', 'error')
        return redirect(request.referrer or url_for('home.home'))

    rows = _read_teams()
    usuario_id = str(current_user.id)
    team = None
    for r in rows:
        if r.get('usuario_id') == usuario_id:
            team = r
            break

    if not team:
        # criar time padrão
        team = {'usuario_id': usuario_id, 'nome_time': f'Time de {current_user.nome}', 'pokemons': ''}
        rows.append(team)

    poks = team.get('pokemons', '')
    lista = [p for p in poks.split(';') if p] if poks else []

    if pokemon_id in lista:
        flash('Pokémon já está no seu time.', 'error')
        return redirect(request.referrer or url_for('home.home'))

    if len(lista) >= 6:
        flash('Seu time já tem 6 pokémons.', 'error')
        return redirect(request.referrer or url_for('home.home'))

    lista.append(pokemon_id)
    team['pokemons'] = ';'.join(lista)
    _write_teams(rows)
    flash('Pokémon adicionado ao time!', 'success')
    return redirect(request.referrer or url_for('usuarios.time'))


@user_bp.route('/time/remover', methods=['POST'])
@login_required
def remove_from_team():
    pokemon_id = request.form.get('pokemon_id')
    if not pokemon_id:
        flash('Pokémon inválido.', 'error')
        return redirect(request.referrer or url_for('home.home'))

    rows = _read_teams()
    usuario_id = str(current_user.id)
    team = None
    for r in rows:
        if r.get('usuario_id') == usuario_id:
            team = r
            break

    if not team:
        flash('Você não tem um time para remover pokémons.', 'error')
        return redirect(request.referrer or url_for('home.home'))

    poks = team.get('pokemons', '')
    lista = [p for p in poks.split(';') if p] if poks else []

    if pokemon_id not in lista:
        flash('Pokémon não está no seu time.', 'error')
        return redirect(request.referrer or url_for('home.home'))

    lista = [p for p in lista if p != pokemon_id]
    team['pokemons'] = ';'.join(lista)
    _write_teams(rows)
    flash('Pokémon removido do time.', 'success')
    return redirect(request.referrer or url_for('usuarios.time'))

