

def OnGround(time, acceleration, position, epsilon):
    listGroundIndexes = []
    accelerationRef = acceleration[0]
    facteurVerif = 0
    for i in range(len(acceleration)-10):
        if (acceleration[i] < accelerationRef+epsilon and acceleration[i] > accelerationRef-epsilon):
            facteurVerif+=1

            if (facteurVerif ==10):
                listGroundIndexes.append([i-10, i])
                facteurVerif=0
        else:
            facteurVerif = 0

    for j in range(len(listGroundIndexes)):
        m = listGroundIndexes[j][0]
        n = listGroundIndexes[j][1]

        for k in range(n-m):
            acceleration[m+k] = 0