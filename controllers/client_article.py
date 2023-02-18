#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, abort, flash, session

from connexion_db import get_db

client_article = Blueprint('client_article', __name__,
                        template_folder='templates')

@client_article.route('/client/index')
@client_article.route('/client/article/show')              # remplace /client
def client_article_show():                                 # remplace client_index
    mycursor = get_db().cursor()
    id_client = session['id_user']
    sql = '''SELECT id_ski AS id_article
                   , libelle_ski AS nom
                   , prix_ski AS prix
                   , stock AS stock
                   , image
                   , id_type_ski AS id_type_article
            FROM ski'''
    condition_and = ""
    list_param = []
    if "filtrer_word" in session or "filter_prix_min" in session or "filter_prix_max" in session or "filter_types" in session:
        sql = sql + " WHERE"
    if "filtrer_word" in session:
        sql = sql + " libelle_ski LIKE %s "
        recherche = "%" + session["filtrer_word"] + "%"
        list_param.append(recherche)
        condition_and = " AND "
    if "filter_prix_min" in session or "filter_prix_max" in session:
        sql = sql + condition_and + " prix_ski BETWEEN %s AND %s "
        list_param.append(session["filter_prix_min"])
        list_param.append(session["filter_prix_max"])
        condition_and = " AND "
    if "filter_types" in session:
        sql = sql + condition_and + "("
        last_item = session['filter_types'][-1]
        for item in session["filter_types"]:
            sql = sql + " ski.id_type_ski=%s "
            if item != last_item:
                sql = sql + " OR "
            list_param.append(item)
        sql = sql + ")"
    tuple_sql = tuple(list_param)
    print("coucou" + sql)
    mycursor.execute(sql, tuple_sql)
    articles = mycursor.fetchall()
    sql = '''
                    SELECT id_type_ski  AS id_type_article
                    ,libelle_type_ski  AS libelle
                    FROM type_ski
                    ORDER BY libelle_type_ski;
                    '''
    mycursor.execute(sql)
    types_article = mycursor.fetchall()




    articles_panier = []

    if len(articles_panier) >= 1:
        sql = ''' calcul du prix total du panier '''
        prix_total = None
    else:
        prix_total = None
    return render_template('client/boutique/panier_article.html'
                           , articles=articles
                           , articles_panier=articles_panier
                           #, prix_total=prix_total
                           , items_filtre=types_article
                           )
