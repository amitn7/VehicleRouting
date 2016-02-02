
import random
import copy
class TSP_2_OPT:
    sequence = []
    distance_matrix=[]
   
        
    def solve(self):
        globalBestSequence=[]
        trial = 0
        localBestCost = sys.maxint
        
        globalBestCost = sys.maxint
        while(trial<10000):         
            random.shuffle(self.sequence)       
            while(true):
                j = 2
                while(j<(len(self.sequence)-1)):
                    self.try2opt(self.sequence, 0, j)
                    j=j+1
                for i in range(len(self.sequence)):
                    j=i+2    
                    while(j<(len(self.sequence)-1)):
                        self.try2opt(self.sequence, i, j)                        
                        j=j+1                            
                cost=self.calculateCost(self.sequence)
                if(cost<localBestCost):
                    localBestCost=cost
                    continue
                else :
                    break               
            if(globalBestCost> localBestCost):
                globalBestCost=localBestCost;
            	globalBestSequence=copy.deepcopy(self.sequence)
            trial=trial+1   
        return globalBestSequence
        

    def reverse(self,sequence,start,end):
        length = end - start
        if(length < 0):
            length += len(sequence)
        length = length / 2 + 1
        for i in range(length):
            temp= sequence[start]
            sequence.insert(start,sequence[end])
            sequence.insert(end,temp)
            start+=1
            if(start >= len(sequence)):
                start = 0
            end =end-1
            if(end < 0):
                end = len(sequence)-1
                
    def try2opt(self,sequence, index1, index2):
        cityXIndex = index1
        cityAIndex = index2
        if( index1==(len(sequence)-1)):
            cityYIndex = 0
        else :
            cityYIndex = index1 + 1

        
        if( index1==(len(sequence)-1)):
            cityBndex = 0
        else :
            cityBIndex = index1 + 1
        if((self.distance_matrix[sequence[cityXIndex]][sequence[cityYIndex]] + self.distance_matrix[sequence[cityAIndex]][sequence[cityBIndex]]) >
          (self.distance_matrix[sequence[cityXIndex]][sequence[cityAIndex]] + self.distance_matrix[sequence[cityYIndex]][sequence[cityBIndex]])):
              self.reverse(sequence, cityYIndex, cityAIndex)


    def calculateCost(self,sequence):
     cost=0.0
     for i in range(len(sequence)-1):
       cost+= self.distance_matrix[sequence[i]][sequence[i+1]]
     return cost 



         




 


class Customer:
      x=0.0
      y=0.0
      d=0
      customerRemaining=0
    
      def getX(self) :
        return self.x
     
      def setX(self,x) :
        self.x = x
     
      def getY(self) :
        return self.y
     
      def setY(self,y) :
        self.y = y
     
      def getD(self) :
        return self.d
     
      def setD(self,d) :
        self.d = d 



         




 


class Saving:
   
       nodeA=0
       nodeB=0
       savings=0.0
       considered=False
       
       def isConsidered(self):
           return self.considered
              
       def setConsidered(self,considered):
           self.considered = considered
       
       def getNodeA(self):
           return self.nodeA
       
       def setNodeA(self,nodeA):
           self.nodeA = nodeA
       
       def getNodeB(self):
           return self.nodeB
       
       def setNodeB(self,nodeB):
           self.nodeB = nodeB
       
       def getSavings(self):
           return self.savings
       
       def setSavings(self,savings):
           self.savings = savings 

