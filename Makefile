INPUT = $(basename $(notdir $(wildcard input/*.flo)))

assembleur_vers_exercutable:
	for a in $(INPUT); do echo "Assemblage: " $${a}; python3 generation_code.py -nasm input/$${a}.flo > output/$${a}.nasm; nasm -f elf -g -F dwarf output/$${a}.nasm; ld -m elf_i386 -o output/$${a} output/$${a}.o; rm output/$${a}.o; done;


INPUT2 = $(basename $(notdir $(wildcard input/tests/*.flo)))

tests: generation_code_nasm
	for a in $(INPUT2); do echo "Assemblage: " $${a}; nasm -f elf -g -F dwarf output/tests/$${a}.nasm; ld -m elf_i386 -o output/tests/$${a} output/tests/$${a}.o; rm output/tests/$${a}.o; done;

generation_code_nasm:
	for a in $(INPUT2); do echo "Generation code nasm: " $${a}; python3 generation_code.py -nasm input/tests/$${a}.flo > output/tests/$${a}.nasm; done;

