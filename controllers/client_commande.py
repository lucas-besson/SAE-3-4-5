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
    sql = ''' SELECT s.id_ski, s.libelle_ski AS nom, lp.quantite, ds.prix_declinaison AS prix, lp.id_declinaison_ski AS id_declinaison_article, ds.stock, l.id_longueur_ski as id_taille, longueur_ski as libelle_couleur, nb_longueurs.nb_longueurs_diff AS nb_declinaison
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
    mycursor.execute(sql, (id_client))
    articles_panier = mycursor.fetchall()

    if len(articles_panier) >= 1:
        sql = ''' SELECT SUM(prix_declinaison*quantite) as prix
                  FROM declinaison_ski
                  INNER JOIN ligne_panier lp on declinaison_ski.id_declinaison_ski = lp.id_declinaison_ski
                  WHERE id_utilisateur=%s '''
        mycursor.execute(sql, id_client)
        prix_total = mycursor.fetchone()
    else:
        prix_total = None
    # etape 2 : selection des adresses
    return render_template('client/boutique/panier_validation_adresses.html'
                           # adresses=adresses
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
        sql = ''' DELETE FROM ligne_panier WHERE id_utilisateur=%s AND id_declinaison_ski=%s '''
        mycursor.execute(sql,(item['id_utilisateur'], item['id_declinaison_ski']))
        sql = '''  SELECT prix_declinaison AS prix FROM declinaison_ski WHERE id_declinaison_ski=%s'''
        mycursor.execute(sql, item['id_declinaison_ski'])
        prix = mycursor.fetchone()
        print(prix)
        sql = ''' INSERT INTO ligne_commande(id_commande,id_declinaison_ski,prix,quantite) VALUES (%s,%s,%s,%s)'''
        tuple_insert = (commande_id['last_insert_id'], item['id_declinaison_ski'], prix['prix'], item['quantite'])
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
               ORDER BY etat_id,date_achat DESC; '''
    mycursor.execute(sql, (id_client,))
    commandes = mycursor.fetchall()

    articles_commande = None
    commande_adresses = None
    id_commande = request.args.get('id_commande', None)
    if id_commande != None:
        print(id_commande)
        sql = ''' SELECT libelle_ski AS nom ,quantite,prix AS prix ,SUM(prix*ligne_commande.quantite) AS prix_ligne, l.longueur_ski as longueur, nb_longueurs.nb_longueurs_diff AS nb_declinaison
                  FROM ligne_commande
                  INNER JOIN declinaison_ski ds on ligne_commande.id_declinaison_ski = ds.id_declinaison_ski
                  INNER JOIN longueur l on ds.id_longueur_ski = l.id_longueur_ski
                  INNER JOIN ski s on ds.id_ski = s.id_ski
                  INNER JOIN (
                    SELECT ds.id_ski, COUNT(DISTINCT ds.id_longueur_ski) AS nb_longueurs_diff
                    FROM declinaison_ski ds
                    GROUP BY ds.id_ski
                    ) AS nb_longueurs ON s.id_ski = nb_longueurs.id_ski
                  WHERE id_commande= %s
                  GROUP BY libelle_ski, quantite, prix, ds.id_declinaison_ski; '''
        mycursor.execute(sql,(id_commande,))
        articles_commande = mycursor.fetchall()


        # partie 2 : selection de l'adresse de livraison et de facturation de la commande selectionnée
        sql = ''' selection des adressses '''

    return render_template('client/commandes/show.html'
                           , commandes=commandes
                           , articles_commande=articles_commande
                           , commande_adresses=commande_adresses
                           )

