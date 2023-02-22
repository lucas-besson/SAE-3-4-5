#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, url_for, abort, flash, session, g
from datetime import datetime
from connexion_db import get_db

client_commande = Blueprint('client_commande', __name__,
                        template_folder='templates')


@client_commande.route('/client/commande/valide', methods=['POST'])
def client_commande_valide():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    sql = ''' SELECT libelle_ski AS nom, quantite, prix_ski AS prix
            FROM ski
            INNER JOIN ligne_panier lp on ski.id_ski = lp.id_ski
            WHERE id_utilisateur=%s 
    '''
    mycursor.execute(sql, (id_client))
    articles_panier = mycursor.fetchall()

    if len(articles_panier) >= 1:
        sql = ''' SELECT SUM(prix_ski*quantite) as prix
                  FROM ski
                  INNER JOIN ligne_panier lp on ski.id_ski = lp.id_ski
                  WHERE id_utilisateur=%s '''
        mycursor.execute(sql, id_client)
        prix_total = mycursor.fetchone()
    else:
        prix_total = None
    # etape 2 : selection des adresses
    return render_template('client/boutique/panier_validation_adresses.html'
                           #, adresses=adresses
                           , articles_panier=articles_panier
                           , prix_total= prix_total
                           , validation=1
                           )

@client_commande.route('/client/commande/add', methods=['POST'])
def client_commande_add():
    mycursor = get_db().cursor()

    # choix de(s) (l')adresse(s)

    id_client = session['id_user']
    sql = '''SELECT * FROM ligne_panier WHERE id_utilisateur=%s '''
    mycursor.execute(sql, id_client)
    items_ligne_panier = mycursor.fetchall()
    if items_ligne_panier is None or len(items_ligne_panier) < 1:
        flash(u'Pas d\'articles dans le ligne_panier', 'alert-warning')
        return redirect(url_for('client_index'))
                                           # https://pynative.com/python-mysql-transaction-management-using-commit-rollback/
    #a = datetime.strptime('my date', "%b %d %Y %H:%M")
    date_commande = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    tuple_insert = (date_commande,id_client,'1')
    sql = ''' INSERT INTO commande(date_achat,id_utilisateur,id_etat) VALUES (%s,%s,%s)'''
    mycursor.execute(sql, tuple_insert)
    sql = '''SELECT last_insert_id() as last_insert_id'''
    mycursor.execute(sql)
    commande_id = mycursor.fetchone()
    print(commande_id, tuple_insert)
    # numéro de la dernière commande

    for item in items_ligne_panier:
        sql = ''' DELETE FROM ligne_panier WHERE id_utilisateur=%s AND id_ski=%s '''
        mycursor.execute(sql,(item['id_utilisateur'], item['id_ski']))
        sql = '''  SELECT prix_ski AS prix FROM ski WHERE id_ski=%s'''
        mycursor.execute(sql, item['id_ski'])
        prix = mycursor.fetchone()
        print(prix)
        sql = ''' INSERT INTO ligne_commande(id_commande,id_ski,prix,quantite) VALUES (%s,%s,%s,%s)'''
        tuple_insert = (commande_id['last_insert_id'], item['id_ski'], prix['prix'], item['quantite'])
        print(tuple_insert)
        mycursor.execute(sql, tuple_insert)
    get_db().commit()
    flash(u'Commande ajoutée','alert-success')
    return redirect('/client/article/show')




@client_commande.route('/client/commande/show', methods=['get','post'])
def client_commande_show():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    sql = '''  SELECT commande.id_commande,date_achat , SUM(quantite) AS nbr_articles, SUM(quantite*prix) AS prix_total,
     e.id_etat AS etat_id,libelle
               FROM commande
               INNER JOIN ligne_commande lc on commande.id_commande = lc.id_commande 
               INNER JOIN etat e on commande.id_etat = e.id_etat
               WHERE id_utilisateur=%s
               GROUP BY commande.id_commande, date_achat,  e.id_etat
               ORDER BY etat_id,date_achat; '''
    mycursor.execute(sql, (id_client,))
    commandes = mycursor.fetchall()

    articles_commande = None
    commande_adresses = None
    id_commande = request.args.get('id_commande', None)
    if id_commande != None:
        print(id_commande)
        sql = ''' SELECT libelle_ski AS nom ,quantite,prix AS prix ,SUM(prix*ligne_commande.quantite) AS prix_ligne
                  FROM ligne_commande
                  INNER JOIN ski s on ligne_commande.id_ski = s.id_ski
                  WHERE id_commande=%s
                  GROUP BY s.id_ski; '''
        mycursor.execute(sql,(id_commande,))
        articles_commande = mycursor.fetchall()

        # partie 2 : selection de l'adresse de livraison et de facturation de la commande selectionnée
        sql = ''' selection des adressses '''

    return render_template('client/commandes/show.html'
                           , commandes=commandes
                           , articles_commande=articles_commande
                           , commande_adresses=commande_adresses
                           )

