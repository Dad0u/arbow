# -*- coding: utf-8 -*-
#Ignore par défaut les fichiers *.db ! (voir fct lire_arguments)

import glob  
import os.path
import hashlib
import string
import time
import sys

class fichier:
    def __init__(self, adresse = "", nom = "", taille = 0, md5=0):
        self.adresse = adresse
        self.nom = nom
        self.md5 = md5
        self.taille = taille
        
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
    
liste = []

def md5_file(f, block_size=2**20):
    md5 = hashlib.md5()
    while True:
        data = f.read(block_size)
        if not data:
            break
        md5.update(data)
    return md5.hexdigest()

def listdirectory_win(path, taille_min, ext_i, ext_e):
    l = glob.glob(path+'\\*')
    global skipped
    for i in l:  
        if os.path.isdir(i):
            #print "Dossier: ",i
            listdirectory_win(i,taille_min, ext_i, ext_e)  
        else:
            try:
                taille = os.path.getsize(i)
            except:
                taille = -2
                print "Erreur lors de la lecture de {}".format(i)
                skipped.append(i)
            if taille >= taille_min:
                chemin = string.split(i,"\\")
                nom = chemin[len(chemin)-1]
                del chemin[len(chemin)-1]
                chemin = string.join(chemin,"\\")+"\\"
                ext = string.split(nom,".")
                if len(ext) == 1:
                    ext = "."
                else:
                    ext = ext[len(ext) - 1]
                if (ext_i != {} and ext.lower() in ext_i) or (ext_i == {} and not ext.lower() in ext_e):
                    #if (chemin,nom) != (os.getcwd()+"\\","arbow_d.py"):
                    if not (chemin+nom in (os.getcwd()+"\\arbow_d.py",os.getcwd()+"\\arbow_s.py",os.getcwd()+"\\arbow_d.txt",os.getcwd()+"\\arbow_s.txt")):
                        liste.append(fichier(chemin,nom,os.path.getsize(i)))
                    if verbose:
                        print "fichier trouvé: "
                        print "Adresse: ",chemin
                        print "Nom: ",nom
                        print "Taille: ",liste[len(liste)-1].taille," Octets"
                        print "--------------------"
                elif verbose:
                    if ext != '.':
                        print "Fichier "+i+" d'extention ."+ext
                    else:
                        print "Fichier "+i+" sans extention"
                    print "Il sera ignoré."
                    print "--------------------"
            elif verbose and taille >= 0:
                print "Fichier ", i, "de taille ", format_taille(os.path.getsize(i)), "il sera ignoré !"

def listdirectory_nux(path, taille_min, ext_i, ext_e):
    l = glob.glob(path+'/*')  
    for i in l:  
        if os.path.isdir(i):
            #print "Dossier: ",i
            listdirectory_nux(i,taille_min, ext_i, ext_e)  
        else:
            if os.path.getsize(i) >= taille_min:
                chemin = string.split(i,"/")
                nom = chemin[len(chemin)-1]
                del chemin[len(chemin)-1]
                chemin = string.join(chemin,"/")+"/"
                ext = string.split(nom,".")
                if len(ext) == 1:
                    ext = "."
                else:
                    ext = ext[len(ext) - 1]
                if (ext_i != {} and ext.lower() in ext_i) or (ext_i == {} and not ext.lower() in ext_e):
                    if not (chemin+nom in (os.getcwd()+"/arbow_d.py",os.getcwd()+"/arbow_s.py",os.getcwd()+"/arbow_d.txt",os.getcwd()+"/arbow_s.txt")):
                        liste.append(fichier(chemin,nom,os.path.getsize(i)))
                    if verbose:
                        print "fichier trouvé: "
                        print "Adresse: ",chemin
                        print "Nom: ",nom
                        print "Taille: ",liste[len(liste)-1].taille," Octets"
                        print "--------------------"
                elif verbose:
                    if ext != '.':
                        print "Fichier "+i+" d'extention ."+ext
                    else:
                        print "Fichier "+i+" sans extention"
                    print "Il sera ignoré."
                    print "--------------------"
            elif verbose:
                print "Fichier ", i, "de taille ", format_taille(os.path.getsize(i)), "il sera ignoré !"

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

