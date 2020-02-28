import numpy as np
import random
from random import randrange
import sys
from numpy.random import random as RP
import numpy as np
from numpy.random import choice
import matplotlib.pyplot as plt

#Defining a model class for the model, also checks satisfiability with respect to the clauses
class modelclass:
    model={}
    def __init__(self, numvariables): #randomly initialising values
        for i in range(numvariables):
            val=bool(random.getrandbits(1)) 
            self.model[i+1]=val

    def model_print(self): #printing model
        print(self.model)
        
    def satisfies(self, clauses): #checking for satisfiability
        flag=1
        unsat=[]
        for clause in clauses:
            for var in clause:
                if var>0: #positive variable
                    if self.model[abs(var)]==True: 
                        sat=1
                        break #if any literal is true in an OR condition, then the clause is true
                    else:
                        sat=0
                else: #negative variable
                    if self.model[abs(var)]==False:
                        sat=1
                        break #if any literal is true in an OR condition, then the clause is true
                    else:
                        sat=0
            if sat==0: #if any clause is false, then model does not satisfy
                flag=0
                unsat.append(clause)
        if flag==1:
            return True, []
        return False, unsat

#Modified WalkSAT problem
def walksat_modified(numclauses, numvariables, clauses, p, maxflips, maxv):
    x=modelclass(numvariables)
    count=0
    for v in range(1, maxv+1): #as given in the question
        unsat=[]
        for i in range(maxflips):
            val, unsat=x.satisfies(clauses)
            count+=1
            if val==True:    #checking if model satisfies clauses
                return x, count
            
            S={}    #generating a list of variables present in unsatisfied clauses
            for unsatclauses in unsat:
                for unsatvar in unsatclauses:
                    S[unsatvar]=True
            S= [ k for k in S ]
            p_=random.uniform(0, 1) #getting the probability

            if p_<p:
                x=FlipVariables(x, S, v)   #flipping v variables simultaneously with a probability p
                
            else:
                import itertools
                w=list(itertools.combinations((S), v)) #getting all possible combinations of v variables
            
                minn=sys.maxsize #to obtain the flip that satisfies most clauses, and store it in minvar
                for setvar in w:
                    unsat2=[]
                    val2, unsat2=x.satisfies(clauses)

                    if minn>len(unsat2):
                        minn=len(unsat2)
                        minvar=setvar
                    x=FlipVariables(x, S, v)
                x=FlipVariables(x, minvar, v)
    return -1, count

def FlipVariables(x, S, v): 
    if len(S)>v:
        flipvars=random.sample(S, v) #randomly picking v variables
    else: #if the number of elements in S is lesser than v
        flipvars=S
    for var in flipvars:
        x.model[abs(var)]=not x.model[abs(var)]
    return x


def CreateCNF(k, m, n): #to generate random instances of K-CNF clauses
    clauses = []
    vars = range(1, n+1)
    while len(clauses) < m:
        clausevars = choice(vars, size=k, replace=False)
        clausevars = np.sort([x * (-1) if RP() < 0.5 else x for x in clausevars])
        clauses.append(clausevars)
    return np.asarray(clauses)


k = 3
# numclauses = 80
numvariables = 10
p=0.5
x=[]
y=[]
all_counts = []
for ratio in range(1, 8+1):
    print(ratio)
    numclauses = numvariables*ratio
    print("For ratio",ratio)
    print(ratio, numvariables, numclauses)
    counts = []
    clauses = CreateCNF(k, numclauses, numvariables)
    for i in range(20):
        mod, cnt = walksat_modified(numclauses, numvariables, clauses, p, 1000, 3)
        counts.append(cnt)
    if(len(counts)>0):
        x.append(ratio)
        y.append(np.mean(counts))
plt.xlabel('m/n ratio', fontsize=18)
plt.ylabel('Mean Value of the time taken (For 10 runs)', fontsize=16)
plt.plot(x, y)
plt.show()
