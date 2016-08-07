# -*- coding: utf-8 -*-

import glob  
import os
import string
import sys

try:
    os.path.getsize("arbow_d.py")
except:
    print "Le fichier arbow_d.py est nécessaire!"
    exit("0")
#os.system("echo a")
os.system("python arbow_d.py -o arbow_s.txt -c \"{}\"".format(os.getcwd()))

class fichier:
    def __init__(self, adresse = "", nom = "", taille = 0, md5=0):
        self.adresse = adresse
        self.nom = nom
        self.md5 = md5
        self.taille = taille
        self.liste = 1
        
    def __eq__(self, fich2):
        return self.taille == fich2.taille and self.md5 == fich2.md5
    
    def __gt__(self, fich2):
        if self.taille == fich2.taille:
            return self.md5 > fich2.md5
        else:
            return self.taille > fich2.taille
        
    def __ge__(self, fich2):
        if self.taille == fich2.taille:
            return self.md5 >= fich2.md5
        else:
            return self.taille > fich2.taille
        
    def __lt__(self, fich2):
        if self.taille == fich2.taille:
            return self.md5 < fich2.md5
        else:
            return self.taille < fich2.taille
        
    def __le__(self, fich2):
        if self.taille == fich2.taille:
            return self.md5 <= fich2.md5
        else:
            return self.taille < fich2.taille
        
    def compareNom(self, fich2):
        if "win" in sys.platform.lower():                   # Potentielle faiblesse (due aux différents OS...): La casse n'est prise en compte QUE sous Linux
            if self.adresse.lower()+self.nom.lower() == fich2.adresse.lower()+fich2.nom.lower():
                return 0
            elif self.adresse.lower()+self.nom.lower() > fich2.adresse.lower()+fich2.nom.lower():
                return 1
            else:
                return -1
        else:
            if self.adresse+self.nom == fich2.adresse.lower()+fich2.nom:
                return 0
            elif self.adresse+self.nom > fich2.adresse+fich2.nom:
                return 1
            else:
                return -1

class action:
    def __init__(self, commande, source, destination):
        self.commande = commande
        self.source = source
        self.destination = destination
    def nom(self):
        tab_action = ["Suppression", "Deplacement", "Copie distante", "Copie locale"]
        if self.commande == 0:
            return "Supression de {}".format(self.source.adresse+self.source.nom)
        else:
            return "{} de {} vers {}".format(tab_action[self.commande],self.source.adresse+self.source.nom,self.destination.adresse+self.destination.nom)
    def __eq__(self, action2):
        return self.commande == action2.commande
    def __lt__(self, action2):
        return self.commande < action2.commande
    
def tri(l):
    for i in xrange(len(l)-1):
        mini=i
        lmini = l[i]
        for j in xrange(i+1,len(l)):
            if l[j]<lmini:
                mini=j
                lmini = l[j]
        l[mini], l[i] = l[i], lmini

def format_taille(taille):
    i = 1
    L = ['', 'K', 'M', 'G', 'T', 'P']
    while (taille > 1024.):
        i+=1
        taille /= 1024.
    return string.join(("{0:.2f}".format(taille),L[i-1]+"o"))


def lire_arguments(argv):
    if "win" in sys.platform.lower():
        output = os.getcwd()+"\\output.txt"
    else:
        output = os.getcwd()+"/output.txt"
    fichier1 = "arbow_s.txt"
    fichier2 = "arbow_d.txt"
    global verbose
    if "-v" in argv or "--verbose" in argv:
        verbose = True
    i = 0
    while i < len(argv) - 1:
        if argv[i] == "-s" or argv[i] == "--source":
            fichier1 = argv[i+1]
        elif argv[i] == "-d" or argv[i] == "--destination":
            fichier2 = argv[i+1]
        elif argv[i] == "-o" or argv[i] == "--output":
            output = chemin_abs(argv[i+1])
        elif argv[i+1] == "-h" or argv[i+1] == "--help" or argv[i] == "-h" or argv[i] == "--help":
            print "Utilisation: py arbo.py [-s/--source fichier source] [-d/--destination fichier destination] [-o/--output fichier de sortie] [-v/--verbose]"
            exit(0)
        i+=1
    return (output, fichier1, fichier2)