def deformat_taille(taille):
    taille_dec = 0
    if len(taille) > 1:
        try:
            taille_dec = int(taille[0:len(taille)-1])
        except:
            print "Format de taille invalide"
            exit(-1)
    else:
        try:
            taille_dec = int(taille)
        except:
            print "Format de taille invalide"
            exit(-1)
    if taille[-1] == 'k' or taille[-1] == 'K':
        taille_dec *= 1024
    elif taille[-1] == 'm' or taille[-1] == 'M':
        taille_dec *= 1024**2
    elif taille[-1] == 'g' or taille[-1] == 'G':
        taille_dec *= 1024**3
    elif taille[-1] == 't' or taille[-1] == 'T':
        taille_dec *= 1024**4
    elif taille[-1] == 'p' or taille[-1] == 'P':
        taille_dec *= 1024**5
    else:
        try:
            taille_dec = int(taille)
        except:
            print "Format de taille invalide"
            exit(0)
    return taille_dec
            
def format_temps(s):
    m=int(s)/60
    h=m/60
    m-=60*h
    s-=3600*h
    s-=60*m
    if h != 0:
        return "{}h {}m {:.2f}s".format(h,m,s)
    elif m != 0:
        return "{}m {:.2f}s".format(m,s)
    else:
        return "{:.2f}s".format(s)

def barre_prog(prog, taille=30):
    chaine = "["
    i = 1
    while i < taille - 1:
        if 1.*i/taille <= prog:
            chaine = chaine+'='
        else:
            chaine = chaine+'-'
        i+=1
    chaine = chaine + "]"
    return chaine

def chemin_abs(chemin):
    #Permet de transformer les chemins relatifs en absolus, quel que soit l'OS.
    if( not ":" in chemin )and "win" in sys.platform.lower():
        chemin = os.getcwd() + "\\" + chemin
    elif chemin[0] != "/" and not "win" in sys.platform.lower():
        chemin = os.getcwd() + "/" + chemin
    return chemin

def lire_arguments(argv):
    taille_min = -1
    extensions_i = {}
    extensions_e = {"db"}                                                                         #------------Ignore par défaut les fichiers *.db !
    if "win" in sys.platform.lower():
        output = os.getcwd()+"\\arbow_d.txt"
    else:
        output = os.getcwd()+"/arbow_d.txt"
    global verbose
    chemin = os.getcwd()
    i = 0
    while i < len(argv) - 1:
        if argv[i] == "-s" or argv[i] == "--size":
            taille_min = deformat_taille(argv[i+1])
        elif argv[i] == "-ei" or argv[i] == "--extension_incluses":
            extensions_i = string.split(argv[i+1].lower(),",")
        elif argv[i] == "-ee" or argv[i] == "--extension_excluses":
            extensions_e = string.split(argv[i+1].lower(),",")
        elif argv[i] == "-o" or argv[i] == "--output":
            output = chemin_abs(argv[i+1])  
        elif argv[i] == "-c" or argv[i] == "--chemin":
            chemin = chemin_abs(argv[i+1]) 
        elif argv[i+1] == "-h" or argv[i+1] == "--help" or argv[i] == "-h" or argv[i] == "--help":
            print "Utilisation: py arbow_s.py [-s/--size Taille minimale] [-ei/--extensions_incluses ext1,ext2,...] [-ee/--extensions_excluses ext1,ext2,...] [-c/--chemin Chemin relatif ou absolu du dossier à analyser (défaut: . )] [-v/--verbose]"
            print "Pour désigner les fichiers sans extensions, utiliser .\n"
            print "Exemple: py arbo.py -s 1M -ei py,txt,.,pyc -c C:\python27"
            print "Cherche les fichiers de plus de 1 Mo, d'extension py, txt, pyc ou sans extension dans le dossier C:\python27"
            exit(0)
        if ("-v" in argv) or ("--verbose" in argv):
            verbose = True
        i+=1
    return (taille_min, extensions_i, extensions_e, verbose, chemin, output)
        
