import sys
from sly import Parser
from analyse_lexicale import FloLexer
import arbre_abstrait

class FloParser(Parser):
	# On récupère la liste des lexèmes de l'analyse lexicale
	tokens = FloLexer.tokens

	# Règles gramaticales et actions associées

	#Programme -----------------------------------------------------------------------

	@_('listeFonctions listeInstructions')
	def prog(self, p):
		return arbre_abstrait.Programme(p[0], p[1])
	
	@_('listeInstructions')
	def prog(self, p):
		return arbre_abstrait.Programme(None, p[0])
	
	
	@_('fonction')
	def listeFonctions(self, p):
		l = arbre_abstrait.ListeFonctions()
		l.fonctions.insert(0,p[0])
		return l

	
	@_('listeFonctions fonction')
	def listeFonctions(self, p):
		p[0].fonctions.append(p[1])
		return p[0]

	
	@_('TYPE IDENTIFIANT "(" listeParametres ")" "{" listeInstructions "}"')
	def fonction(self, p):
		return arbre_abstrait.Fonction(p.TYPE, p.IDENTIFIANT, p.listeParametres, p.listeInstructions)
	
	@_('TYPE IDENTIFIANT "(" ")" "{" listeInstructions "}"')
	def fonction(self, p):
		return arbre_abstrait.Fonction(p.TYPE, p.IDENTIFIANT, arbre_abstrait.ListeParametres(), p.listeInstructions)
	
	#Liste Instructions --------------------------------------------------------------------
					
	@_('instruction listeInstructions')
	def listeInstructions(self, p):
		p[1].instructions.insert(0, p[0])
		return p[1]
	
	@_('instruction')
	def listeInstructions(self, p):
		l = arbre_abstrait.ListeInstructions()
		l.instructions.insert(0, p[0])
		return l
	
	#Instruction -----------------------------------------------------------------------
		
	@_('ecrire')
	def instruction(self, p):
		return p[0]
	
	@_('ECRIRE "(" expr ")" ";"')
	def ecrire(self, p):
		return arbre_abstrait.Ecrire(p.expr) #p.expr = p[2]

	@_('TYPE IDENTIFIANT ";"')
	def instruction(self, p):
		return arbre_abstrait.Declaration(p.TYPE, p.IDENTIFIANT)
	
	@_('IDENTIFIANT "=" expr ";"')
	def instruction(self, p):
		return arbre_abstrait.Affectation(p.IDENTIFIANT, p.expr)
	
	@_('TYPE IDENTIFIANT "=" expr ";"')
	def instruction(self, p):
		return arbre_abstrait.DeclarationAffectation(p.TYPE, p.IDENTIFIANT, p.expr)
	
	@_('RETOURNER expr ";"')
	def instruction(self, p):
		return arbre_abstrait.Retourner(p.expr)

	#If -----------------------------------------------------------------------
	@_('SI "(" expr ")" "{" listeInstructions "}" branchage')
	def instruction(self, p):
		return arbre_abstrait.Si(p.expr, p.listeInstructions, p.branchage)
	
	@_('SINONSI "(" expr ")" "{" listeInstructions "}" branchage')
	def branchage(self, p):
		return arbre_abstrait.SinonSi(p.expr, p.listeInstructions, p.branchage)
	
	@_('SINON "{" listeInstructions "}"')
	def branchage(self, p):
		return arbre_abstrait.Sinon(p.listeInstructions)
	
	@_('')
	def branchage(self, p):
		return arbre_abstrait.Empty()
	
	#While -----------------------------------------------------------------------

	@_('TANTQUE "(" expr ")" "{" listeInstructions "}"')
	def instruction(self, p):
		return arbre_abstrait.TantQue(p.expr, p.listeInstructions)

	#Expressions nonboolean -----------------------------------------------------------------------
		
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
	
	@_('"-" unsignedfacteur')
	def facteur(self, p):
		return arbre_abstrait.Operation('-',arbre_abstrait.Entier(0),p[1])
	
	@_('unsignedfacteur')
	def facteur(self, p):
		return p.unsignedfacteur

	@_('ENTIER')
	def unsignedfacteur(self, p):
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
	
    #Fonctions -----------------------------------------------------------------------


	
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
	
	#Call not void -----------------------------------------------------------------------
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
	
	#Call void -----------------------------------------------------------------------
	@_('IDENTIFIANT "(" listeExpressions ")" ";"')
	def instruction(self, p):
		return arbre_abstrait.AppelFonction(p.IDENTIFIANT, p.listeExpressions)
	
	@_('IDENTIFIANT "(" ")" ";"')
	def instruction(self, p):
		return arbre_abstrait.AppelFonction(p.IDENTIFIANT)
	
	#Expressions boolean -----------------------------------------------------------------------

	@_('boolean')
	def expr(self, p):
		return p.boolean
	
	@_('nonboolean')
	def expr(self, p):
		return p.nonboolean
	
	@_('VRAI')
	def booleanfinal(self, p):
		return arbre_abstrait.Boolean(True)
	
	@_('FAUX')
	def booleanfinal(self, p):
		return arbre_abstrait.Boolean(False)
	
	@_('NON booleanfinal')
	def facteurbool(self, p):
		return arbre_abstrait.Negation(p.booleanfinal)
	
	@_('produitbool OU facteurbool')
	def produitbool(self, p):
		return arbre_abstrait.Operation('OU',p[0],p[2])
	
	@_('boolean ET produitbool')
	def boolean(self, p):
		return arbre_abstrait.Operation('ET',p[0],p[2])
	
	@_('booleanfinal')
	def facteurbool(self, p):
		return p.booleanfinal

	@_('facteurbool')
	def produitbool(self, p):
		return p.facteurbool
	
	@_('produitbool')
	def boolean(self, p):
		return p.produitbool
	
	@_('nonboolean INFERIEUR nonboolean')
	def booleanfinal(self, p):
		return arbre_abstrait.Comparaison('<',p[0],p[2])
	
	@_('nonboolean SUPERIEUR nonboolean')
	def booleanfinal(self, p):
		return arbre_abstrait.Comparaison('>',p[0],p[2])
	
	@_('nonboolean EGAL nonboolean')
	def booleanfinal(self, p):
		return arbre_abstrait.Comparaison('==',p[0],p[2])
	
	@_('nonboolean DIFFERENT nonboolean')
	def booleanfinal(self, p):
		return arbre_abstrait.Comparaison('!=',p[0],p[2])
	
	@_('nonboolean INFERIEUR_OU_EGAL nonboolean')
	def booleanfinal(self, p):
		return arbre_abstrait.Comparaison('<=',p[0],p[2])
	
	@_('nonboolean SUPERIEUR_OU_EGAL nonboolean')
	def booleanfinal(self, p):
		return arbre_abstrait.Comparaison('>=',p[0],p[2])

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
