"""
Universidad del Valle de Guatemla
Estructura de Datos
Autores: Ricardo Franco, 13261
		 Brandon Mendez, 13087

"""
import random
import simpy


RANDOM_SEED = 10                                                                                    #definiendo la semilla del Random
NuevoProceso = 25                                                                                   #Definiendo el tottal de procesos a ejecutar
IntervaloDeProcesos = 10.0                                                                          #intervalo de tiempo con el que van a llegar los
cantRAM=100                                                                                         #cantidad de Ram disponible para darle a los procesos

def source(env, numero, intervalo, RAM, CPU, ESPERA,cantRAM,contador):

    """se crean los procesos"""
    for i in range(numero):			                                                    #se crean los 25 procesos, con su respectivo nombre
        instrucciones = random.randint(1,10)
        memoria = random.randint(1,10)                                                              #definiendo cuanto de memoria utilizara cada proceso, por medio de un random
        if contador != 1:
            cantRAM = cantRAM - memoria                                                             #se dismimuye la cantidad de ram que tenemos por la que utiliza el proceso, recien creado
        contador = contador + 1
        c = procesos(env, i, memoria, RAM, CPU, ESPERA, instrucciones,cantRAM)	                    #se llenan los datos del proceso recien creado
        env.process(c)
        t = random.expovariate(1.0 / intervalo)	                                                    #La creación de procesos siguiendo una distribución exponencial
        yield env.timeout(t)


def procesos(env, nombre,memoria, RAM, CPU, ESPERA, instrucciones,cantRAM):
    arrive = env.now                                                                                #se crea la variable arrive, para saber cuanto tiempo se tardo en ejecutar el proceso
    print ('%7.4f %s: NEW (esperando RAM %s), RAM disponible %s' % (arrive, nombre, memoria, cantRAM)) #se muestra al usuario que el proceso creado ya tiene memoria RAM 
    with RAM.get(memoria) as reqRAM:
        yield reqRAM	                                                                            #e proceso espera hasta que le den memoria
		
    esperando = env.now - arrive		                                                    #se calcula el tiempo que espero
    print ('%7.4f %s: Esperando RAM, tiempo: %6.3f' % (env.now, nombre, esperando))                 #se muestra el tiempo que espero
        
    while instrucciones >0:
        with CPU.request() as reqCPU:                                                               #pasamos a la ejecucion de instrucciones
            yield reqCPU	                                                                    #espera por la CPU
            print ('%7.4f %s: FASE WAITING %6.3f' % (env.now, nombre,instrucciones))
            yield env.timeout(1)	                                                            #tiempo dedicado por CPU para las instrucciones

            if instrucciones>3:                                                                     #se ejecutan las primeras 3 instrucciones y se se evalua si sobraron instrucciones
        	    instrucciones = instrucciones -3
            else:
                instrucciones = 0
				
    if instrucciones >0:	                                                                    #si sobraron instrucciones
        pasoSiguiente= random.choice (["LISTO","ESPERANDO"])                                        #se genera el random para decidir si debe ir a Ready o a esperar como I/O
        if pasoSiguiente == "ESPERANDO":	
            with Waiting.request() as reqespera:
                yield reqespera
                print ('%7.4f %s: Estado I/0 %s' % (env.now,nombre))                                #se muestra al usuario el camino que se tomo devido al random
                yield env.timeout(1)	
        print ('%7.4f %s: Esperando en Ready...' % (env.now,nombre))


    tiempoProceso= env.now -arrive                                                                  #se calcula el tiempo total que tomó ejecutar todas las instrucciones
    print('%7.4f %s: FIN DE EJECUCION DE PROCESO  %s' % (env.now, nombre, tiempoProceso))     #se muestra al usuario



    with RAM.put(memoria) as reqDevolverRAM:
        yield reqDevolverRAM	#se devuelve la memoria                                             #se devuelve la memoria Ram tomada para la ejecucion del proceso
        print('%7.4f %s: Devolviendo Memoria ram ... %s' % (env.now, nombre, memoria))             #se muestra al usuario, que se devuelve la memoria



		
random.seed(RANDOM_SEED)
env = simpy.Environment()
CPU = simpy.Resource(env, capacity=1) 	                                                            #cantidad de CPUs
RAM = simpy.Container(env, init=100, capacity=100)		                                    #cantidad de memoria RAM
ESPERA= simpy.Resource(env,capacity=1)		                                                    #tiempo de espera en la cola I/O
env.process(source(env, NuevoProceso, IntervaloDeProcesos, RAM, CPU, ESPERA,cantRAM,1))	            #aqui le meto los 25 procesos
env.run()
