INPUT = $(basename $(notdir $(wildcard input/*.flo)))

assembleur_vers_exercutable:
	for a in $(INPUT); do echo "Assemblage: " $${a}; python3 generation_code.py -nasm input/$${a}.flo > output/$${a}.nasm; nasm -f elf -g -F dwarf output/$${a}.nasm; ld -m elf_i386 -o output/$${a} output/$${a}.o; rm output/$${a}.o; done;

