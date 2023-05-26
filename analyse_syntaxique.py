import sys
from sly import Parser
from analyse_lexicale import FloLexer
import arbre_abstrait

class FloParser(Parser):
	# On récupère la liste des lexèmes de l'analyse lexicale
	tokens = FloLexer.tokens

	# Règles gramaticales et actions associées

	@_('listeInstructions')
	def prog(self, p):
		return arbre_abstrait.Programme(p[0])

	@_('instruction')
	def listeInstructions(self, p):
		l = arbre_abstrait.ListeInstructions()
		l.instructions.append(p[0])
		return l
					
	@_('instruction listeInstructions')
	def listeInstructions(self, p):
		p[1].instructions.append(p[0])
		return p[1]
		
	@_('ecrire')
	def instruction(self, p):
		return p[0]
			
	@_('ECRIRE "(" expr ")" ";"')
	def ecrire(self, p):
		return arbre_abstrait.Ecrire(p.expr) #p.expr = p[2]
		
	@_('nonboolean "+" produit')
	def nonboolean(self, p):
		return arbre_abstrait.Operation('+',p[0],p[2])
	
	@_('nonboolean "-" produit')
	def nonboolean(self, p):
		return arbre_abstrait.Operation('-',p[0],p[2])
	
	@_('produit "*" facteur')
	def produit(self, p):
		return arbre_abstrait.Operation('*',p[0],p[2])
	
	@_('produit "/" facteur')
	def produit(self, p):
		return arbre_abstrait.Operation('/',p[0],p[2])
	
	@_('produit "%" facteur')
	def produit(self, p):
		return arbre_abstrait.Operation('%',p[0],p[2])

	@_('"(" nonboolean ")"')
	def facteur(self, p):
		return p.nonboolean #ou p[1]
	
	@_('"-" "(" nonboolean ")"')
	def facteur(self, p):
		return arbre_abstrait.Operation('*',arbre_abstrait.Entier(-1),p.nonboolean)
		
	@_('ENTIER')
	def facteur(self, p):
		return arbre_abstrait.Entier(p.ENTIER) #p.ENTIER = p[0]
	
	@_('facteur')
	def produit(self, p):
		return p.facteur
	
	@_('produit')
	def nonboolean(self, p):
		return p.produit

	@_('LIRE "(" ")"')
	def facteur(self,p):
		return arbre_abstrait.Lire()
	
	@_('IDENTIFIANT')
	def facteur(self,p):
		return arbre_abstrait.Identifiant(p.IDENTIFIANT)
	
	@_('IDENTIFIANT "(" listeExpressions ")"')
	def facteur(self, p):
		return arbre_abstrait.AppelFonction(p.IDENTIFIANT, p.listeExpressions)
	
	@_('IDENTIFIANT "(" ")"')
	def facteur(self, p):
		return arbre_abstrait.AppelFonction(p.IDENTIFIANT)

	@_('expr "," listeExpressions')
	def listeExpressions(self, p):
		p[2].expressions.insert(0, p[0])
		return p[2]

	@_('expr')
	def listeExpressions(self, p):
		l = arbre_abstrait.ListeExpressions()
		l.expressions.append(p[0])
		return l
	
	@_('boolean')
	def expr(self, p):
		return p.boolean
	
	@_('nonboolean')
	def expr(self, p):
		return p.nonboolean
	
	@_('NON boolean')
	def boolean(self, p):
		return arbre_abstrait.Negation(p.boolean)

	@_('VRAI')
	def boolean(self, p):
		return arbre_abstrait.Boolean(True)
	
	@_('FAUX')
	def boolean(self, p):
		return arbre_abstrait.Boolean(False)
	
	@_('nonboolean INFERIEUR nonboolean')
	def boolean(self, p):
		return arbre_abstrait.Comparaison('<',p[0],p[2])
	
	@_('nonboolean SUPERIEUR nonboolean')
	def boolean(self, p):
		return arbre_abstrait.Comparaison('>',p[0],p[2])
	
	@_('nonboolean EGAL nonboolean')
	def boolean(self, p):
		return arbre_abstrait.Comparaison('==',p[0],p[2])
	
	@_('nonboolean DIFFERENT nonboolean')
	def boolean(self, p):
		return arbre_abstrait.Comparaison('!=',p[0],p[2])
	
	@_('nonboolean INFERIEUR_OU_EGAL nonboolean')
	def boolean(self, p):
		return arbre_abstrait.Comparaison('<=',p[0],p[2])
	
	@_('nonboolean SUPERIEUR_OU_EGAL nonboolean')
	def boolean(self, p):
		return arbre_abstrait.Comparaison('>=',p[0],p[2])
	
	@_('TYPE IDENTIFIANT "(" listeParametres ")" "{" listeInstructions "}"')
	def instruction(self, p):
		return arbre_abstrait.Fonction(p.IDENTIFIANT, p.listeParametres, p.listeInstructions)
	
	@_('parametre "," listeParametres')
	def listeParametres(self, p):
		p[2].parametres.insert(0, p[0])
		return p[2]
	
	@_('parametre')
	def listeParametres(self, p):
		l = arbre_abstrait.ListeParametres()
		l.parametres.append(p[0])
		return l
	
	@_('TYPE IDENTIFIANT')
	def parametre(self, p):
		return arbre_abstrait.Parametre(p.IDENTIFIANT)
	
	
	@_('IDENTIFIANT "=" expr ";"')
	def instruction(self, p):
		return arbre_abstrait.Affectation(p.IDENTIFIANT, p.expr)


if __name__ == '__main__':
	lexer = FloLexer()
	parser = FloParser()
	if len(sys.argv) < 2:
		print("usage: python3 analyse_syntaxique.py NOM_FICHIER_SOURCE.flo")
	else:
		with open(sys.argv[1],"r") as f:
			data = f.read()
			try:
				arbre = parser.parse(lexer.tokenize(data))
				arbre.afficher()
			except EOFError:
			    exit()
