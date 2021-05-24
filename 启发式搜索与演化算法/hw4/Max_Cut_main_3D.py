import sys
import Max_Cut_RRMS_3D
import numpy as np
import random
import math
import sdp_do


def GetFacebookData(filePath):
    dataFile=open(filePath)
    maxIndex=-1
    minIndex=100000000
    for line in dataFile.readlines():
        items=line.split()
        if int(items[0])>maxIndex:
            maxIndex=int(items[0])
        if int(items[0])<minIndex:
            minIndex=int(items[0])
        if int(items[1]) > maxIndex:
            maxIndex = int(items[1])
        if int(items[1]) < minIndex:
            minIndex = int(items[1])
    nodeNum=maxIndex-minIndex+1
    print("maxIndex, minIndex, nodeNum is %d,%d,%d respectively."%(maxIndex,minIndex,nodeNum))
    dataFile.close()

    dataFile = open(filePath)
    data=np.mat(np.zeros((nodeNum,nodeNum)))
    for line in dataFile.readlines():
        items = line.split()
        if int(items[0])!=int(items[1]):#eliminate the self-circle
            data[int(items[0])-minIndex,int(items[1])-minIndex]=1.0
            data[int(items[1])-minIndex,int(items[0])-minIndex]=1.0
    dataFile.close()
    return data

class ObjectiveFunction:
    def __init__(self,data,w=None):#w is the weight of objective functions
        #initialize the random seed to make sure the reproduce of the result.
        #data is the adjacent matrix
        np.random.seed(1)
        random.seed(1)
        n = np.shape(data)[0]
        self.n=n
        self.data=data
        self.weightOfGraph1=1.0*np.mat(np.random.rand(n,n))
        self.weightOfGraph2=1.0*np.mat(np.random.rand(n,n))
        self.weightOfGraph3=1.0*np.mat(np.random.rand(n,n))
        self.weightList = [self.weightOfGraph1, self.weightOfGraph2, self.weightOfGraph3]
        self.ReformalizeWeightMatrix(n, data, *self.weightList)
        #self.Pow(n,*self.weightList)
        #self.wightOfEachMovie=np.mat([10.0*self.dataMean[i,0]/np.sum(self.dataMean) for i in range(self.numOfMovies)])
        self.f1=0.0
        self.f2=0.0
        self.f3=0.0
        self.w=w

    def Pow(self,n,*weightList):
            for i in range(n):
                for j in range(i,n):
                    count=1
                    for weightMatrix in weightList:
                        exp=1.0/count
                        weightMatrix[i,j]=math.pow(weightMatrix[i,j],exp)
                        weightMatrix[j,i]=weightMatrix[i,j]
                        count+=1


    def ReformalizeWeightMatrix(self,n,data,*args):
        for i in range(n):
            for j in range(i,n):
                if data[i,j]<0.5:#means data[i,j]==0
                    for item in args:
                        item[i,j]=0.0
                        item[j,i]=0.0
                else:
                    for item in args:
                        item[j,i]=item[i,j]

    def GetWeightList(self,k):
        return self.weightList[k]
    def F1(self,S):# S is the index of selected items
        S_hat = [item for item in range(self.n) if item not in S]
        self.f1=np.sum((self.weightOfGraph1[S,:])[:,S_hat])
        return self.f1

    def F2(self,S):# S is the index of selected
        S_hat = [item for item in range(self.n) if item not in S]
        self.f2 = np.sum((self.weightOfGraph2[S,:])[:,S_hat])
        return self.f2

    def F3(self,S): #S is the index of selected
        S_hat = [item for item in range(self.n) if item not in S]
        self.f3 = np.sum((self.weightOfGraph3[S,:])[:,S_hat])
        return self.f3

    def FS(self,matrix,S):
        S_hat = [item for item in range(self.n) if item not in S]
        return np.sum((matrix[S,:])[:,S_hat])
    def ObjectiveSpacePoint(self,S):
        self.f1 = self.F1(S)
        self.f2 = self.F2(S)
        self.f3 = self.F3(S)
        return [self.f1,self.f2,self.f3]


if __name__=="__main__":

    data=GetFacebookData('./football.gml')
    objectiveFunc = ObjectiveFunction(data)
    n = np.shape(data)[0]


    ###population is the list of solutions
    ##############################################################
    #for example population=[[0,3,5],[5,3,2],[1,2,5,8,9]] means that population contains three solutions
    #the fisrt solution solution [0,3,5] means all the nodes are divided into two partitions , nodes 0,3,5 are in one partition, and all the other nodes are in another partition
    #the second solution solution [5,3,2] means all the nodes are divided into two partitions , nodes 5,3,2 are in one partition, and all the other nodes are in another partition
    #the second solution solution [1,2,5,8,9] means all the nodes are divided into two partitions , nodes 1,2,5,8,9 are in one partition, and all the other nodes are in another partition
    # whe  you need to compute your regret ratio, please replace the population with your population
    ##############################################################
    population=[]

    ratio = Max_Cut_RRMS_3D.Do(population, data, objectiveFunc)
    print('the regret ratio is %f'%(ratio))
