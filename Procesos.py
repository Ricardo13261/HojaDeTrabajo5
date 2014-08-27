"""
Universidad del Valle de Guatemla
Estructura de Datos
Autores: Ricardo Franco, 13261
		 Brandon Mendez, 13087

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
        instrucciones = random.randint(1,10)
        memoria = random.randint(1,10)
        if contador != 1:
            cantRAM = cantRAM - memoria
        contador = contador + 1
        c = procesos(env, i, memoria, RAM, CPU, ESPERA, instrucciones,cantRAM)	#se llenan los datos del proceso
        env.process(c)
        t = random.expovariate(1.0 / intervalo)	#La creación de procesos siguiendo una 
															#distribución exponencial con intervalo = 10
        yield env.timeout(t)


def procesos(env, nombre,memoria, RAM, CPU, ESPERA, instrucciones,cantRAM):
    arrive = env.now
    print ('%7.4f %s: NEW (esperando RAM %s), RAM disponible %s' % (arrive, nombre, memoria, cantRAM))
    with RAM.get(memoria) as reqRAM:
        yield reqRAM	                            #espera hasta que le den memoria
		
    esperando = env.now - arrive		    #tiempo que espero
    print ('%7.4f %s: Esperando RAM, tiempo: %6.3f' % (env.now, nombre, esperando))
        
    while instrucciones >0:
        with CPU.request() as reqCPU:
            yield reqCPU	#espera por la CPU
            print ('%7.4f %s: FASE WAITING %6.3f' % (env.now, nombre,instrucciones))
            yield env.timeout(1)	#tiempo dedica por CPU para las instrucciones

            if instrucciones>3:
        	    instrucciones = instrucciones -3
            else:
                instrucciones = 0
				
    if instrucciones >0:	
        pasoSiguiente= random.choice (["LISTO","ESPERANDO"])
        if pasoSiguiente == "ESPERANDO":	
            with Waiting.request() as reqespera:
                yield reqespera
                print ('%7.4f %s: Estado I/0 %s' % (env.now,nombre))
                yield env.timeout(1)	
        print ('%7.4f %s: Esperando en Ready...' % (env.now,nombre))


    tiempoProceso= env.now -arrive
    print('%7.4f %s: Tiempo de ejecucion Terminado!! :D %s' % (env.now, nombre, tiempoProceso))



    with RAM.put(memoria) as reqDevolverRAM:
        yield reqDevolverRAM	#se devuelve la memoria
        print('%7.4f %s: regresando la memoria RAM... %s' % (env.now, nombre, memoria))



		
random.seed(RANDOM_SEED)
env = simpy.Environment()
CPU = simpy.Resource(env, capacity=1) 	#cantidad de CPUs
RAM = simpy.Container(env, init=100, capacity=100)		#cantidad de memoria RAM
ESPERA= simpy.Resource(env,capacity=1)		#tiempo de espera en la cola I/O
env.process(source(env, NuevoProceso, IntervaloDeProcesos, RAM, CPU, ESPERA,cantRAM,1))	#aqui le meto los 25 procesos
env.run()
