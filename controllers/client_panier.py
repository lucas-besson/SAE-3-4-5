#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import request, render_template, redirect, abort, flash, session

from connexion_db import get_db

client_panier = Blueprint('client_panier', __name__,
                        template_folder='templates')


@client_panier.route('/client/panier/add', methods=['POST'])
def client_panier_add():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    id_article = request.form.get('id_article')
    quantite = int(request.form.get('quantite'))
    id_declinaison_article=request.form.get('id_declinaison_article', None)

    if id_declinaison_article==None:
        sql = ''' SELECT d.id_declinaison_ski as id_declinaison_article, d.stock, l.id_longueur_ski as id_taille, l.longueur_ski as libelle_taille
                 FROM declinaison_ski d
                 INNER JOIN longueur l ON d.id_longueur_ski=l.id_longueur_ski
                 WHERE d.id_ski=%s  '''
        mycursor.execute(sql, (id_article,))

    else:
        sql = ''' SELECT d.id_declinaison_ski as id_declinaison_article, d.stock, l.id_longueur_ski as id_taille, l.longueur_ski as libelle_taille
                        FROM declinaison_ski d
                        INNER JOIN longueur l ON d.id_longueur_ski=l.id_longueur_ski
                        WHERE d.id_declinaison_ski=%s  '''
        mycursor.execute(sql, (id_declinaison_article,))

    declinaisons = mycursor.fetchall()
    if len(declinaisons) == 1:
        id_declinaison_article = declinaisons[0]['id_declinaison_article']
    elif len(declinaisons) == 0:
        return abort(404, "pb nb de declinaison")
    else:
        sql = '''SELECT id_declinaison_ski as id_declinaison_article, stock,prix_declinaison as prix,s.image,id_longueur_ski, libelle_ski as nom, prix_ski as prix
                 FROM declinaison_ski
                 INNER JOIN ski s on declinaison_ski.id_ski = s.id_ski
                 WHERE s.id_ski=%s'''
        mycursor.execute(sql, (id_article,))
        article = mycursor.fetchone()
        return render_template('client/boutique/declinaison_article.html'
                           , declinaisons=declinaisons
                           , quantite=quantite
                           , article=article)


    sql = " Select * from ligne_panier where id_declinaison_ski=%s and id_utilisateur=%s"
    mycursor.execute(sql,(id_declinaison_article, id_client))
    article_panier = mycursor.fetchone()

    mycursor.execute(" Select * from declinaison_ski where id_declinaison_ski=%s", ( id_declinaison_article ))
    article = mycursor.fetchone()

    if not (article_panier is None) and int(article_panier['quantite']) >= 1:
        tuple_update = (quantite, id_client, id_declinaison_article)
        sql="Update ligne_panier set quantite = quantite+%s where id_utilisateur=%s and id_declinaison_ski=%s"
        mycursor.execute(sql, tuple_update)
    else:
        tuple_insert = (id_client, id_declinaison_article, quantite)
        sql="INSERT INTO ligne_panier (id_utilisateur, id_declinaison_ski, quantite, date_ajout) values (%s,%s,%s, current_timestamp)"
        mycursor.execute(sql, tuple_insert)

    sql ='''SELECT stock FROM declinaison_ski WHERE id_declinaison_ski=%s'''
    mycursor.execute(sql, id_declinaison_article)
    stock_actuellle = mycursor.fetchone()['stock']

    if quantite <= stock_actuellle:
        stock_final = stock_actuellle - quantite

        sql = '''UPDATE declinaison_ski SET stock=%s WHERE id_declinaison_ski=%s'''
        mycursor.execute(sql, (stock_final, id_declinaison_article))
        get_db().commit()
        return redirect('/client/article/show')
    else:
        flash("Article plus disponible")
        return redirect('/client/article/show')


