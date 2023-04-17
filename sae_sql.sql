DROP TABLE IF EXISTS liste_envie;
DROP TABLE IF EXISTS historique;
DROP TABLE IF EXISTS commentaire;
DROP TABLE IF EXISTS note;
DROP TABLE IF EXISTS ligne_panier;
DROP TABLE IF EXISTS ligne_commande;
DROP TABLE IF EXISTS declinaison_ski;
DROP TABLE IF EXISTS ski;
DROP TABLE IF EXISTS commande;
DROP TABLE IF EXISTS date_consultation;
DROP TABLE IF EXISTS date_update;
DROP TABLE IF EXISTS date_commentaire;
DROP TABLE IF EXISTS adresse;
DROP TABLE IF EXISTS niveau_ski;
DROP TABLE IF EXISTS longueur;
DROP TABLE IF EXISTS type_ski;
DROP TABLE IF EXISTS etat;
DROP TABLE IF EXISTS utilisateur;


CREATE TABLE utilisateur (
    id_utilisateur INT AUTO_INCREMENT PRIMARY KEY,
    login VARCHAR(255),
    email VARCHAR(255),
    password VARCHAR(255),
    role VARCHAR(255),
    nom VARCHAR(255),
    est_actif TINYINT(1)
);

INSERT INTO utilisateur(id_utilisateur, login, email,
                        password,
                        role, nom, est_actif)
VALUES (1, 'admin', 'admin@admin.fr','sha256$dPL3oH9ug1wjJqva$2b341da75a4257607c841eb0dbbacb76e780f4015f0499bb1a164de2a893fdbf','ROLE_admin', 'admin', '1'),
       (2, 'client', 'client@client.fr','sha256$1GAmexw1DkXqlTKK$31d359e9adeea1154f24491edaa55000ee248f290b49b7420ced542c1bf4cf7d','ROLE_client', 'client', '1'),
       (3, 'client2', 'client2@client2.fr','sha256$MjhdGuDELhI82lKY$2161be4a68a9f236a27781a7f981a531d11fdc50e4112d912a7754de2dfa0422','ROLE_client', 'client2', '1');

SELECT * FROM utilisateur;

CREATE TABLE etat(
   id_etat INT AUTO_INCREMENT,
   libelle VARCHAR(255),
   PRIMARY KEY(id_etat)
);

CREATE TABLE type_ski(
   id_type_ski INT AUTO_INCREMENT,
   libelle_type_ski VARCHAR(255),
   PRIMARY KEY(id_type_ski)
);

CREATE TABLE longueur(
   id_longueur_ski INT AUTO_INCREMENT,
   longueur_ski INT,
   PRIMARY KEY(id_longueur_ski)
);

CREATE TABLE niveau_ski(
   id_niveau INT AUTO_INCREMENT,
   libelle_niveau VARCHAR(255),
   PRIMARY KEY(id_niveau)
);

CREATE TABLE adresse(
   id_adresse INT AUTO_INCREMENT,
   nom VARCHAR(255),
   rue VARCHAR(255),
   code_postal INT,
   ville VARCHAR(255),
   date_utilisation DATE,
   id_utilisateur INT NOT NULL,
   PRIMARY KEY(id_adresse),
   FOREIGN KEY(id_utilisateur) REFERENCES utilisateur(id_utilisateur)
);

CREATE TABLE date_commentaire(
   date_publication DATE,
   PRIMARY KEY(date_publication)
);

CREATE TABLE date_update(
   date_update DATE,
   PRIMARY KEY(date_update)
);

CREATE TABLE date_consultation(
   date_consultation DATE,
   PRIMARY KEY(date_consultation)
);

CREATE TABLE commande(
   id_commande INT AUTO_INCREMENT,
   date_achat DATE,
   id_adresse INT,
   id_adresse_1 INT,
   id_etat INT NOT NULL,
   id_utilisateur INT NOT NULL,
   PRIMARY KEY(id_commande),
   FOREIGN KEY(id_adresse) REFERENCES adresse(id_adresse),
   FOREIGN KEY(id_adresse_1) REFERENCES adresse(id_adresse),
   FOREIGN KEY(id_etat) REFERENCES etat(id_etat),
   FOREIGN KEY(id_utilisateur) REFERENCES utilisateur(id_utilisateur)
);

