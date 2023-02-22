#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, flash, session

from connexion_db import get_db

admin_commande = Blueprint('admin_commande', __name__,
                        template_folder='templates')

@admin_commande.route('/admin')
@admin_commande.route('/admin/commande/index')
def admin_index():
    return render_template('admin/layout_admin.html')


@admin_commande.route('/admin/commande/show', methods=['get','post'])
def admin_commande_show():
    mycursor = get_db().cursor()
    admin_id = session['id_user']
    sql = 'SELECT commande.id_commande,date_achat , sum(quantite) AS nbr_articles, sum(prix*quantite) AS prix_total, e.id_etat AS etat_id,libelle from commande '\
          'INNER JOIN ligne_commande l on commande.id_commande = l.id_commande '\
          'INNER JOIN etat e on commande.id_etat = e.id_etat '\
          'GROUP BY commande.id_commande, date_achat,quantite, e.id_etat, libelle '
    mycursor.execute(sql)
    commandes = mycursor.fetchall()
    articles_commande = None
    commande_adresses = None
    id_commande = request.args.get('id_commande', None)
    print(id_commande)
    if id_commande != None:
        print(id_commande)
        sql = ''' SELECT libelle_ski AS nom ,quantite,prix_ski AS prix ,SUM(prix*ligne_commande.quantite) AS prix_ligne
                  FROM ligne_commande
                  INNER JOIN ski s on ligne_commande.id_ski = s.id_ski
                  WHERE id_commande=%s
                  GROUP BY s.id_ski; '''
        mycursor.execute(sql,(id_commande,))
        articles_commande = mycursor.fetchall()
        commande_adresses = []
    return render_template('admin/commandes/show.html'
                           , commandes=commandes
                           , articles_commande=articles_commande
                           , commande_adresses=commande_adresses
                           )


@admin_commande.route('/admin/commande/valider', methods=['get','post'])
def admin_commande_valider():
    mycursor = get_db().cursor()
    commande_id = request.form.get('id_commande', None)
    if commande_id != None:
        print(commande_id)
        sql = 'UPDATE commande set id_etat=2 where id_commande=%s '
        mycursor.execute(sql, commande_id)
        get_db().commit()
    return redirect('/admin/commande/show')