verbose = False
(taille_min, ext_i, ext_e, verbose, path, output) = lire_arguments(sys.argv)
skipped = []

if taille_min >= 0:
    print "taille mini: ", format_taille(taille_min)

if ext_i != {}:
    print "Cherche les fichiers d'extensions: "
    for j in ext_i:
        print j

if ext_e != {}:
    print "Exclue les fichiers d'extensions: "
    for j in ext_e:
        print j
print "Découverte des fichiers..."

#path = "C:\\Python27\\programmes\\Arbo\\test"
if path[len(path) - 1] == "/" or path[len(path) - 1] == "/":
    path = path[0:len(path) - 1]
if "win" in sys.platform.lower():
    skipped = []
    listdirectory_win(path, taille_min, ext_i, ext_e)
    if len(skipped) != 0:
        print "Attenion: {} fichiers sautés".format(len(skipped))
else:
    listdirectory_nux(path, taille_min, ext_i, ext_e)
for i in liste:
    i.adresse = i.adresse[len(path):len(i.adresse)]
    #print "Adresse relative: "+i.adresse
    
print "Lecture des fichiers terminée:",len(liste),"fichiers trouvés"

taille_tot = 0

for i in liste:     #Calcul de la taille totale
    taille_tot+=i.taille
print "Taille totale:",format_taille(taille_tot)
print "Génération des sommes MD5..."

j = 0
taille = 0
taille_prec = 0

t1 = time.time()-1
t0 = time.time()

for i in liste:         #Generation des sommes MD5
    j+=1
    i.md5 = md5_file(open(path+i.adresse+i.nom,"rb"))
    taille+=i.taille
    t2 = time.time()
    if t2 - t1 > 1:
        if "win" in sys.platform.lower() and not verbose:
            os.system("cls")
        elif not verbose:
            os.system("clear")
        print "{} fichiers trouvés dans {}".format(len(liste),path)
        print "Génération des sommes MD5..."
        print "Progression:"
        print("{0:.2f} %".format(100.*taille/taille_tot)+" ("+format_taille(taille)+"/"+format_taille(taille_tot)+") ("\
              +format_taille((taille-taille_prec)/(t2-t1))+"/s)")
        print barre_prog(1.*taille/taille_tot)
        if verbose:
            print "no",j,"/",len(liste)
            print "fichier: ",i.adresse+i.nom
            print "Taille: "+format_taille(i.taille)
            print "Somme MD5: ",i.md5
        print "Temps écoulé: "+format_temps((t2-t0))
        print "Temps restant: "
        print "-Moyenne: "+format_temps((t2-t0)*(taille_tot-taille)/taille)
        print "-Instantané: "+format_temps((taille_tot-taille)/(taille-taille_prec)*(t2-t1))
        t1 = t2
        taille_prec = taille

print "Génération des sommes MD5 terminée ! Tri de la liste..."
if len(skipped) != 0:
    print "Attenion: {} fichiers sautés (nom incorrect ?):".format(len(skipped))
    for i in skipped:
        print i
tri(liste)
print "Tri effectué, création du fichier récapitulatif à cette adresse: "+output

output = open(output,"wb")     #Ecriture du fichier sortie

if 'win' in sys.platform.lower():
    output.write("w\n")
    for i in liste:
        if verbose:
            print 'écriture du fichier: taille:{},Somme MD5:{} {}{}\n'.format(format_taille(i.taille),i.md5,i.adresse,i.nom).decode('cp1252').encode('utf-8')
        output.write("{},{} {}{}\x0a".format(i.taille,i.md5,i.adresse,i.nom).decode('cp1252').encode('utf-8'))
else:
    output.write("l\n")
    for i in liste:
        if verbose:
            print 'écriture du fichier: taille:{},Somme MD5:{} {}{}\n'.format(format_taille(i.taille),i.md5,i.adresse.replace("/","\\"),i.nom)
        output.write("{},{} {}{}\x0a".format(i.taille,i.md5,i.adresse.replace("/","\\"),i.nom))
output.close()
