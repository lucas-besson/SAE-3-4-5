#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint, jsonify
from flask import Flask, request, render_template, redirect, abort, flash, session

from connexion_db import get_db

admin_dataviz = Blueprint('admin_dataviz', __name__,
                        template_folder='templates')

@admin_dataviz.route('/admin/dataviz/etat1')
def show_type_article_stock():
    mycursor = get_db().cursor()

    sql = '''SELECT DISTINCT ski.id_type_ski AS id_type, ts.libelle_type_ski as libelle_type
             FROM ski
             INNER JOIN type_ski ts on ski.id_type_ski = ts.id_type_ski'''
    mycursor.execute(sql)
    ski_types = mycursor.fetchall()
    ski_type = request.args.get('type_ski')

    sql_somme = 'SELECT SUM(prix_declinaison) as total FROM declinaison_ski'
    mycursor.execute(sql_somme)
    somme = mycursor.fetchone()

    if ski_type is None:
        return render_template('admin/dataviz/dataviz_etat_1.html', ski_types=ski_types, somme=somme)
    else:
        sql = '''
        SELECT d.id_declinaison_ski AS id_declinaison, s.libelle_ski AS nom_ski, d.stock, l.longueur_ski
        FROM ski s
        INNER JOIN declinaison_ski d ON s.id_ski = d.id_ski
        INNER JOIN longueur l on d.id_longueur_ski = l.id_longueur_ski
        WHERE s.id_type_ski = %s
        '''
        mycursor.execute(sql, (ski_type,))
        data = mycursor.fetchall()
        labels = [f"{row['nom_ski']} ({row['longueur_ski']} cm)" for row in data]
        values = [row['stock'] for row in data]

        return jsonify(labels=labels, values=values)

@admin_dataviz.route('/admin/dataviz/etat2')
def show_type_article_stock_etat2():
    mycursor = get_db().cursor()

    sql = '''SELECT t.id_type_ski AS id, t.libelle_type_ski AS libelle_type , COUNT(*) as nb_articles
             FROM type_ski t
             JOIN ski s ON t.id_type_ski = s.id_type_ski
             GROUP BY t.id_type_ski, t.libelle_type_ski;'''
    mycursor.execute(sql)
    bilan_type = mycursor.fetchall()


    sql = '''
            SELECT s.libelle_ski AS libelle_ski, COUNT(*) AS nb_commandes
            FROM commande c
            INNER JOIN ligne_commande lc ON c.id_commande = lc.id_commande
            INNER JOIN declinaison_ski ds ON lc.id_declinaison_ski = ds.id_declinaison_ski
            INNER JOIN ski s ON ds.id_ski = s.id_ski
            GROUP BY s.libelle_ski
            ORDER BY nb_commandes DESC
            LIMIT 3
        '''
    mycursor.execute(sql)
    data = mycursor.fetchall()

    labels_commande = [str(row['libelle_ski']) for row in data]
    values_commande = [str(row['nb_commandes']) for row in data]

    sql= '''SELECT l.longueur_ski AS longueur_ski, COUNT(*) AS nb_commandes
            FROM commande c
            INNER JOIN ligne_commande lc ON c.id_commande = lc.id_commande
            INNER JOIN declinaison_ski ds ON lc.id_declinaison_ski = ds.id_declinaison_ski
            INNER JOIN longueur l on ds.id_longueur_ski = l.id_longueur_ski
            GROUP BY ds.id_longueur_ski
            ORDER BY nb_commandes DESC
            LIMIT 3'''
    mycursor.execute(sql)
    data2 = mycursor.fetchall()
    labels_longueur = [str(row['longueur_ski']) + " (cm)" for row in data2]
    values_longueur = [str(row['nb_commandes']) for row in data2]

    sql = '''SELECT utilisateur.nom AS libelle, SUM(prix * quantite) as total_lignes_commande
             FROM utilisateur
             JOIN commande ON utilisateur.id_utilisateur = commande.id_utilisateur
             JOIN ligne_commande ON commande.id_commande = ligne_commande.id_commande
             GROUP BY nom
             LIMIT 3;'''
    mycursor.execute(sql)
    data3 = mycursor.fetchall()
    labels_client = [str(row['libelle']) for row in data3]
    values_client = [str(row['total_lignes_commande']) for row in data3]

    return render_template('admin/dataviz/dataviz_etat_2.html', labels_commande=labels_commande
                           ,values_commande=values_commande
                           , labels_longueur=labels_longueur
                           , values_longueur=values_longueur
                           , bilan_type=bilan_type
                           ,labels_client=labels_client
                           ,values_client=values_client)