CREATE TABLE ski(
   id_ski INT AUTO_INCREMENT,
   libelle_ski VARCHAR(255),
   prix_ski INT,
   image VARCHAR(255),
   description VARCHAR(255),
   id_niveau INT,
   id_type_ski INT NOT NULL,
   PRIMARY KEY(id_ski),
   FOREIGN KEY(id_niveau) REFERENCES niveau_ski(id_niveau),
   FOREIGN KEY(id_type_ski) REFERENCES type_ski(id_type_ski)
);

CREATE TABLE declinaison_ski(
   id_declinaison_ski INT AUTO_INCREMENT,
   stock INT,
   prix_declinaison INT,
   image VARCHAR(255),
   id_longueur_ski INT NOT NULL,
   id_ski INT NOT NULL,
   PRIMARY KEY(id_declinaison_ski),
   FOREIGN KEY(id_longueur_ski) REFERENCES longueur(id_longueur_ski),
   FOREIGN KEY(id_ski) REFERENCES ski(id_ski)
);

CREATE TABLE ligne_commande(
   id_commande INT,
   id_declinaison_ski INT NOT NULL ,
   prix INT NOT NULL,
   quantite INT NOT NULL,
   PRIMARY KEY(id_commande, id_declinaison_ski),
   FOREIGN KEY(id_commande) REFERENCES commande(id_commande),
   FOREIGN KEY(id_declinaison_ski) REFERENCES declinaison_ski(id_declinaison_ski)
);


CREATE TABLE ligne_panier(
   id_utilisateur INT,
   id_declinaison_ski INT,
   quantite INT,
   date_ajout DATE,
   PRIMARY KEY(id_utilisateur, id_declinaison_ski),
   FOREIGN KEY(id_utilisateur) REFERENCES utilisateur(id_utilisateur),
   FOREIGN KEY(id_declinaison_ski) REFERENCES declinaison_ski(id_declinaison_ski)
);

CREATE TABLE note(
   id_utilisateur INT,
   id_ski INT,
   note INT,
   PRIMARY KEY(id_utilisateur, id_ski),
   FOREIGN KEY(id_utilisateur) REFERENCES utilisateur(id_utilisateur),
   FOREIGN KEY(id_ski) REFERENCES ski(id_ski)
);

CREATE TABLE commentaire(
   id_utilisateur INT,
   id_ski INT,
   date_publication DATE,
   commentaire VARCHAR(255),
   valider BOOLEAN,
   PRIMARY KEY(id_utilisateur, id_ski, date_publication),
   FOREIGN KEY(id_utilisateur) REFERENCES utilisateur(id_utilisateur),
   FOREIGN KEY(id_ski) REFERENCES ski(id_ski),
   FOREIGN KEY(date_publication) REFERENCES date_commentaire(date_publication)
);

CREATE TABLE historique(
   id_utilisateur INT,
   id_ski INT,
   date_consultation DATE,
   PRIMARY KEY(id_utilisateur, id_ski, date_consultation),
   FOREIGN KEY(id_utilisateur) REFERENCES utilisateur(id_utilisateur),
   FOREIGN KEY(id_ski) REFERENCES ski(id_ski),
   FOREIGN KEY(date_consultation) REFERENCES date_consultation(date_consultation)
);

CREATE TABLE liste_envie(
   id_utilisateur INT,
   id_ski INT,
   date_update DATE,
   PRIMARY KEY(id_utilisateur, id_ski, date_update),
   FOREIGN KEY(id_utilisateur) REFERENCES utilisateur(id_utilisateur),
   FOREIGN KEY(id_ski) REFERENCES ski(id_ski),
   FOREIGN KEY(date_update) REFERENCES date_update(date_update)
);

INSERT INTO type_ski (libelle_type_ski) VALUES
        ('PISTE'),
        ('ALL-MOUNTAIN'),
        ('FREERIDE'),
        ('FREESTYLE');

SELECT * FROM type_ski;

INSERT INTO longueur (longueur_ski) VALUES
        (70),
        (80),
        (92),
        (136),
        (138),
        (142),
        (146),
        (149),
        (153),
        (160),
        (162),
        (164),
        (167),
        (172),
        (176),
        (178),
        (181),
        (185);

SELECT * FROM longueur;

INSERT INTO niveau_ski (libelle_niveau) VALUES
        ('DEBUTANT'),
        ('INTERMEDIARE'),
        ('CONFIRME');