def chemin_abs(chemin):
    #Permet de transformer les chemins relatifs en absolus, quel que soit l'OS.
    if not ":" in chemin and "win" in sys.platform.lower():
        chemin = os.getcwd() + "\\" + chemin
    elif chemin[0] != "/" and not "win" in sys.platform.lower():
        chemin = os.getcwd() + "/" + chemin
    return chemin


def mirroir(liste):
    global verbose
    groupe1 = []
    groupe2 = []
    listeAction = []
    for fich in liste:
        if  groupe1 + groupe2 == [] or fich == (groupe1 + groupe2)[0]: # si identique au précédent
            if fich.liste == 1:
                groupe1.append(fich)
            else:
                groupe2.append(fich)
        if not (groupe1 + groupe2 == [] or fich == (groupe1 + groupe2)[0]) or (fich == liste[len(liste)-1] and fich.compareNom(liste[len(liste)-1]) == 0): #Sinon (fichier different) OU si dernier fichier...
            if verbose:
                
                print "Groupe de {} fichiers trouvé:\n".format(len(groupe1+groupe2))
                print "Groupe 1:"
                for i in groupe1:
                    print "{}{}".format(i.adresse,i.nom,i.liste)
                print "Groupe 2:"
                for i in groupe2:
                    print "{}{}".format(i.adresse,i.nom,i.liste)               
            if groupe1 == []:
                if verbose:  
                    print "Pas de groupe 1! On supprime le groupe 2"
                for j in groupe2:
                    listeAction.append(action(0,j,0))
            elif groupe2 == []:
                if verbose:
                    print "Pas de groupe 2! On copie tout depuis groupe 1"
                for j in groupe1:
                    listeAction.append(action(2,j,j))
            else:
                paire1 = []
                paire2 = []
                for i in range(0,len(groupe1)):
                    for j in range(0,len(groupe2)):
                        if groupe1[i].compareNom(groupe2[j]) == 0:
                            paire1.append(i)
                            paire2.append(j)
                #print "restants sur liste1: {}".format(len(groupe1)-len(paire1))
                #print "restants sur liste2: {}".format(len(groupe2)-len(paire1))
                if len(groupe2)-len(paire1) == 0 and len(groupe1)-len(paire1) == 0:  #Tout est apairé: il ne reste plus rien à traiter
                    if verbose:
                        print "Fin du traitement du groupe"
                elif len(groupe1)-len(paire1) == 0:  #Si il ne reste plus de fichiers non apairés sur la source, mais il en reste sur destination: a supprimer
                    for i in range(0,len(groupe2)):
                        if i not in paire2:
                            listeAction.append(action(0,groupe2[i],0))
                            if verbose:
                                print "On supprime {}".format(groupe2[i].adresse+groupe2[i].nom)
                elif len(groupe1) == len(groupe2):  #Si il y a le bon nombre de fichiers mais pas au bon endroit: il faut encore en déplacer (ceux qui ne sont pas apairés)
                    j = 0
                    for i in range(0,len(groupe2)):
                        if i not in paire2:
                            while j in paire1:
                                j += 1
                            listeAction.append(action(1,groupe2[i],groupe1[j]))
                            if verbose:
                                print "On déplace {} vers {}.".format(groupe2[i].adresse+groupe2[i].nom,groupe1[j].adresse+groupe1[j].nom)
                            j+=1
                elif len(groupe2)-len(paire1) == 0:  #Si tout est apairé sur la destination mais qu'il en reste sur la source:
                    for i in range(0,len(groupe1)):
                        if i not in paire1:
                            listeAction.append(action(3,groupe2[paire2[0]],groupe1[i]))
                            if verbose:
                                print "On copie (en local) {} vers {}.".format(groupe2[paire2[0]].adresse+groupe2[paire2[0]].nom,groupe1[i].adresse+groupe1[i].nom)
                            j+=1
                elif len(paire1) != 0: #Si il reste des fichiers non apairés des 2 côtés mais il existe une paire (et le nombre est different)
                    if len(groupe1) > len(groupe2): #Si il y a plus de fichiers sur la source
                        j = 0
                        for i in range(0,len(groupe2)): #On commence par deplacer les mal placés
                            if i not in paire2:
                                while j in paire1:
                                    j += 1
                                listeAction.append(action(1,groupe2[i],groupe1[j]))
                                if verbose:
                                    print "On déplace {} vers {}.".format(groupe2[i].adresse+groupe2[i].nom,groupe1[j].adresse+groupe1[j].nom)
                                j+=1
                        while j < len(groupe1):         #Puis on copie ceux qui restent à partir d'un fichier déjà bien placé
                            if j not in paire1:
                                listeAction.append(action(3,groupe2[paire2[0]],groupe1[i]))
                                if verbose:
                                    print "On copie (en local) {} vers {}.".format(groupe2[paire2[0]].adresse+groupe2[paire2[0]].nom,groupe1[i].adresse+groupe1[i].nom)
                            j+=1
                    else:   #Sinon: Il y a plus de fichiers sur la destination
                        i = 0
                        j = 0
                        while i < len(groupe1): #On déplace les premiers mal placés
                            if i not in paire1:
                                while j in paire2:
                                    j += 1
                                listeAction.append(action(1,groupe2[j],groupe1[i]))
                                if verbose:
                                    print "On déplace {} vers {}.".format(groupe2[j].adresse+groupe2[j].nom,groupe1[i].adresse+groupe1[i].nom)
                                j+=1
                            i+=1
                        for i in range(j,len(groupe2)):# Puis on supprime les autres
                            if  i not in paire2:
                                listeAction.append(action(0,groupe2[i],0))
                                if verbose:
                                    print "On supprime {}".format(groupe2[i].adresse+groupe2[i].nom)
                else: #Si il existe plusieurs fichiers de chaque côté, mais pas une seule paire
                    if len(groupe1) > len(groupe2): #Si il y a plus de fichiers sur la source
                        for i in range(0,len(groupe2)): #On commence par deplacer les mal placés
                                listeAction.append(action(1,groupe2[i],groupe1[i]))
                                if verbose:
                                    print "On déplace {} vers {}.".format(groupe2[i].adresse+groupe2[i].nom,groupe1[i].adresse+groupe1[i].nom)
                        for i in range(len(groupe2),len(groupe1)):        #Puis on copie ceux qui restent à partir d'un fichier déjà bien placé (le premier déplacé précédemment)
                                listeAction.append(action(3,groupe1[0],groupe1[i]))
                                if verbose:
                                    print "On copie (en local) {} vers {}.".format(groupe1[0].adresse+groupe1[0].nom,groupe1[i].adresse+groupe1[i].nom)
                    else:   #Sinon: Il y a plus de fichiers sur la destination
                        for i in range(0,len(groupe1)): #On déplace les premiers mal placés
                                listeAction.append(action(1,groupe2[i],groupe1[i]))
                                if verbose:
                                    print "On déplace {} vers {}.".format(groupe2[i].adresse+groupe2[i].nom,groupe1[i].adresse+groupe1[i].nom)
                        for i in range(len(groupe1),len(groupe2)): #Puis on supprime les autres
                                listeAction.append(action(0,groupe2[i],0))
                                if verbose:
                                    print "On supprime {}".format(groupe2[i].adresse+groupe2[i].nom)                                  
            groupe1 = []
            groupe2 = []
            if fich.liste == 1:
                groupe1.append(fich)
            else:
                groupe2.append(fich)
            if verbose:
                print "--------------\n"
    return listeAction