@client_panier.route('/client/panier/delete', methods=['POST'])
def client_panier_delete():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    id_article = request.form.get('id_article','')
    quantite = 1
    id_declinaison_article=request.form.get('id_declinaison_article', None)

    sql = ''' SELECT *
                  FROM ligne_panier
                  WHERE id_utilisateur=%s AND id_declinaison_ski=%s; '''
    mycursor.execute(sql, (id_client, id_declinaison_article))
    article_panier= mycursor.fetchone()

    if not(article_panier is None) and article_panier['quantite'] > 1:
        print(id_declinaison_article)
        sql = ''' UPDATE declinaison_ski SET stock=(stock+1) WHERE id_declinaison_ski=%s '''
        mycursor.execute(sql,id_declinaison_article)
        sql2 = ''' UPDATE ligne_panier SET quantite = quantite-1 WHERE id_declinaison_ski=%s '''
        mycursor.execute(sql2, id_declinaison_article)
    else:
        print(id_declinaison_article)
        sql3 = ''' DELETE FROM ligne_panier WHERE id_utilisateur=%s AND id_declinaison_ski=%s'''
        mycursor.execute(sql3,(id_client,id_declinaison_article))

        sql4 = '''UPDATE declinaison_ski SET stock=stock+1 WHERE id_declinaison_ski=%s'''
        mycursor.execute(sql4, id_declinaison_article)

    get_db().commit()
    return redirect('/client/article/show')



@client_panier.route('/client/panier/vider', methods=['POST'])
def client_panier_vider():
    mycursor = get_db().cursor()
    client_id = session['id_user']
    sql = ''' SELECT *
                  FROM ligne_panier
                  WHERE id_utilisateur=%s '''
    mycursor.execute(sql, (client_id))
    items_panier = mycursor.fetchall()
    for item in items_panier:
        sql = ''' DELETE FROM ligne_panier WHERE id_utilisateur=%s AND id_declinaison_ski=%s '''
        mycursor.execute(sql, (client_id, item['id_declinaison_ski'] ))

        sql2=''' UPDATE declinaison_ski SET stock=(stock+%s) WHERE id_declinaison_ski=%s'''
        mycursor.execute(sql2, (item['quantite'], item['id_declinaison_ski']))
        get_db().commit()
    return redirect('/client/article/show')


@client_panier.route('/client/panier/delete/line', methods=['POST'])
def client_panier_delete_line():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    id_article = request.form.get('id_article')
    id_declinaison_article = request.form.get('id_declinaison_article')

    sql = ''' SELECT *
              FROM ligne_panier
              WHERE id_utilisateur=%s AND id_declinaison_ski=%s; '''
    mycursor.execute(sql,(id_client,id_declinaison_article))
    quantiter = mycursor.fetchone()

    sql = ''' DELETE FROM ligne_panier WHERE id_utilisateur=%s AND id_declinaison_ski=%s '''
    mycursor.execute(sql, (id_client, id_declinaison_article))
    sql2=''' UPDATE declinaison_ski SET stock=(stock+%s) WHERE id_declinaison_ski=%s'''
    mycursor.execute(sql2, (quantiter['quantite'], id_declinaison_article))

    get_db().commit()
    return redirect('/client/article/show')


@client_panier.route('/client/panier/filtre', methods=['POST'])
def client_panier_filtre():
    filter_word = request.form.get('filter_word', None)
    filter_prix_min = request.form.get('filter_prix_min', None)
    filter_prix_max = request.form.get('filter_prix_max', None)
    filter_types = request.form.getlist('filter_types', None)
    if filter_word or filter_word == "":
        if len(filter_word) > 1:
            if filter_word.isalpha():
                session['filtrer_word'] = filter_word
            else:
                flash(u'votre mot recherché doit uniquement être composé de lettres')
        else:
            if len(filter_word) == 1:
                flash(u'votre mot recherché doit être composé de au moins 2 lettres')
            else:
                session.pop('filtrer_word', None)
    if filter_prix_min or filter_prix_max:
        if filter_prix_min.isdecimal() or filter_prix_max.isdecimal():
            if int(filter_prix_min) < int(filter_prix_max):
                session["filter_prix_min"] = filter_prix_min
                session["filter_prix_max"] = filter_prix_max
            else:
                flash(u'min < max')
        else:
            flash(u'min et max doivent être des numériques')
    if filter_types and filter_types != []:
        print(f"types: {filter_types}")
        if isinstance(filter_types, list):
            check = True
            for number in filter_types:
                print(f"number: {number}")
                if not number.isdecimal():
                    check = False
            if check:
                session["filter_types"] = filter_types
    return redirect('/client/article/show')


@client_panier.route('/client/panier/filtre/suppr', methods=['POST'])
def client_panier_filtre_suppr():
    session.pop('filter_word', None)
    session.pop('filter_prix_min', None)
    session.pop('filter_prix_max', None)
    session.pop('filter_types', None)
    print("suppr filtre")
    return redirect('/client/article/show')
