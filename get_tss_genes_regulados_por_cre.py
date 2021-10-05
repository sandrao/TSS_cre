
if __name__ == "__main__":
	#cargando lista de genes que se sabe que son regulados por CRE
	archivo_lista_cre = open("lista80.txt","r")
	genes_regulados_por_cre = []
	for linea in archivo_lista_cre:
		genes_regulados_por_cre.append(linea[:-1].upper()) # la parte de [:-1] hace que cargue el gen sin el salto de linea (n); el upper es para tener todo el nombre del gen en mayuscula
	archivo_lista_cre.close()
	gtf = open("Mus_musculus.GRCm38.100.gtf","r")
	transcritos = {} #diccionario que tendra  ls informacion de los transcritos 
	for linea in gtf:	
		linea = linea[:-1].split("\t")#separo por tabulacion
		if len(linea) > 1:
			if linea[2] == "transcript" :
				nombre_gen = linea[-1].split("gene_name \"")[1].split("\"")[0].upper() #a la ultima columna la separo por la palabra gene name " donde la comilla doble esta al lado del nombre del gen, luego selecciono lo que esta adelante de esa comilla doble (posicion [1]) y lo separo por " que esta al final del nombre del gen, entonces selecciono lo que esta antes de esa comilla (posicion [0]) y ahi tengo el nombre del gen, luego lo convierto a mayusculas con upper y asi lo puedo comparar 
				if nombre_gen in genes_regulados_por_cre: #si el gen esta en esa lista entonces guardo los datos
					id = linea[-1].split("transcript_name \"")[1].split("\"")[0] # obtengo el nombre del transcrito
					if id not in transcritos:
						chr = linea[0]
						inicio = linea[3]
						termino = linea[4]
						hebra = linea[6]
						transcritos[id] = {"chr":chr,"inicio":inicio,"termino":termino,"hebra":hebra, "gen":nombre_gen}
				
	gtf.close()
	chrs = ["1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","X","Y"] #para tener la salida ordenada por cromosoma
	archivo_salida = open("tss_genes_regulados_por_cre.bed","w")
	genes_encontrados = []
	for chr in chrs:
		for id in transcritos:
			if transcritos[id]["chr"] == chr:
				#calculo el TSS en funcion de la hebra, si la hebra es positiva entonces el TSS es inicio, inicio+1; si la hebra es negativa entonces TSS es igual a termino -1, termino
				if transcritos[id]["hebra"] == "+":
					archivo_salida.write(transcritos[id]["chr"]+"\t"+transcritos[id]["inicio"]+"\t"+str(int(transcritos[id]["inicio"])+1)+"\n")
				if transcritos[id]["hebra"] == "-":
					archivo_salida.write(transcritos[id]["chr"]+"\t"+str(int(transcritos[id]["termino"])-1)+"\t"+transcritos[id]["termino"]+"\n")
				if transcritos[id]["gen"] not in genes_encontrados:
					genes_encontrados.append(transcritos[id]["gen"] )
	archivo_salida.close()

	
	for gen in genes_regulados_por_cre:
		if gen not in genes_encontrados:
			print("el gen "+gen+" de la lista CRE no lo encuentro en el archivo GTF")
