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

    sql = '''
            SELECT id_ski AS id_article
                   , libelle_ski AS nom
                   , prix_ski AS prix
                   , stock AS stock
                   , image
            FROM ski
            ORDER BY libelle_ski;
            '''
    mycursor.execute(sql)
    ski = mycursor.fetchall()
    articles = ski

    sql = '''
                SELECT id_type_ski  AS id_type_article
                        ,libelle_type_ski  AS libelle
                FROM type_ski
                ORDER BY libelle_type_ski;
                '''
    mycursor.execute(sql)
    taille= mycursor.fetchall()
    types_article = taille
    print(types_article)

    sql = '''    '''
    list_param = []
    condition_and = ""
    # utilisation du filtre
    sql3='''  '''
    #articles =[]


    # pour le filtre
    #types_article = []


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
