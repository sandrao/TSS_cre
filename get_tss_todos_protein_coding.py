
if __name__ == "__main__":
	gtf = open("Mus_musculus.GRCm38.100.gtf","r")
	transcritos = {}
	for linea in gtf:
		
		linea = linea[:-1].split("\t")#separo por tabulacion
		if len(linea) > 1:
			if linea[2] == "transcript" :
				if "transcript_biotype \"protein_coding\";" in linea[-1]:
					#obteniendo ID del transcrito
					id = linea[-1].split("transcript_name \"")[1].split("\"")[0] # obtengo el nombre del transcrito
					#si el transcrito  no esta en el diccionario de transcritos lo agrego
					if id not in transcritos:
						chr = linea[0]
						inicio = linea[3]
						termino = linea[4]
						hebra = linea[6]
						transcritos[id] = {"chr":chr,"inicio":inicio,"termino":termino,"hebra":hebra}
	gtf.close()
	chrs = ["1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","X","Y"] #para tener la salida ordenada por cromosoma
	archivo_salida = open("tss_protein_coding.bed","w")
	
	for chr in chrs:
		for id in transcritos:
			if transcritos[id]["chr"] == chr:
				#calculo el TSS en funcion de la hebra, si la hebra es positiva entonces el TSS es inicio, inicio+1; si la hebra es negativa entonces TSS es igual a termino -1, termino
				if transcritos[id]["hebra"] == "+":
					archivo_salida.write(transcritos[id]["chr"]+"\t"+transcritos[id]["inicio"]+"\t"+str(int(transcritos[id]["inicio"])+1)+"\n")
				if transcritos[id]["hebra"] == "-":
					archivo_salida.write(transcritos[id]["chr"]+"\t"+str(int(transcritos[id]["termino"])-1)+"\t"+transcritos[id]["termino"]+"\n")
	archivo_salida.close()
