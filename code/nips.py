# -*- coding: utf-8 -*-
# test LDA 
import os
import logging, gensim, bz2 ,numpy as np
from gensim import corpora, models, similarities,utils 
import random,csv
import timeit

import time
start_time = time.time()
#nytimes 400 k week
#pubmed  2000 k  month
#β = 0.01
#α =2/K
#dictionary= corpora.ucicorpus.UciReader("docword.kos.txt", )
#
#docword="docword.kos.txt"
#vocabulary="vocab.kos.txt"
#dictionary=corpora.ucicorpus.UciCorpus(docword,vocabulary)
#
#dictx=dictionary.create_dictionary() 
#
#dictionary.save(docword + '_.dict')
#
#corpora.mmcorpus.MmCorpus.serialize(docword + '_.mm', dictionary)
#mm = corpora.mmcorpus.MmCorpus(docword + '_.mm') # `mm` document stream now has random access
 
# Ant Part*************************************************************************************************
ant_count = 5
iterations = 7
PheromoneConstant = 1.0
DecayConstant = 0.2
Alpha = 1	# Pheromone constant
Beta = 1	# Heuristic constant

RANDOM = 1
CITY0 = 0
initialization = RANDOM

#city List represent parameter to tune 
#cityA=[0.001,0.005,0.010,0.015,0.02,0.025,0.03,0.035,0.04,0.045,0.05,0.055,0.06,0.065,0.07,0.075,0.08,0.085,0.09,0.1]#2
#cityB=[0.01,0.03,0.05,0.08,0.1,0.13,0.15,0.18,0.2,0.23,0.25,0.28,0.3,0.33,0.35,0.38,0.4,0.43,0.45,0.48,0.5]#2
cityA=[0.05,0.1,0.15,0.2,0.25]#2
cityB=[0.0025,0.005,0.0075,0.01,0.0125,0.015,0.0175,0.02,0.0225,0.025,0.0275,0.03]#2
cityC=[10] # 9

cities_countA=len(cityA)
cities_countB=len(cityB)
cities_countC=len(cityC)

def emptyPath(cities_countA,cities_countB):
    path = []
    for from_city in range(cities_countA):
        path1 = []
        for to_city in range(cities_countB):
             path1.append(0)
	path.append(path1)
    
    return path



def initialize_ants(ant_count,cities_count):
	
	path=[]
	for ant in range(ant_count):
		if initialization == RANDOM:
			path.append([random.randint(0,cities_count-1)])
		elif initialization == CITY0:
			path.append([CITY0])
        print "initial Ant :: %s" % path	
        
        return path


# Calculate sum total of the probability distribution to unvisited cities
def sumTotal(cities_matrix, PheromoneAB,EachpathAnt):
		
	total = 0.0
	if len(EachpathAnt) == 1:
	   #print  len(EachpathAnt)
	   #print  "Each path Ant to city B"
	   for city in range(len(cityB)): #
	        #print EachpathAnt[0]		
		#total =1
		#print "PheromoneAB[EachpathAnt[0]][city]"
		#print PheromoneAB[EachpathAnt[0]][city]
		
		total = total + pow(PheromoneAB[EachpathAnt[0]][city],Alpha)* pow(1.0/1,Beta)
		#print PheromoneAB
	else:
	   #print  len(EachpathAnt)
	   #print  "Each path Ant to city C" 
	   for city in range(len(cityC)): #		
		#total =1
		
		
		total = total + pow(PheromoneAB[EachpathAnt[1]][city],Alpha)* pow(1.0/1,Beta)
	return total


# get Probability Distribution
def getProbabilityDistributionList(cities_matrix, PheromoneAB,EachpathAnt):

	sumTotalValue = sumTotal(cities_matrix, PheromoneAB,EachpathAnt)
	#print " sumTotalValue %s" % sumTotalValue 
	probList = []
		
	total = 0
	current_city = EachpathAnt[-1]  #
	#print "EachpathAnt as current city %s" %current_city
	#print "Current City:"+str(current_city)
	if sumTotalValue != 0:	# 1st iteration where there is no pheromone trail
	       if len(EachpathAnt) == 1:
	          #print "prob list for city B"
		  for city in range(len(cities_matrix)):
			#if city not in EachpathAnt:
				prev_probability = 0
				if len(probList) > 0:
					(prev_city,prev_prob) = probList[-1]
					prev_probability = prev_prob
					#print "prev_probability %s "  %prev_probability
                                #print "distribute prop"
                                #print  pow(PheromoneAB[current_city][city],Alpha)
                                cummulative_prob = (prev_probability + (pow(PheromoneAB[EachpathAnt[0]][city],Alpha) * pow(1.0/1,Beta))/sumTotalValue)
				
				probList.append((city,cummulative_prob))
				#print "probList B  %s"  %probList
	       else:
	          #print "prob list for city C"
		  for city in range(len(cities_matrix)):
			#if city not in EachpathAnt:
				prev_probability = 0
				if len(probList) > 0:
					(prev_city,prev_prob) = probList[-1]
					prev_probability = prev_prob
					#print "prev_probability %s "  %prev_probability
                                #print "distribute prop"
                                #print  pow(PheromoneAB[current_city][city],Alpha)
                                #cummulative_prob = (prev_probability + (pow(PheromoneAB[EachpathAnt[1]][city],Alpha) * pow(1.0/1,Beta))/sumTotalValue)
				cummulative_prob = (0 + (pow(PheromoneAB[EachpathAnt[1]][city],Alpha) * pow(1.0/1,Beta))/sumTotalValue)
				
				probList.append((city,cummulative_prob))
				#print "probList C %s"  %probList		
				
	#print "probList C %s"  %probList			
	return probList


