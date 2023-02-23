DROP TABLE IF EXISTS ligne_panier;
DROP TABLE IF EXISTS ligne_commande;
DROP TABLE IF EXISTS ski;
DROP TABLE IF EXISTS commande;
DROP TABLE IF EXISTS niveau_ski;
DROP TABLE IF EXISTS taille_ski;
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

CREATE TABLE taille_ski(
   id_taille_ski INT AUTO_INCREMENT,
   taille_ski INT,
   PRIMARY KEY(id_taille_ski)
);

CREATE TABLE niveau_ski(
   id_niveau INT AUTO_INCREMENT,
   libelle_niveau VARCHAR(255),
   PRIMARY KEY(id_niveau)
);

CREATE TABLE commande(
   id_commande INT AUTO_INCREMENT,
   date_achat DATE,
   id_etat INT NOT NULL,
   id_utilisateur INT NOT NULL,
   PRIMARY KEY(id_commande),
   FOREIGN KEY(id_etat) REFERENCES etat(id_etat),
   FOREIGN KEY(id_utilisateur) REFERENCES utilisateur(id_utilisateur)
);

CREATE TABLE ski(
   id_ski INT AUTO_INCREMENT,
   libelle_ski VARCHAR(255),
   prix_ski NUMERIC(6,2),
   stock INT,
   image VARCHAR(255),
   description VARCHAR(255),
   id_niveau INT NOT NULL,
   id_taille_ski INT NOT NULL,
   id_type_ski INT NOT NULL,
   PRIMARY KEY(id_ski),
   FOREIGN KEY(id_niveau) REFERENCES niveau_ski(id_niveau),
   FOREIGN KEY(id_taille_ski) REFERENCES taille_ski(id_taille_ski),
   FOREIGN KEY(id_type_ski) REFERENCES type_ski(id_type_ski)
);

CREATE TABLE ligne_commande(
   id_commande INT,
   id_ski INT,
   prix DECIMAL(10,2),
   quantite INT,
   PRIMARY KEY(id_commande, id_ski),
   FOREIGN KEY(id_commande) REFERENCES commande(id_commande),
   FOREIGN KEY(id_ski) REFERENCES ski(id_ski)
);

CREATE TABLE ligne_panier(
   id_utilisateur INT,
   id_ski INT,
   JJ_MM_AAAA DATE,
   quantite INT,
   date_ajout DATE,
   PRIMARY KEY(id_utilisateur, id_ski),
   FOREIGN KEY(id_utilisateur) REFERENCES utilisateur(id_utilisateur),
   FOREIGN KEY(id_ski) REFERENCES ski(id_ski)
);


INSERT INTO type_ski (libelle_type_ski) VALUES
        ('PISTE'),
        ('ALL-MOUNTAIN'),
        ('FREERIDE'),
        ('FREESTYLE');

SELECT * FROM type_ski;

INSERT INTO taille_ski (taille_ski) VALUES
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

SELECT * FROM taille_ski;

INSERT INTO niveau_ski (libelle_niveau) VALUES
        ('DEBUTANT'),
        ('INTERMEDIARE'),
        ('CONFIRME');

SELECT *FROM niveau_ski;

INSERT INTO ski (libelle_ski, prix_ski, stock, image,description, id_niveau, id_taille_ski, id_type_ski) VALUES
        ('BLACKOPS W92 OPEN ', 375.0, 4, 'BLACKOPS.png','très bon ski', 2, 4, 3),
        ('ESCAPER 87 OPEN', 520.0, 5, 'ESCAPER.png','très bon ski', 2, 9, 2),
        ('EXPERIENCE 78 CARBON (XPRESS)', 430.0, 2, 'EXPERIENCE_78.png','très bon ski', 2, 5, 2),
        ('EXPERIENCE 86 BASALT (KONECT)', 740.0, 2, 'EXPERIENCE_86.png','très bon ski', 2, 8, 2),
        ('ENFANT EXPERIENCE Pro (Team 4GW)', 130.0, 9, 'EXPERIENCE_PRO.png','très bon ski', 2, 1, 2),
        ('FREESTYLE TRIXIE', 299.0, 4, 'TRIXIE.png','très bon ski',  2, 5, 4),
        ('NOVA 10 TI (XPRESS) ', 675.0, 3, 'NOVA_10_TI.png','très bon ski',  2, 9, 1),
        ('QST 98 ', 600.0, 1, 'QST_98.png', 'très bon ski', 2, 12, 3),
        ('QST BLANK TEAM', 350.0, 6, 'QST_BLANK_TEAM.png','très bon ski',  2, 14, 3),
        ('S FORCE Ti.80 PRO', 850.0, 2, 'FORCE_Ti_80_PRO.png', 'très bon ski', 2, 18, 1),
        ('S MAX N°6 XT (and M10)', 450.0, 5, 'MAX_XT.png','très bon ski',  1, 7, 1),
        ('SENDER 104 T1 OPEN', 740.0, 2, 'SENDER_104_TI_OPEN.png','très bon ski',  3, 12, 3),
        ('Signature PALMARES (KONECT) ', 780.0, 3, 'SIGNATURE_PALMARES.png','très bon ski',  2, 8, 1),
        ('SIGNATURE ROC 550 (XPRESS) ', 540.0, 3, 'SIGNATURE_ROC_550.png','très bon ski',  2, 6, 1),
        ('STRATO EDITION (Konect)', 1195.0, 5, 'SIGNATURE_STRATO.png', 'très bon ski', 3, 11, 1);

INSERT INTO etat (libelle) VALUES
        ('en cours de traitement'),
        ('expédié');

INSERT INTO commande (date_achat, id_etat, id_utilisateur) VALUES
        ('2018-09-2',1,3),
        ('2021-09-2',2,3);

INSERT INTO ligne_commande (id_commande,id_ski,prix,quantite) VALUES
        (1,1,750,2),
        (1,3,750,2),
        (2,2,1125,3);

SELECT *
FROM ligne_panier
WHERE id_utilisateur=2 AND id_ski=1;

DELETE FROM ligne_panier WHERE id_utilisateur=2 AND id_ski=1;
