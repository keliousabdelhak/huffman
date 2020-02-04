from copy import copy

# ouvrir le fichier VictorHugo.txt et le mettre dans une variable txt pour s'en servire après dans le main
txt=""
with open("VictorHugo.txt","r") as f:
	txt=f.read()

def findFrequence(txt):
	"""
	cette fonction permet  de  calculer  pour  chaque caractère du texte à compresser sa fréquence
	"""
	txt1=copy(txt)
	dico={}
	tailleTXT=len(txt)
	liste_caractere=list(set(txt)) #récuperer dans une liste tout les cararctères dans texte sans redondance grace au set  
	for i in liste_caractere:
		dico[i]=txt1.count(i)/tailleTXT #pour chaque caractère on lui calcule sa fréquence et on le rajoute au dictionnaire 
	return dico

class Noeud:
	def __init__(self,caractere,freq,gauche=None,droite=None):
		self.caractere=caractere
		self.freq=freq
		self.next={'gauche':gauche,'droite':droite}
		self.codage="" #j'ai changer la nature de cet attribut a fin d'optimiser le code est écrire le moindre possible de code  

	def getCaractere(self):
		return self.caractere

	def getfreq(self):
		return self.freq

	def getNext(self):
		return self.next

	def getCodage(self):
		return self.codage

	def __str__(self):
		tmp="caractere : {}\nfréquance : {}\nnext : {}\ncodage: {} ".format(self.getCaractere(),self.getfreq(),self.getNext(),self.getCodage())
		return tmp 

class Arbre:
	def __init__(self,dicoFreq):
		self.codes={}
		self.ListeNoeuds=[]
		self.dicoFreq=dicoFreq
		self.remplireListe() #remplire la list des noeuds  

	def remplireListe(self):
		# 1er partie remplire la liste par des noeuds crées a partir du dictionnaire des fréquances dicoFreq
		for i in self.dicoFreq:
			self.ListeNoeuds.append(Noeud(i,self.dicoFreq[i]))

		"""
		2eme partie:
		on cherche 2 nœuds ayant les fréquences les plus faibles et on les supprime de ListeNoeud.
		On crée un nouveau nœud dont la fréquence est égale à la somme des fréquences des 2 nœuds et et le caractère égale à la concaténation
		des caractères des 2 noeud. 
		On relie ce nouveau nœud aux 2 nœuds supprimés de  la liste.
		On ajoute ce nœud dans ListeNoeuds.
		"""
		while (len(self.ListeNoeuds)!=1):
			min1=self.removeNoeuds(self.ListeNoeuds.index(self.findMin()))
			min2=self.removeNoeuds(self.ListeNoeuds.index(self.findMin())) 
			car=min1.getCaractere()+min2.getCaractere()
			frq=min1.getfreq()+min2.getfreq()
			node=Noeud(car,frq,min1,min2)
			self.addNoeud(node)

	def findMin(self):
		#fonction qui return le minimum dans une liste 
		m=2 #une variable initialement plus grande que le maximum des fréquances qui est 1, elle me permet de faire la comparaison à chaque itération  
		for i in self.ListeNoeuds:
			if i.getfreq()<m:
				m=i.getfreq()
				mini=self.ListeNoeuds.index(i)
		return self.ListeNoeuds[mini]

	def removeNoeuds(self,node):
		#supprimer un noeud de la liste des noeud je me sert de pop car ça me fais moins de ligne de code 
		return self.ListeNoeuds.pop(node)

	def addNoeud(self,node):
		#ajouter un noeud à la liste des noeuds 
		self.ListeNoeuds.append(node)

	def etiquetage(self,node):
		#implémentation de l'algorithme fourni dans l'énoncé page 7

		for n in node.next:
			if node.next[n]==None:
				self.codes[node.getCaractere()]=node.getCodage()
				return
			else:
				if n=='gauche':
					node.next[n].codage=node.getCodage()+'0'
				else :
					node.next[n].codage=node.getCodage()+'1'
			self.etiquetage(node.next[n])

	def compress(self,txt):
		"""
		-dans cette fonction on parcours le texte  caractère par caractère 
		-pour chaque caractère on retire son code dans le dictionnaire codes et on le rajoute à une chaine de caractère qui est
		 initialement vide 
		"""
		x=""
		for i in txt:
			x+=self.codes[i]
		return x

	def uncompress(self,txt):
		"""
		Dans cette fonction on parcours le texts compressé (txt en argument) et on chercher si une suite binaire représente une valeur dans
		le dictionnaire codes: si oui  alors:
		                                    - on récupère la clé de cette valeur qui est le caractère
		                                    - on rajoute ce caractère à une chaine de caractère qui est initialement vide
		                                    - prochain parcours du texte sera de ( n + la taille de la suite binaire trouvée) initialement n=0 

		"""
		n=0
		caractere=""
		txtCompresser=""
		for i in txt[n:len(txt)]:
			n+=1
			caractere+=i
			for key,val in self.codes.items():
				if caractere==val:
					txtCompresser+=key
					caractere=""
		return txtCompresser



#programme principale fourni par l'enseignant
texteACompresser = txt  # txt contient le fichier VictorHugo
dicoFreq = findFrequence(texteACompresser) 
G = Arbre(dicoFreq) 
G.etiquetage(G.ListeNoeuds[0])              # On passe en argument le nœud racine pour etiqueter tout l’arbre 
texteCompresse=G.compress(texteACompresser)       
print(texteCompresse) 
# Affichage taux de compression 
print('Taux de compression : ', 100*(len(texteACompresser)*8-len(texteCompresse))/(len(texteACompresser)*8)) 
# decompression du texte compréssé 
texte = G.uncompress(texteCompresse) 
print(texte) 
# test pour vérifier que tout fonctionne ! 
if texte == texteACompresser:      
	print('Bravo cela fonctionne correctement !') 
else:      
	print('Encore un petit effort, vous y êtes presque !') 
