import sys
from analyse_lexicale import FloLexer
from analyse_syntaxique import FloParser
import arbre_abstrait

num_etiquette_courante = -1 #Permet de donner des noms différents à toutes les étiquettes (en les appelant e0, e1,e2,...)

def nom_nouvelle_etiquette() :
	global num_etiquette_courante
	num_etiquette_courante +=1
	return "e"+ str(num_etiquette_courante)

afficher_table = False
afficher_nasm = False
"""
Un print qui ne fonctionne que si la variable afficher_table vaut Vrai.
(permet de choisir si on affiche le code assembleur ou la table des symboles)
"""
def printifm(*args,**kwargs):
	if afficher_nasm:
		print(*args,**kwargs)

"""
Un print qui ne fonctionne que si la variable afficher_table vaut Vrai.
(permet de choisir si on affiche le code assembleur ou la table des symboles)
"""
def printift(*args,**kwargs):
	if afficher_table:
		print(*args,**kwargs)

"""
Fonction locale, permet d'afficher un commentaire dans le code nasm.
"""
def nasm_comment(comment):
	if comment != "":
		printifm("\t\t ; "+comment)#le point virgule indique le début d'un commentaire en nasm. Les tabulations sont là pour faire jolie.
	else:
		printifm("")  
"""
Affiche une instruction nasm sur une ligne
Par convention, les derniers opérandes sont nuls si l'opération a moins de 3 arguments.
"""
def nasm_instruction(opcode, op1="", op2="", op3="", comment=""):
	if op2 == "":
		printifm("\t"+opcode+"\t"+op1+"\t\t",end="")
	elif op3 =="":
		printifm("\t"+opcode+"\t"+op1+",\t"+op2+"\t",end="")
	else:
		printifm("\t"+opcode+"\t"+op1+",\t"+op2+",\t"+op3,end="")
	nasm_comment(comment)


"""
Retourne le nom d'une nouvelle étiquette
"""
def nasm_nouvelle_etiquette():
	num_etiquette_courante+=1
	return "e"+str(num_etiquette_courante)

"""
Affiche le code nasm correspondant à tout un programme
"""
def gen_programme(programme):
	printifm('%include\t"io.asm"')
	printifm('section\t.bss')
	printifm('sinput:	resb	255	;reserve a 255 byte space in memory for the users input string')
	printifm('v$a:	resd	1')
	printifm('section\t.text')
	printifm('global _start')
	printifm('_start:')
	gen_listeInstructions(programme.listeInstructions)
	nasm_instruction("mov", "eax", "1", "", "1 est le code de SYS_EXIT") 
	nasm_instruction("mov", "ebx", "0", "", "") 
	nasm_instruction("int", "0x80", "", "", "exit") 
	
"""
Affiche le code nasm correspondant à une suite d'instructions
"""
def gen_listeInstructions(listeInstructions):
	for instruction in listeInstructions.instructions:
		gen_instruction(instruction)

"""
Affiche le code nasm correspondant à une instruction
"""
def gen_instruction(instruction):
	if type(instruction) == arbre_abstrait.Ecrire:
		gen_ecrire(instruction)
	else:
		print("type instruction inconnu",type(instruction))
		exit(1)

"""
Affiche le code nasm correspondant au fait d'envoyer la valeur entière d'une expression sur la sortie standard
"""	
def gen_ecrire(ecrire):
	gen_expression(ecrire.exp) #on calcule et empile la valeur d'expression
	nasm_instruction("pop", "eax", "", "", "") #on dépile la valeur d'expression sur eax
	nasm_instruction("call", "iprintLF", "", "", "") #on envoie la valeur d'eax sur la sortie standard

"""
Affiche le code nasm pour calculer et empiler la valeur d'une expression
"""
def gen_expression(expression):
	if type(expression) == arbre_abstrait.Operation:
		gen_operation(expression) #on calcule et empile la valeur de l'opération
	elif type(expression) == arbre_abstrait.Entier:
		nasm_instruction("push", str(expression.valeur), "", "", "") #on met sur la pile la valeur entière			
	elif type(expression) == arbre_abstrait.Boolean:
		if expression.valeur:
			nasm_instruction("push", "1", "", "", "")
		else:
			nasm_instruction("push", "0", "", "", "")
	elif type(expression) == arbre_abstrait.Negation:
		gen_negation(expression)
	elif type(expression) == arbre_abstrait.Comparaison:
		gen_comparaison(expression)
	elif type(expression) == arbre_abstrait.Lire:
		gen_lire()
	else:
		print("type d'expression inconnu",type(expression))
		exit(1)


"""
Affiche le code nasm pour calculer l'opération et la mettre en haut de la pile
"""
def gen_lire():
	nasm_instruction("mov", "eax" , "sinput")
	nasm_instruction("call", "readline")
	nasm_instruction("call", "atoi")
	nasm_instruction("push", "eax")

