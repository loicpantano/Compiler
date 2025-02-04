"""
Affiche une chaine de caractère avec une certaine identation
"""
def afficher(s,indent=0):
	print(" "*indent+s)
	
class Programme:
	def __init__(self,listeFonctions, listeInstructions):
		self.listeFonctions = listeFonctions
		self.listeInstructions = listeInstructions
		if self.listeFonctions == None:
			self.listeFonctions = ListeFonctions()
		if self.listeInstructions == None:
			self.listeInstructions = ListeInstructions()
	def afficher(self,indent=0):
		afficher("<programme>",indent)
		self.listeFonctions.afficher(indent+1)
		self.listeInstructions.afficher(indent+1)
		afficher("</programme>",indent)

class ListeInstructions:
	def __init__(self):
		self.instructions = []
	def afficher(self,indent=0):
		afficher("<listeInstructions>",indent)
		for instruction in self.instructions:
			instruction.afficher(indent+1)
		afficher("</listeInstructions>",indent)

class ListeFonctions:
	def __init__(self):
		self.fonctions = []
	def afficher(self,indent=0):
		afficher("<listeFonctions>",indent)
		for instruction in self.fonctions:
			instruction.afficher(indent+1)
		afficher("</listeFonctions>",indent)

class Ecrire:
	def __init__(self,exp):
		self.exp = exp
	def afficher(self,indent=0):
		afficher("<ecrire>",indent)
		self.exp.afficher(indent+1)
		afficher("</ecrire>",indent)
		
class Declaration:
	def __init__(self, type, nom):
		self.type = type
		self.nom = nom
	def afficher(self,indent=0):
		afficher("<declaration>",indent)
		afficher("[type:"+self.type+"]",indent+1)
		afficher("[nom:"+self.nom+"]",indent+1)
		afficher("</declaration>",indent)

class Affectation:
	def __init__(self,nom,exp):
		self.nom = nom
		self.exp = exp
	def afficher(self,indent=0):
		afficher("<affectation>",indent)
		afficher("[nom:"+self.nom+"]",indent+1)
		self.exp.afficher(indent+1)
		afficher("</affectation>",indent)

class DeclarationAffectation:
	def __init__(self,type,nom,exp):
		self.type = type
		self.nom = nom
		self.exp = exp
	def afficher(self,indent=0):
		afficher("<declarationAffectation>",indent)
		afficher("[type:"+self.type+"]",indent+1)
		afficher("[nom:"+self.nom+"]",indent+1)
		self.exp.afficher(indent+1)
		afficher("</declarationAffectation>",indent)

class Si:
	def __init__(self,exp,listeInstructions, branchage):
		self.exp = exp
		self.listeInstructions = listeInstructions
		self.branchage = branchage
	def afficher(self,indent=0):
		afficher("<si>",indent)
		afficher("<condition>",indent+1)
		self.exp.afficher(indent+2)
		afficher("</condition>",indent+1)
		self.listeInstructions.afficher(indent+1)
		afficher("</si>",indent)
		self.branchage.afficher(indent)

class SinonSi:
	def __init__(self,branche):
		self.exp = branche.exp
		self.listeInstructions = branche.listeInstructions
		self.branchage = branche.branchage
	def afficher(self,indent=0):
		afficher("<sinonsi>",indent)
		afficher("<condition>",indent+1)
		self.exp.afficher(indent+2)
		afficher("</condition>",indent+1)
		self.listeInstructions.afficher(indent+1)
		afficher("</sinonsi>",indent)
		self.branchage.afficher(indent)

class Sinon:
	def __init__(self,listeInstructions):
		self.listeInstructions = listeInstructions
	def afficher(self,indent=0):
		afficher("<sinon>",indent)
		self.listeInstructions.afficher(indent+1)
		afficher("</sinon>",indent)

class TantQue:
	def __init__(self,exp,listeInstructions):
		self.exp = exp
		self.listeInstructions = listeInstructions
	def afficher(self,indent=0):
		afficher("<tantque>",indent)
		afficher("<condition>",indent+1)
		self.exp.afficher(indent+2)
		afficher("</condition>",indent+1)
		self.listeInstructions.afficher(indent+1)
		afficher("</tantque>",indent)


