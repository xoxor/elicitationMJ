import sys, os, statistics, math, csv, random, numpy


def median (vector):
    if(len(vector)%2==0):
        return vector[len(vector)//2]
    return vector[math.ceil(len(vector)/2)-1]


def questionsIterative(vector,n,m,k):
    gv=[]
    for i in range(n):
        Q = []
        while (len(Q) < k):
            num = random.randint(0, m)
            if num == 0:
                gv.append(vector[i])
                break
            elif not num in Q:
                Q.append(num)
    return gv

def questions(vector,n,m,k):
    gv=[]
    for i in range(n):
        if (random.random() < k/m): #the probability that each voter asks about "j_0" is n/k
            gv.append(vector[i])
    return gv

def probabilityOneBetterThanAll(n,m,k):
    vector = [5 for x in range(n)]
    for i in range(math.floor(n/2)+1):
        vector[i]=7
    count = 0
    for i in range(10000):
        incompleteV = questions(vector,n,m,k)
        if(len(incompleteV)==0 or median(incompleteV)==5):
            count+=1
    return(count/10000)
    

def generateICMatrix(n,m):
    vector = [random.randint(1,6) for x in range(n)]
    for i in range(math.floor(n/2)+1):
        vector[i]=7
    count = 0
    vector.sort(reverse=True)
    matrix = []
    matrix.append(vector)
    for i in range(m-1):
        vec = None
        while (vec is None or median(vec) >= 7):
            vec = [random.randint(1,7) for x in range(n)]
            vec.sort(reverse=True)
        matrix.append(vec.copy())
    return matrix

def statProbabilityNotWin(matrix,n,m,k,batch = 1000):
    counts = []
    for i in range(batch):
        counts.append(probabilityNotWinner(matrix,n,m,k))
    return numpy.average(counts), numpy.var(counts)

def probabilityNotWinner(matrix,n,m,k,expCount = 1000):
    if matrix is None:
        matrix = generateICMatrix(n,m)
    count = 0
    for i in range(expCount):
        medians = []
        for vector in matrix:
            incompleteV = questions(vector,n,m,k)
            if (len(incompleteV)==0):
                medians.append(-1)
            else:
                medians.append(median(incompleteV))
        winners = []
        while len(winners) < k:
            winners.append(numpy.array(medians).argmax())
            medians[winners[-1]] = -2
        if not 0 in winners: # We assume the winner to be the first vector of the matrix
            count+=1
    return count/expCount


def tableProbIC():
    f = open('table.csv', 'w')
    writer = csv.writer(f)
    header = ["n","m","k","ProbOfMiss", "SD"]
    writer.writerow(header)
    N = [100]
    M = [1/2]
    #Q = [1/8, 1/4, 1/3, 1/2, 2/3]
    #KsM = [0.05, 0.07, 0.1, 0.15, 0.2, 0.25, 0.3, 0.4]
    for n in N:
        for mu in M:
            m = math.floor(mu*n)
            for k in range(1, math.floor(m/2)+1):
                #k = math.floor(ksm * m)
                print("N",n,"M",m,"K",k)
                av, var = statProbabilityNotWin(None,n,m,k)
                writer.writerow([n,m,k,av,var])
    f.close

def tableProbElection():
    f = open('electiontable.csv', 'w')
    writer = csv.writer(f)
    header = ["n","m","k","ProbOfMiss", "SD"]
    writer.writerow(header)
    m = 12
    N = [10,25,50,100,250,500,1000,1500]
    for n in N:
        matrix = generateElectionMatrix(n)
        for k in range(1, math.ceil(m/2)):
            print("N",n,"M",m,"K",k)
            av, var = statProbabilityNotWin(matrix,n,m,k)
            print(av, var)
            writer.writerow([n,m,k,av,var])
    f.close

def makePercentageVector(n, l):
    vec = []
    valsum = 0.0
    for perc, value in l:
        vec.extend([value] * (math.floor(perc * n)))
        valsum += perc
    while (len(vec) < n):
        vec.append(1)
    return vec


def generateElectionMatrix(n):
    #n = 1147
    m1 = [(0.29, 7), (0.23, 6), (0.16, 5), (0.11, 4), (0.07, 3), (0.05, 2), (0.09, 1)]
    m2 = [(0.10, 7), (0.17, 6), (0.22, 5), (0.19, 4), (0.15, 3), (0.09, 2), (0.08, 1)]
    m3 = [(0.12, 7), (0.12, 6), (0.14, 5), (0.14, 4), (0.14, 3), (0.14, 2), (0.20, 1)]
    m4 = [(0.02, 7), (0.06, 6), (0.16, 5), (0.23, 4), (0.21, 3), (0.17, 2), (0.15, 1)]
    m5 = [(0.02, 7), (0.06, 6), (0.13, 5), (0.18, 4), (0.25, 3), (0.22, 2), (0.14, 1)]
    m6 = [(0.02, 7), (0.05, 6), (0.12, 5), (0.17, 4), (0.17, 3), (0.22, 2), (0.25, 1)]
    m7 = [(0.03, 7), (0.06, 6), (0.08, 5), (0.10, 4), (0.17, 3), (0.19, 2), (0.37, 1)]
    m8 = [(0.01, 7), (0.03, 6), (0.05, 5), (0.09, 4), (0.21, 3), (0.31, 2), (0.30, 1)]
    m9 = [(0.01, 7), (0.01, 6), (0.03, 5), (0.05, 4), (0.14, 3), (0.28, 2), (0.48, 1)]
    m10 = [(0.01, 7), (0.01, 6), (0.02, 5), (0.03, 4), (0.05, 3), (0.12, 2), (0.76, 1)]
    m11 = [(0.01, 7), (0.01, 6), (0.02, 5), (0.03, 4), (0.03, 3), (0.06, 2), (0.84, 1)]
    m12 = [(0.02, 7), (0.01, 6), (0.01, 5), (0.01, 4), (0.02, 3), (0.02, 2), (0.91, 1)]
    matrix = [makePercentageVector(n, m1),
    makePercentageVector(n, m2),
    makePercentageVector(n, m3),
    makePercentageVector(n, m4),
    makePercentageVector(n, m5),
    makePercentageVector(n, m6),
    makePercentageVector(n, m7),
    makePercentageVector(n, m8),
    makePercentageVector(n, m9),
    makePercentageVector(n, m10),
    makePercentageVector(n, m11),
    makePercentageVector(n, m12)]
    return matrix


def main():

    #print(probabilityOneBetterThanAll(10676,14,5))
    #print(probabilityOneBetterThanAll(100,50,10))
    
    tableProbIC()
    tableProbElection()



if __name__ == "__main__":
    main()