def gen_comparaison(comparaison):
    op = comparaison.op

    gen_expression(comparaison.exp1) # on calcule et empile la valeur de exp1
    gen_expression(comparaison.exp2) # on calcule et empile la valeur de exp2

    nasm_instruction("pop", "ebx", "", "", "dépile la seconde opérande dans ebx")
    nasm_instruction("pop", "eax", "", "", "dépile la première opérande dans eax")

    nasm_instruction("cmp", "eax", "ebx", "", "compare les deux opérandes")

    if op in ['==']:
        e_label = nom_nouvelle_etiquette()
        end_label = nom_nouvelle_etiquette()
        nasm_instruction("je", e_label, "", "", "sauter à l'étiquette si les valeurs sont égales")
        nasm_instruction("push", "0", "", "", "empile 0 (false) si les valeurs sont différentes")
        nasm_instruction("jmp", end_label, "", "", "sauter à la fin de la comparaison")
        nasm_instruction(e_label+":", "", "", "étiquette si les valeurs sont égales")
        nasm_instruction("push", "1", "", "", "empile 1 (true) si les valeurs sont égales")
        nasm_instruction(end_label+":", "", "", "étiquette de fin de la comparaison")

    elif op in ['<', '>', '<=', '>=']:
        l_label = nom_nouvelle_etiquette()
        g_label = nom_nouvelle_etiquette()
        le_label = nom_nouvelle_etiquette()
        ge_label = nom_nouvelle_etiquette()
        end_label = nom_nouvelle_etiquette()

        # sauts conditionnels
        if op == '<':
            nasm_instruction("jl", l_label, "", "", "sauter à l'étiquette si 'eax' < 'ebx'")
        elif op == '>':
            nasm_instruction("jg", g_label, "", "", "sauter à l'étiquette si 'eax' > 'ebx'")
        elif op == '<=':
            nasm_instruction("jle", le_label, "", "", "sauter à l'étiquette si 'eax' <= 'ebx'")
        elif op == '>=':
            nasm_instruction("jge", ge_label, "", "", "sauter à l'étiquette si 'eax' >= 'ebx'")

        nasm_instruction("push", "0", "", "", "empile 0 (false)")
        nasm_instruction("jmp", end_label, "", "", "sauter à la fin de la comparaison")

        if op == '<':
            nasm_instruction(l_label+":", "", "", "étiquette si 'eax' >= 'ebx'")
        elif op == '>':
            nasm_instruction(g_label+":", "", "", "étiquette si 'eax' <= 'ebx'")
        elif op == '<=':
            nasm_instruction(le_label+":", "", "", "étiquette si 'eax' > 'ebx'")
        elif op == '>=':
            nasm_instruction(ge_label+":", "", "", "étiquette si 'eax' < 'ebx'")
        nasm_instruction("push", "1", "", "", "empile 1 (true)")

        nasm_instruction(end_label+":", "", "", "étiquette de fin de la comparaison")

    elif op in ['!=']:
        e_label = nom_nouvelle_etiquette()
        end_label = nom_nouvelle_etiquette()
        nasm_instruction("jne", e_label, "", "", "sauter à l'étiquette si les valeurs sont différentes")
        nasm_instruction("push", "0", "", "", "empile 0 (false) si les valeurs sont égales")
        nasm_instruction("jmp", end_label, "", "", "sauter à la fin de la comparaison")
        nasm_instruction( e_label+":", "", "", "étiquette si les valeurs sont différentes")
        nasm_instruction("push", "1", "", "", "empile 1 (true) si les valeurs sont différentes")
        nasm_instruction(end_label+":", "", "", "étiquette de fin de la comparaison")

def gen_operation(operation):
	op = operation.op
		
	gen_expression(operation.exp1) #on calcule et empile la valeur de exp1
	gen_expression(operation.exp2) #on calcule et empile la valeur de exp2
	
	nasm_instruction("pop", "ebx", "", "", "dépile la seconde operande dans ebx")
	nasm_instruction("pop", "eax", "", "", "dépile la permière operande dans eax")
	
	code = {"+":"add","*":"imul","-":"sub","/":"div","%":"div","OU":"or","ET":"and"} #Un dictionnaire qui associe à chaque opérateur sa fonction nasm
	#Voir: https://www.bencode.net/blob/nasmcheatsheet.pdf
	if op in ['+']:
		nasm_instruction(code[op], "eax", "ebx", "", "effectue l'opération eax" +op+"ebx et met le résultat dans eax" )
	if op in ['-']:
		nasm_instruction(code[op], "eax", "ebx", "", "effectue l'opération eax" +op+"ebx et met le résultat dans eax" )
	if op == '*':
		nasm_instruction(code[op], "ebx", "", "", "effectue l'opération eax" +op+"ebx et met le résultat dans eax" )
	if op == '/':
		nasm_instruction("mov", "edx", "0", "", "met 0 dans edx pour éviter un problème de division")
		nasm_instruction(code[op], "ebx", "", "", "effectue l'opération eax" +op+"ebx et met le résultat dans eax" )
	if op == '%':
		nasm_instruction("mov", "edx", "0", "", "met 0 dans edx pour éviter un problème de division")
		nasm_instruction(code[op], "ebx", "", "", "effectue l'opération eax" +op+"ebx et met le résultat dans eax" )
		nasm_instruction("mov", "eax", "edx", "", "met le reste de la division dans eax")
	if op == 'OU':
		nasm_instruction(code[op], "eax", "ebx", "", "effectue l'opération eax" +op+"ebx et met le résultat dans eax" )
	if op == 'ET':
		nasm_instruction(code[op], "eax", "ebx", "", "effectue l'opération eax" +op+"ebx et met le résultat dans eax" )

	nasm_instruction("push",  "eax" , "", "", "empile le résultat");	

def gen_negation(negation):
	gen_expression(negation.valeur)
	nasm_instruction("pop", "eax")
	nasm_instruction("xor", "eax", "1")
	nasm_instruction("push", "eax")

if __name__ == "__main__":
	afficher_nasm = True
	lexer = FloLexer()
	parser = FloParser()
	if len(sys.argv) < 3 or sys.argv[1] not in ["-nasm","-table"]:
		print("usage: python3 generation_code.py -nasm|-table NOM_FICHIER_SOURCE.flo")
		exit(1)
	if sys.argv[1]  == "-nasm":
		afficher_nasm = True
	else:
		afficher_tableSymboles = True
	with open(sys.argv[2],"r") as f:
		data = f.read()
		try:
			arbre = parser.parse(lexer.tokenize(data))
			gen_programme(arbre)
		except EOFError:
			exit()
