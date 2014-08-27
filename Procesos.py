"""
Universidad del Valle de Guatemla
Estructura de Datos
Autores: Ricardo Franco, 13261
		 Brandon Mendez, 13

Escenario:
  Simulación de corrida de programas en un sistema operativo de tiempo compartido (el procesador se comparte por una 
  porción de tiempo entre cada programa que se desea correr). 
"""
import random
import simpy


RANDOM_SEED = 10
NuevoProceso = 25                                           #Total de procesos
IntervaloDeProcesos = 10.0                                  #intervalo de creacion de procesos
cantRAM=100

def source(env, numero, intervalo, RAM, CPU, ESPERA,cantRAM,contador):

    """se crean los procesos"""
    for i in range(numero):			#se crean los 25 procesos
 
        c = proceso(env, i, memoria, RAM, CPU, ESPERA, instrucciones,cantidadRAM)	#se llenan los datos del proceso
        env.process(c)
        t = random.expovariate(1.0 / intervalo)	#La creación de procesos siguiendo una 
															#distribución exponencial con intervalo = 10
        yield env.timeout(t)


def procesos(env, nombre,memoria, RAM, CPU, ESPERA, instruccione,cantRAM):
    """Procesos en ejecucion y esperas"""
    arrive = env.now
    print('%7.4f %s: Programa en espera de memoria RAM... MEMORIA RAM DISPONIBLE %s' % (arrive, nombre,memoria,cantidadRAM))
	#se solicita la memoria RAM
    with RAM.get(memoria) as reqRAM:
        yield reqRAM	                            #espera hasta que le den memoria
		
    esperando = env.now - arrive		    #tiempo que espero
    print ('%7.4f %s: Esperando RAM, tiempo: %6.3f' % (env.now, nombre, esperando))
        
    #se ejecuta el proceso mientras tenga instrucciones
    while instrucciones >0:
    with CPU.request() as reqCPU:
                yield reqCPU	#espera por la CPU
                print ('%7.4f %s: esperando CPU.. CPU corriendo instrucciones %6.3f' % (env.now, nombre))
                yield env.timeout(1)	#tiempo dedica por CPU para las instrucciones
                #se verifica cuantas intrucciones faltan por ejecutar
                if instrucciones>3:
		    instrucciones = instrucciones -3
    		else:
                    instrucciones = 0
                    #se ejecutaron todas las instrucciones
				
	    if instrucciones >0:	#si aun quedan instrucciones por ejecutar
            #se realiza un random para saber si debe ir a ready o waiting
                pasoSiguiente= random.choice (["ready","waiting"])
		if pasoSiguiente =="waiting":	#se va a las operaciones de I/O
                    with Waiting.request() as reqESPERA:
                        yield reqESPERA  #realiza cola en las operaciones I/O
			print ('%7.4f %s: Esperando en operaciones I/O... %s' % (env.now,nombre))
			yield env.timeout(1)	#es el tiempo de espera en operaciones I/O
		#se vuelve a hacer cola en ready, para pasar a ejecutar instrucciones faltantes
		print ('%7.4f %s: Esperando en Ready...' % (env.now,nombre))
        #se termino el proceso
	tiempoProceso= env.now -arrive
	print('%7.4f %s: Tiempo de ejecucion Terminado!! :D %s' % (env.now, nombre, tiempoProceso))
	#regresamos la memoria
	with RAM.put(memoria) as reqDevolverRAM:
	yield reqDevolverRAM	#se devuelve la memoria
	print('%7.4f %s: regresando la memoria RAM... %s' % (env.now, nombre, memoria))
		
# Setup and start the simulation
print('..:EJECUTANDO PROCESOS:..')
random.seed(RANDOM_SEED)
env = simpy.Environment()

# Start processes and run
CPU = simpy.Resource(env, capacity=1) 	#cantidad de CPUs
RAM = simpy.Container(env, init=100, capacity=100)		#cantidad de memoria RAM
ESPERA= simpy.Resource(env,capacity=1)		#tiempo de espera en la cola I/O
env.procesos(source(env, NuevoProceso, IntervaloDeProcesos, RAM, CPU, ESPERA))	#aqui le meto los 25 procesos
env.run()
