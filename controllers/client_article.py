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
    sql = '''SELECT ski.id_ski AS id_article
                , ski.libelle_ski AS nom
                , ski.prix_ski AS prix
                , SUM(ds.stock) AS stock
                , ski.image
                , ski.id_type_ski AS id_type_article
                , COUNT(DISTINCT id_longueur_ski) AS nb_declinaison
                FROM ski
             INNER JOIN declinaison_ski ds on ski.id_ski = ds.id_ski'''
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
    sql+= ''' GROUP BY ski.id_ski, ski.libelle_ski, ski.prix_ski, ski.image, ski.id_type_ski; '''
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



    sql=''' SELECT s.id_ski, s.libelle_ski AS nom, lp.quantite, ds.prix_declinaison AS prix, lp.id_declinaison_ski AS id_declinaison_article, ds.stock, l.id_longueur_ski as id_taille, longueur_ski as libelle_couleur, nb_longueurs.nb_longueurs_diff AS nb_declinaison
            FROM ligne_panier lp
            INNER JOIN declinaison_ski ds ON lp.id_declinaison_ski = ds.id_declinaison_ski
            INNER JOIN longueur l on ds.id_longueur_ski = l.id_longueur_ski
            INNER JOIN ski s ON ds.id_ski = s.id_ski
            INNER JOIN (
                SELECT ds.id_ski, COUNT(DISTINCT ds.id_longueur_ski) AS nb_longueurs_diff
                FROM declinaison_ski ds
                GROUP BY ds.id_ski
            ) AS nb_longueurs ON s.id_ski = nb_longueurs.id_ski
            WHERE lp.id_utilisateur = %s
            GROUP BY s.id_ski, s.libelle_ski, lp.quantite, ds.prix_declinaison, lp.id_declinaison_ski, ds.stock, longueur_ski;'''
    mycursor.execute(sql,(id_client))
    articles_panier = mycursor.fetchall()

    if len(articles_panier) >= 1:
        sql = ''' SELECT SUM(ds.prix_declinaison*lp.quantite) as prix
                  FROM ligne_panier lp
                  INNER JOIN declinaison_ski ds ON lp.id_declinaison_ski = ds.id_declinaison_ski
                  INNER JOIN ski s ON ds.id_ski = s.id_ski
                  WHERE lp.id_utilisateur=%s;'''
        mycursor.execute(sql, id_client)
        prix_total = mycursor.fetchone()
    else:
        prix_total = None
    return render_template('client/boutique/panier_article.html'
                           , articles=articles
                           , articles_panier=articles_panier
                           , prix_total=prix_total
                           , items_filtre=types_article
                           )