verbose = False
(output, fichier1, fichier2) = lire_arguments(sys.argv)
if verbose:
    print "Fichier source: {}".format(fichier1)
    print "Fichier destination: {}".format(fichier2)
    print "Fichier sortie: {}".format(output)

fich1 = open(fichier1,"r")
fich2 = open(fichier2,"r")
Lfich1 = string.split(fich1.read(),"\x0a")
Lfich2 = string.split(fich2.read(),"\x0a")
os_source = Lfich1[0]
Lfich1 = Lfich1[1:]
Lfich2 = Lfich2[1:]
fich1.close()
fich2.close()

del Lfich1[len(Lfich1) - 1]
del Lfich2[len(Lfich2) - 1]


liste1 = []
liste2 = []

for L in Lfich1:
    SplitedLine = string.split(L,",")
    fich = fichier()
    fich.taille = int(SplitedLine[0])
    del SplitedLine[0]
    Line = ",".join(SplitedLine)
    fich.md5 = Line[0:32]
    Line = Line[33:]
    chemin = string.split(Line,"\\")
    fich.nom = chemin[len(chemin)-1]
    del chemin[len(chemin)-1]
    fich.adresse = string.join(chemin,"\\")+"\\"
    liste1.append(fich)
if verbose:
    print("Chargement du fichier 1 terminé, total: {} fichiers.".format(len(Lfich1)))