# Find the next unvisited city
def nextCity(cities_matrix, pheromone_trail,EachpathAnt):
#def nextCity(cities_countA, PheromoneAB,pathAnt):
	#pathAnt[ant].append(nextCity(cities_countA, PheromoneAB,pathAnt[ant]))	
	#print " EachpathAnt in Nextcity function %s" % EachpathAnt 	
	prob_list = getProbabilityDistributionList(cities_matrix, pheromone_trail,EachpathAnt)
        
	next_city = -1
	
	if len(prob_list) == 0:	# initial condition
		next_city = random.randint(0,len(cities_matrix)-1) 		
		#print "next_city in initial condition "		
	else:
		#print "list------"+str(prob_list)
		toss = random.random()
		for (city, prob) in prob_list:
			#print "next_city in toss {}, {}, {}".format(toss, prob, city) 
			if toss <= prob:
			       # print 'inner' 
				#print str(visited_path)+"*************************************"+str(city)+":"+str(prob)
				next_city = city
				#print 'next city', next_city
				break
		 	
				
	if next_city == -1:
		#print str(prob_list)+"*****"+str(toss)
		next_city = random.randint(0,len(cities_matrix)-1) 
	return next_city


# new pheromone for a particulat edge
def newPheromoneAB(from_city,to_city,paths):
	
	tot = 0.0

	return tot

# Update Pheromone  function call when end each iteration    not complete
def updatePheromoneAB(pathAnt,PheromoneAB,PheromoneBC):


        for p in range(len(pathAnt)):
                
                
#	for from_city in range(len(pheromone_trail)):
#		for to_city in range(len(pheromone_trail)):
                PheromoneAB[pathAnt[p][0]][pathAnt[p][1]] = (1 - DecayConstant) * PheromoneAB[pathAnt[p][0]][pathAnt[p][1]]+ PheromoneConstant	
		PheromoneBC[pathAnt[p][1]][pathAnt[p][2]] = (1 - DecayConstant) * PheromoneBC[pathAnt[p][1]][pathAnt[p][2]]+PheromoneConstant	/2
#			pheromone_trail[from_city][to_city] = (1 - DecayConstant) * pheromone_trail[from_city][to_city] + newPheromone(from_city,to_city,path_array,cities_matrix)
 #       print "Update Pheromone"
	#print " PheromoneAB %s" % PheromoneAB 	
 #       print " PheromoneBC %s" % PheromoneBC		

def main():
    globalBest = 999999999999
    print "starting number of Ant ", ant_count,"iteration= ",iterations
    PheromoneAB = emptyPath(cities_countA,cities_countB)
    PheromoneBC = emptyPath(cities_countB,cities_countC)
    print " Pheromone Trail has create "
    for iteration in range(iterations):
        print "Iteration:-----"+str(iteration+1)
        pathAnt=initialize_ants(ant_count,cities_countA)
        
        f = open("inputAnt.txt", "w")
        
        for ant in range(ant_count):	
					
		pathAnt[ant].append(nextCity(cityB, PheromoneAB,pathAnt[ant]))	# Find next town
		#print pathAnt
                pathAnt[ant].append(nextCity(cityC, PheromoneBC,pathAnt[ant]))   
                #print                   
                #print "Paramite for Ant " ,ant ,"Path :: " ,pathAnt
                       
                paramAnt01=[cityA[pathAnt[ant][0]],cityB[pathAnt[ant][1]],cityC[pathAnt[ant][2]]]
                ###print " paramAnt01 when end iteration %s" % paramAnt01
                #print ant,' ',cityA[pathAnt[ant][0]],' ',cityB[pathAnt[ant][1]],' ',cityC[pathAnt[ant][2]]
                data_write = '{} {} {} {} \n'.format(ant, cityA[pathAnt[ant][0]], cityB[pathAnt[ant][1]], cityC[pathAnt[ant][2]])
                f.write(data_write)
        print " pathAnt when end iteration %s" % pathAnt
         

        f.close()
        os.system("hdfs dfs -put -f 'inputAnt.txt' /input_nips_{}".format(iteration));
        os.system("hadoop jar /code/hadoop-streaming.jar \
		-D mapreduce.map.memory.mb=2048 \
		-D mapreduce.reduce.memory.mb=2048 \
		-file /code/nips_mapper.py -mapper /code/nips_mapper.py -file /code/nips_reducer.py   -reducer /code/nips_reducer.py \
        -input /input_nips_{} -output /output_nips_{}".format(iteration, iteration))
        localBest = 99999999999999
        
        per_hdfs = os.popen('hdfs dfs -cat /output_nips_{}/part-00000'.format(iteration)).read()

        # for ant in range(ant_count): 			        
        per_word_perplex=float(per_hdfs.replace('\t\n','').split(' ')[1])

        if per_word_perplex < globalBest:
			globalBest = per_word_perplex
			path = [pathAnt[ant][0],pathAnt[ant][1],pathAnt[ant][2]]
			param = [cityA[pathAnt[ant][0]],cityB[pathAnt[ant][1]],cityC[pathAnt[ant][2]]]
	  #  if SumParameter < localBest:
			#localBest = SumParameter
        if per_word_perplex < localBest:
			localBest = per_word_perplex
			
			
			
	print "local Best:"+str(localBest) ,"path: %s" %path,"parameters: %s" %param
	
	
	
        updatePheromoneAB(pathAnt,PheromoneAB,PheromoneBC)
        print "End of each iteration*************************************************************"
    print "Globa; Best:"+str(globalBest) 
    print PheromoneAB
    print PheromoneBC

   

main()
print("--- %s seconds ---" % (time.time() - start_time))