import urllib
import copy
import math
class VRP:
    distance_matrix =  []
    savingsList = []
    customerList = []
    tourList = []
    data = ""
    nCust = 0
    vCapacity = 0
    noOfVehicle = 0
    
    def __init__(self,url):
        
        urlData = urllib.urlopen(url)
        data = urlData.read()
        data  = data.replace("\n","").replace("\r","")
        values = data[12:len(data)-16]
        values = values.split("</br>")
        initData = values[0].split(",")
        self.nCust = int(initData[0])
        self.noOfVehicle = int(initData[1])
        self.vCapacity = int(initData[2])
        self.data = values
        
        self.distance_matrix = [[0.0 for x in range(self.nCust)] for x in range(self.nCust)]
    
    def extractCustomerData(self):
        index = 0       
        for i in self.data:
            val = i.split(",")
            if index > 0: 
                m = i.split(",")
                customer = Customer()
                customer.setD(int(val[0]))
                customer.setX(float(val[1]))
                customer.setY(float(val[2]))
                self.customerList.append(customer)
            index+=1
    
    def createDistanceMatrix(self):
        for i in range(self.nCust):
            for j in range(self.nCust):
                if i==j:
                    self.distance_matrix[i][j] = (float(sys.maxint))
                else:
                    self.distance_matrix[i][j] = self.getDistance(self.customerList[i].getX(),self.customerList[i].getY(),self.customerList[j].getX(),self.customerList[j].getY())    
        
    
    def createSavingsList(self):
        for i in range(self.nCust):
            for j in range(self.nCust):
                if i!=0 and j>i:
                    saving = Saving()
                    saving.setNodeA(i)
                    saving.setNodeB(j)
                    saving.setSavings(self.distance_matrix[0][i]+self.distance_matrix[0][j]-self.distance_matrix[i][j])
                    self.savingsList.append(saving)            
        self.savingsList = sorted(self.savingsList,key=self.sortingKey)           
        
    def createTours(self):
        for saving in self.savingsList:
            if saving.isConsidered() == False:
                   self.updateTours(saving)
                   saving.setConsidered(True)
        
    
    def updateTours(self,saving):
        notInTheTours=0
        currentTour=[]
        if len(self.tourList) == 0:
            tour = []
            tour.append(0)
	    tour.append(saving.getNodeA())
	    tour.append(saving.getNodeB())
	    if self.isTourAffordable(tour):
	         self.tourList.append(tour)
	         return True
        else:
            
            
	    for i in range(len(self.tourList)):
	        currentTour=copy.deepcopy(self.tourList[i])
	        if (saving.getNodeA() in currentTour) and (saving.getNodeB() in currentTour):
		     return False
    	        elif not(saving.getNodeA() in currentTour) and not(saving.getNodeB() in currentTour):
	             notInTheTours += 1
        	     continue
	        elif self.isCustInterior(currentTour,saving.getNodeA()) or self.isCustInterior(currentTour,saving.getNodeB()):
	 	     continue
                else:
                     try:
    		         indexA=currentTour.index(saving.getNodeA())
                     except ValueError:
                         indexA=-1
                     try:    
	   	         indexB=currentTour.index(saving.getNodeB())
                     except ValueError:
                         indexB=-1
	  	     if indexA!=-1:
			  for j in range(len(self.tourList)):
                              
			      searchTour = self.tourList[j]
			      
                              if (saving.getNodeB() in searchTour) and not(self.isCustInterior(searchTour,saving.getNodeB())):
   			          mergedtour = self.mergeTours(saving.getNodeA(),saving.getNodeB(),copy.deepcopy(currentTour),copy.deepcopy(searchTour))
			          if self.isTourAffordable(mergedtour):
			 	       self.tourList.append(mergedtour)
				       self.tourList.remove(currentTour)
				       self.tourList.remove(searchTour)
				       return True
			          else:
				       break
                              if not(self.isAlreadyAssigned(saving.getNodeB())): 
				  modifiedTour= copy.deepcopy(currentTour)
		           	  if indexA == 1:
				       modifiedTour.insert(1,saving.getNodeB())
			          else:
				       modifiedTour.append(saving.getNodeB())
		  		  if self.isTourAffordable(modifiedTour):
				       self.tourList.remove(currentTour)
				       self.tourList.append(modifiedTour)
				       return True
				
		     else:
			  for j in range(len(self.tourList)):
			      searchTour=self.tourList[j]
			      if (saving.getNodeA() in searchTour) and not(self.isCustInterior(searchTour,saving.getNodeA())):
				  mergedtour=self.mergeTours(saving.getNodeB(),saving.getNodeA(),copy.deepcopy(currentTour),copy.deepcopy(searchTour)) 
				  if self.isTourAffordable(mergedtour):
				       self.tourList.append(mergedtour) 
				       self.tourList.remove(currentTour) 
				       self.tourList.remove(searchTour) 
				       return True
				  else:
				       break
                              if not(self.isAlreadyAssigned(saving.getNodeA())):
				 modifiedTour= copy.deepcopy(currentTour)
				 if (indexB == 1):
				       modifiedTour.insert(1,saving.getNodeA())
				 else:
				       modifiedTour.append(saving.getNodeA())
				 if self.isTourAffordable(modifiedTour):
				       self.tourList.remove(currentTour)
				       self.tourList.append(modifiedTour)
				       return True

        if notInTheTours==len(self.tourList):
	     tour= []
	     tour.append(0)
	     tour.append(saving.getNodeA())
	     tour.append(saving.getNodeB())
             if self.isTourAffordable(tour):
		  self.tourList.append(tour)
		  return True
             
				 
    def mergeTours(self,nodeA, nodeB, tour1, tour2):
	indexA = tour1.index(nodeA)
	indexB = tour2.index(nodeB)
	  
	if indexA==1 and indexB==1:
	   tour2.reverse()
           tour2 = copy.deepcopy(tour2[0:len(tour2)-1])
	   tour2.insert(0,0);
           tour1.remove(0);
           for i in range(len(tour1)):
	       tour2.append(tour1[i])
	   mergedTour=copy.deepcopy(tour2)

        elif indexA==1 and indexB==len(tour2)-1:
	   tour1 = copy.deepcopy(tour1[1:])
 	   for i in range(len(tour1)):
	       tour2.append(tour1[i])
	   mergedTour=copy.deepcopy(tour2)

	elif indexA==len(tour1)-1 and indexB==1:
	   tour2 = copy.deepcopy(tour2[1:])
	   for i in range(len(tour2)):
	       tour1.append(tour2[i])
	       mergedTour=copy.deepcopy(tour1)

	elif indexA == len(tour1)-1 and indexB == len(tour2)-1:
           tour2.reverse() 
	   tour2 = copy.deepcopy(tour2[0:len(tour2)-1])
	   for i in range(len(tour2)):
	       tour1.append(tour2[i])
	   mergedTour=copy.deepcopy(tour1)
        return mergedTour	  
        
        
    def displayTours(self):
        cost=0.0
        for i in range(len(self.tourList)):
            self.tourList[i].append(0)
        for i in range(len(self.tourList)):
            cost+=self.calculateCost(self.tourList[i])
        
        print cost
        sequence=""
        for i in range(len(self.tourList)):
        	for j in range(len(self.tourList[i])):
        	    sequence += str(self.tourList[i][j])+ " "
                print sequence
        	sequence=""
        
        remaniningVehicles =  self.noOfVehicle -len(self.tourList)
        for i in range(remaniningVehicles):
            print '0 0'    
          
    def isAlreadyAssigned(self,cust):

	  index=-1
	  for i in range(len(self.tourList)):
	      if cust in self.tourList[i]:
		    index=i
	  return False if index < 0 else True
	  
    def isCustInterior(self,tour,customer):
          try:
	      return tour.index(customer) > 1 and tour.index(customer) < len(tour)-1
          except ValueError:
              return False
 
    def isTourAffordable(self,tour):
	  totalDemand = 0
	  for i in range(len(tour)):
	      totalDemand += self.customerList[tour[i]].getD()
	  return True if totalDemand < self.vCapacity else False
	      
    def getDistance(self,x1,y1,x2,y2):
        return math.sqrt(math.pow(math.fabs(x2-x1),2) + math.pow(math.fabs(y2-y1),2))    
        
    def sortingKey(self,saving):
        return -(saving.getSavings())
        
    def calculateCost(self,sequence):
    	cost=0.0
    	for i in range(len(sequence)-1):
    		 cost+= self.distance_matrix[sequence[i]][sequence[i+1]]
    	return cost 



         




 