class Retourner:
	def __init__(self,exp):
		self.exp = exp
	def afficher(self,indent=0):
		afficher("<retourner>",indent)
		self.exp.afficher(indent+1)
		afficher("</retourner>",indent)

class Operation:
	def __init__(self,op,exp1,exp2):
		self.exp1 = exp1
		self.op = op
		self.exp2 = exp2
	def afficher(self,indent=0):
		afficher(f"<operation \"{self.op}\" >", indent)
		self.exp1.afficher(indent+1)
		self.exp2.afficher(indent+1)
		afficher("</operation>",indent)
class Entier:
	def __init__(self,valeur):
		self.str = "entier"
		self.valeur = valeur
	def afficher(self,indent=0):
		afficher("[Entier:"+str(self.valeur)+"]",indent)

class Boolean:
	def __init__(self, valeur):
		self.str = "booleen"
		self.valeur = valeur

	def afficher(self, indent=0):
		afficher("[Boolean:"+str(self.valeur)+"]",indent)

class Negation:
	def __init__(self, valeur):
		self.valeur = valeur

	def afficher(self, indent=0):
		afficher("<Negation>", indent)
		self.valeur.afficher(indent+1)
		afficher("</Negation>", indent)

class Comparaison:
	def __init__(self,op,exp1,exp2):
		self.exp1 = exp1
		self.op = op
		self.exp2 = exp2
	def afficher(self,indent=0):
		afficher(f"<comparaison \"{self.op}\" >", indent)
		self.exp1.afficher(indent+1)
		self.exp2.afficher(indent+1)
		afficher("</comparaison>",indent)

class Lire:
    def __init__(self):
        self.nom = "Lire"
    def afficher(self,indent=0):
        afficher("<Lire>",indent)
        afficher("</Lire>",indent)
	
class Identifiant:
	def __init__(self, nom):
		self.nom = nom
	def afficher(self,indent=0):
		afficher("[Identifiant:"+self.nom+"]",indent)

class ListeExpressions:
	def __init__(self ):
		self.expressions = []

	def afficher(self, indent=0):
		afficher("<ListeExpressions>", indent)
		for expression in self.expressions:
			expression.afficher(indent+1)
		afficher("</ListeExpressions>", indent)

class AppelFonction:
	def __init__(self, nom, listeExpressions = ListeExpressions()):
		self.nom = nom
		self.listeExpressions = listeExpressions

	def afficher(self, indent=0):
		afficher("<AppelFonction>", indent)
		afficher("<" +self.nom + ">", indent+1)
		self.listeExpressions.afficher(indent+2)
		afficher("</" +self.nom + ">", indent+1)
		afficher("</AppelFonction>", indent)



class Fonction:
	def __init__(self, type, nom, listeParametres, listeInstructions):
		self.type = type
		self.nom = nom
		self.listeParametres = listeParametres
		self.listeInstructions = listeInstructions

	def afficher(self, indent=0):
		afficher("<Fonction>", indent)
		afficher("<" +self.nom + ">", indent+1)
		afficher("[" +self.type + "]", indent+2)
		self.listeParametres.afficher(indent+2)
		self.listeInstructions.afficher(indent+2)
		afficher("</" +self.nom + ">", indent+1)
		afficher("</Fonction>", indent)

class ListeParametres:
	def __init__(self):
		self.parametres = []

	def afficher(self, indent=0):
		afficher("<ListeParametres>", indent)
		for parametre in self.parametres:
			parametre.afficher(indent+1)
		afficher("</ListeParametres>", indent)

class Parametre:
	def __init__(self, nom, type):
		self.nom = nom
		self.type = type
	def afficher(self, indent=0):
		afficher("<Parametre>", indent)
		afficher("<" +self.nom + ">", indent+1)
		afficher("</" +self.nom + ">", indent+1)
		afficher("</Parametre>", indent)

class Empty:
	def __init__(self):
		pass
	def afficher(self,indent=0):
		pass