for L in Lfich2:
    SplitedLine = string.split(L,",")
    fich = fichier()
    fich.taille = int(SplitedLine[0])
    del SplitedLine[0]
    Line = ",".join(SplitedLine)
    fich.md5 = Line[0:32]
    Line = Line[33:]
    chemin = string.split(Line,"\\")
    fich.nom = chemin[len(chemin)-1]
    del chemin[len(chemin)-1]
    fich.adresse = string.join(chemin,"\\")+"\\"
    fich.liste = 2
    liste2.append(fich)
if verbose:
    print("Chargement du fichier 2 terminé, total: {} fichiers.".format(len(Lfich2)))
    print "Réunion des listes..."
liste = liste1 + liste2
if verbose:
    print "Tri de la liste..."
tri(liste)
if verbose:
    print "Traitement de la liste..."
listeAction = mirroir(liste)
if verbose:
    print "Tri de la liste d'actions"
tri(listeAction)
dossier = "arbow"
copDist = False
if os_source == "w":
    script = open("script.bat","w")
    script.write("@echo off\n")
    for i in listeAction:
        if i.commande == 0:
            script.write("del \".{}\"\n".format(i.source.adresse+i.source.nom))
        elif i.commande == 1:
            script.write("move \".{}\" \".{}\"\n".format(i.source.adresse+i.source.nom,i.destination.adresse+i.destination.nom))
        elif i.commande == 2:
            if not copDist:
                os.system("mkdir \".\{}\"".format(dossier))
            copDist = True
            print "copy \".{}\" \".\{}\"\n".format(i.source.adresse+i.source.nom,dossier+i.source.adresse+i.source.nom)
            os.system("mkdir \".\{}\"".format(dossier+i.source.adresse))
            os.system("copy \".{}\" \".\{}\"\n".format(i.source.adresse+i.source.nom,dossier+i.source.adresse+i.source.nom))
            if i.destination.adresse != "\\":
                script.write("mkdir \".{}\"\n".format(i.destination.adresse))
            script.write("move \".\{}\" \".{}\"\n" .format(dossier+i.source.adresse+i.source.nom,i.destination.adresse+i.destination.nom))
        elif i.commande == 3:
            if i.destination.adresse != "\\":
                script.write("mkdir \".{}\"\n".format(i.destination.adresse))
            script.write("copy \".{}\" \".{}\"\n".format(i.source.adresse+i.source.nom,i.destination.adresse+i.destination.nom))
    if copDist == True:
        script.write("rmdir /s /q .\\{}".format(dossier))
        
elif os_source == "l":
    script = open("script.sh","w")
    script.write("#!/bin/bash\n")
    for i in listeAction:
        if i.commande == 0:
            script.write("rm -f \".{}\"\n".format(i.source.adresse.replace("\\","/")+i.source.nom))
        elif i.commande == 1:
            script.write("mv \".{}\" \".{}\"\n".format(i.source.adresse.replace("\\","/")+i.source.nom,i.destination.adresse.replace("\\","/")+i.destination.nom))
        elif i.commande == 2:
            if not copDist:
                os.system("mkdir ./{}".format(dossier))
            copDist = True
            os.system("mkdir ./{}".format(dossier+i.source.adresse.replace("\\","/")))
            os.system("cp \".{}\" \"./{}\"\n".format(i.source.adresse.replace("\\","/")+i.source.nom,dossier+i.source.adresse.replace("\\","/")+i.source.nom))
            script.write("mv \"./{}\" \".{}\"\n" .format(dossier+i.source.adresse.replace("\\","/")+i.source.nom,i.destination.adresse.replace("\\","/")+i.destination.nom))
        elif i.commande == 3:
            if i.destination.adresse != "/":
                script.write("mkdir \".{}\"\n".format(i.destination.adresse.replace("\\","/")))
            script.write("cp \".{}\" \".{}\"\n".format(i.source.adresse.replace("\\","/")+i.source.nom,i.destination.adresse.replace("\\","/")+i.destination.nom))
    if copDist == True:
        script.write("rmdir ./{}".format(dossier))        
        
script.close()