class VRP1(VRP):
     def createSavingsList(self,l,m):
        for i in range(self.nCust):
            for j in range(self.nCust):
                if i!=0 and j>i:
                    saving = Saving()
                    saving.setNodeA(i)
                    saving.setNodeB(j)
                    saving.setSavings(self.distance_matrix[0][i]+self.distance_matrix[0][j]-l*self.distance_matrix[i][j] + m*math.fabs(self.distance_matrix[0][i]-self.distance_matrix[0][j]))
                    self.savingsList.append(saving)            
        self.savingsList = sorted(self.savingsList,key=self.sortingKey) 
        
     def createTours(self):
             for l in self.drange(0.1,0.3,0.1):
                 for m in self.drange(0.0,0.2,0.1):
                     self.createSavingsList(l,m)
                     #for i in self.savingsList:
                      #      print 'x',i.getNodeA(),'y',i.getNodeB(),'s',i.getSavings()
                     for saving in self.savingsList:
                        if saving.isConsidered() == False:
                               self.updateTours(saving)
                               saving.setConsidered(True)  
                     bestCost=sys.maxint
                     bestTour = []
                     cost = 0
                     for i in range(len(self.tourList)):
                        self.tourList[i].append(0)
                     for i in range(len(self.tourList)):
                        cost+=self.calculateCost(self.tourList[i])
                               
                     if cost < bestCost:
                        bestCost = cost
                     bestTour = self.tourList
                     self.savingsList = []
                     self.tourList = []
                     print bestCost
                               
             self.tourList = copy.deepcopy(bestTour)                  
                               
     def drange(self,start, stop, step):
        r = start
        while r < stop:
        	yield r
        	r += step 



         




 


import urllib

dataUrl = "http://people.cs.clemson.edu/~saurabr/" 

v = VRP1(dataUrl)
v.extractCustomerData()
v.createDistanceMatrix()
#v.createSavingsList()
v.createTours()
#for i in v.savingsList:
#    print 'x',i.getNodeA(),'y',i.getNodeB(),'s',i.getSavings()
v.displayTours() 
