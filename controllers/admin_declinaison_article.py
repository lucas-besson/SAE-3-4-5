#! /usr/bin/python
# -*- coding:utf-8 -*-

from flask import Blueprint
from flask import request, render_template, redirect, flash
from pymysql import IntegrityError

from connexion_db import get_db

admin_declinaison_article = Blueprint('admin_declinaison_article', __name__,
                         template_folder='templates')


@admin_declinaison_article.route('/admin/declinaison_article/add')
def add_declinaison_article():
    id_article=request.args.get('id_article')
    mycursor = get_db().cursor()
    sql1 = '''SELECT id_ski AS id_article FROM ski WHERE id_ski = %s'''
    mycursor.execute(sql1, (id_article,))
    article = mycursor.fetchone()
    sql = '''
            SELECT id_longueur_ski AS id_taille, longueur_ski AS libelle 
            FROM longueur
        '''
    mycursor.execute(sql)
    tailles = mycursor.fetchall()
    return render_template('admin/article/add_declinaison_article.html'
                           , article=article
                           #, couleurs=couleurs
                           , tailles=tailles
                           )


@admin_declinaison_article.route('/admin/declinaison_article/add', methods=['POST'])
def valid_add_declinaison_article():
    mycursor = get_db().cursor()
    id_article = request.form.get('id_article')
    stock = request.form.get('stock')
    taille = request.form.get('taille')

    sql = 'SELECT prix_ski FROM ski WHERE id_ski=%s'
    mycursor.execute(sql, id_article)
    prix=mycursor.fetchone()
    sql = 'SELECT image FROM ski WHERE id_ski=%s'
    mycursor.execute(sql, id_article)
    image = mycursor.fetchone()
    #couleur = request.form.get('couleur')
    sql = 'INSERT INTO declinaison_ski (id_ski, id_longueur_ski, stock,prix_declinaison,image) VALUES (%s, %s, %s, %s,%s)'
    tuples_insert = (id_article, taille, stock, prix['prix_ski'],image['image'])
    mycursor.execute(sql, tuples_insert)
    get_db().commit()
    return redirect('/admin/article/edit?id_article=' + id_article)


@admin_declinaison_article.route('/admin/declinaison_article/edit', methods=['GET'])
def edit_declinaison_article():
    id_declinaison_article = request.args.get('id_declinaison_article')
    mycursor = get_db().cursor()

    sql = '''SELECT id_declinaison_ski AS id_declinaison_article, l.id_longueur_ski AS taille_id, l.longueur_ski AS libelle, declinaison_ski.stock, image AS image_article, id_ski AS article_id 
               FROM declinaison_ski
               INNER JOIN longueur l ON declinaison_ski.id_longueur_ski = l.id_longueur_ski
                WHERE id_declinaison_ski=%s'''
    mycursor.execute(sql, (id_declinaison_article))
    declinaison_article = mycursor.fetchone()

    sql2 = '''
        SELECT longueur.id_longueur_ski AS id_taille, longueur_ski AS libelle
        FROM longueur
        LEFT JOIN declinaison_ski ON declinaison_ski.id_longueur_ski = longueur.id_longueur_ski
        AND declinaison_ski.id_declinaison_ski = %s;
    '''
    mycursor.execute(sql2, (id_declinaison_article))
    tailles = mycursor.fetchall()

    couleurs=''

    return render_template('admin/article/edit_declinaison_article.html'
                           , tailles=tailles
                           , couleurs=couleurs
                           , declinaison_article=declinaison_article
                           )



@admin_declinaison_article.route('/admin/declinaison_article/edit', methods=['POST'])
def valid_edit_declinaison_article():
    id_declinaison_article = request.form.get('id_declinaison_article','')
    id_article = request.form.get('id_article','')
    stock = request.form.get('stock','')
    taille_id = request.form.get('id_taille','')
    couleur_id = request.form.get('id_couleur','')
    mycursor = get_db().cursor()
    sql = '''  UPDATE declinaison_ski SET stock=%s,id_longueur_ski=%s  where id_declinaison_ski=%s '''
    mycursor.execute(sql, (stock,taille_id, id_declinaison_article))
    get_db().commit()

    message = u'declinaison_article modifié , id:' + str(id_declinaison_article) + '- stock :' + str(stock) + ' - taille_id:' + str(taille_id) + ' - couleur_id:' + str(couleur_id)
    flash(message, 'alert-success')
    return redirect('/admin/article/edit?id_article=' + str(id_article))


@admin_declinaison_article.route('/admin/declinaison_article/delete', methods=['GET'])
def admin_delete_declinaison_article():
    id_declinaison_article = request.args.get('id_declinaison_article','')
    id_article = request.args.get('id_article','')
    print(id_article)
    mycursor = get_db().cursor()
    try:
        sql = "DELETE FROM declinaison_ski WHERE id_declinaison_ski=%s"
        mycursor.execute(sql, (id_declinaison_article,))
        get_db().commit()
        flash(u'déclinaison supprimée, id_declinaison_article : ' + str(id_declinaison_article), 'alert-success')
        return redirect('/admin/article/edit?id_article=' + str(id_article))

    except IntegrityError:
        flash(u"Impossible de supprimer la déclinaison, car elle est liée à une commande.", 'alert-warning')
        return redirect('/admin/article/edit?id_article=' + str(id_article))

    #flash(u'declinaison supprimée, id_declinaison_article : ' + str(id_declinaison_article),  'alert-success')
    #return redirect('/admin/article/edit?id_article=' + str(id_article))