SELECT * FROM niveau_ski;

INSERT INTO ski (libelle_ski, prix_ski, image, description, id_niveau, id_type_ski) VALUES
        ('BLACKOPS W92 OPEN ', 375.0, 'BLACKOPS.png','très bon ski', 2, 3),
        ('ESCAPER 87 OPEN', 520.0,  'ESCAPER.png','très bon ski', 2,  2),
        ('EXPERIENCE 78 CARBON (XPRESS)', 430.0,  'EXPERIENCE_78.png','très bon ski', 2, 2),
        ('EXPERIENCE 86 BASALT (KONECT)', 740.0, 'EXPERIENCE_86.png','très bon ski', 2,  2),
        ('ENFANT EXPERIENCE Pro (Team 4GW)', 130.0,  'EXPERIENCE_PRO.png','très bon ski', 2, 2),
        ('FREESTYLE TRIXIE', 299.0, 'TRIXIE.png','très bon ski',  2, 4),
        ('NOVA 10 TI (XPRESS) ', 675.0, 'NOVA_10_TI.png','très bon ski',  2,  1),
        ('QST 98 ', 600.0, 'QST_98.png', 'très bon ski', 2,  3),
        ('QST BLANK TEAM', 350.0, 'QST_BLANK_TEAM.png','très bon ski',  2,  3),
        ('S FORCE Ti.80 PRO', 850.0, 'FORCE_Ti_80_PRO.png', 'très bon ski', 2,  1),
        ('S MAX N°6 XT (and M10)', 450.0, 'MAX_XT.png','très bon ski',  1,  1),
        ('SENDER 104 T1 OPEN', 740.0,'SENDER_104_TI_OPEN.png','très bon ski',  3,  3),
        ('Signature PALMARES (KONECT) ', 780.0, 'SIGNATURE_PALMARES.png','très bon ski',  2,  1),
        ('SIGNATURE ROC 550 (XPRESS) ', 540.0,  'SIGNATURE_ROC_550.png','très bon ski',  2,  1),
        ('STRATO EDITION (Konect)', 1195.0, 'SIGNATURE_STRATO.png', 'très bon ski', 3,  1);

SELECT * FROM ski;

INSERT INTO etat (libelle) VALUES
        ('en cours de traitement'),
        ('expédié');

INSERT INTO declinaison_ski (stock, prix_declinaison, image, id_longueur_ski, id_ski) VALUES
        (4,375.0,'BLACKOPS.png',4,1),
        (8,375.0,'BLACKOPS.png',5,1),
        (5,520.0,'ESCAPER 87 OPEN',9,2),
        (2,430.0,'EXPERIENCE_78.png',5,3),
        (2,740.0,'EXPERIENCE_86.png',8,4),
        (9,130.0,'EXPERIENCE_PRO.png',1,5),
        (4,299.0,'TRIXIE.png',5,6),
        (3,675.0,'NOVA_10_TI.png',9,7),
        (1,600.0,'QST_98.png',12,8),
        (6,350.0,'QST_BLANK_TEAM.png',14,9),
        (2,850.0,'FORCE_Ti_80_PRO.png',18,10),
        (5,450.0,'MAX_XT.png',7,11),
        (2,740.0,'SENDER_104_TI_OPEN.png',12,12),
        (3,780.0,'SIGNATURE_PALMARES.png',8,13),
        (3,540.0,'SIGNATURE_ROC_550.png',6,14),
        (5,1195.0,'SIGNATURE_STRATO.png',11,15);

INSERT INTO commande(id_commande, date_achat, id_etat, id_utilisateur) VALUES
    (1,'2023-03-23',1,2),
    (2,'2023-03-23',1,2),
    (3,'2023-03-23',1,2),
    (4,'2023-03-23',1,3);


INSERT INTO ligne_commande(id_commande, id_declinaison_ski, prix, quantite) VALUES
    (1,2,375,1),
    (1,4,375,1),
    (2,7,299,1),
    (3,12,450,1),
    (4,1,375,1),
    (4,6,130,1),
    (4,13,740,1);

SELECT utilisateur.nom, SUM(prix * quantite) as total_lignes_commande
FROM utilisateur
JOIN commande ON utilisateur.id_utilisateur = commande.id_utilisateur
JOIN ligne_commande ON commande.id_commande = ligne_commande.id_commande
GROUP BY nom
LIMIT 3;

