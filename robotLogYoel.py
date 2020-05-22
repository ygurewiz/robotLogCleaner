



def robotLineAnalizer(lines,DirectionList,outputFile,writerHeaderFile):
    i=0
    currentDirection = ""
    Steps = list()
    #reverse = False
    #rotation = False
    #rotationDetails = None
    #Params = None
    #reverseDetails = None
    header=False
    robotHeaderLineList = list()
    robotStatusList1 = []
    robotStatusList2 = []
    robotStatusList3 = []
    for line in lines:
        if(len(line)<len("xxx\n")+1):
            continue
        i+=1
        timeStamp = str.split(getTimeStamp(line,i),'_')
        #write all lines
        #outLine = robotLogLineAnalizer(line,i)
        #if(outLine==None):
        #    continue
        #outputFile.write(str(i)+': '+outLine[0])
    #Header
        encoders = getLOG_LOCATION_DATA_ENCODERS_DISTANCE(line,i)
        if(not encoders==None):
            print("Date: "+timeStamp[0]+" Time: "+timeStamp[1]+' ' + " Left: "+ encoders[0] + " Right: "+ encoders[1])
        headingDirection = getLOG_LOCATION_INIT_ON_START_MOVEMENT(line,i)
        
        if(not headingDirection==""):
            print("Date: "+timeStamp[0]+" Time: "+timeStamp[1]+' ' + " Direction of Movement: " +headingDirection)
        
        headerStatus = getRobotStatus(line,i)
        if(not headerStatus==None):
            if(str(headerStatus[0])=='1'):
                robotStatusList1 = headerStatus[1:]
            elif(str(headerStatus[0])=='2'):
                robotStatusList2 = headerStatus[1:]
            elif(str(headerStatus[0])=='3'):
                robotStatusList3 = headerStatus[1:]
            header = (len(robotStatusList1)>0 and len(robotStatusList2)>0 and len(robotStatusList3)>0)
            if(header):
                robotHeaderLineList.append(rHeader(i,timeStamp[0],timeStamp[1],robotStatusList1,robotStatusList2,robotStatusList3))
                header=False
                robotStatusList1 = []
                robotStatusList2 = []
                robotStatusList3 = []
        #index=str.find(line,"LOG_STEP_")
        #if(not index==-1):
            #print(line)
    #step
        #stepStart = isStepStart(line,i)
        #stepEnd = isStepEnd(line,i)
    #Rotation
        #rotation = isTurn(line,i)
        #if(rotation):
        #    rotation = getTurnDetails(line,i,reverseDetails,rotationDetails,Params,rotation)
        #else:
        #    rotationDetails = None
        #    Params = None
        #    

    for i in robotHeaderLineList:
        l = i.outputHeader()
        writerHeaderFile.writerow(l)

    
    #movement
        #direction = getRobotHDirection(line,i)
        #reverse = isReverse(line,i)
        #if(reverse):
        #    print(line)
        #if(not direction==""):#returns "" if no direction declaration
        #    currentDirection = direction#direction declared
        #if(not currentDirection==""):
        #    distance = getRobotDistanceTraveled(line,i)
        #    if(not distance==None):
        #        if(reverse):
        #            reverse=True
        #            go = 'R'
        #        else:
        #            reverse=False
        #            go = 'F'
        #        RHorizontalDirection = rHorizontalDirection(timeStamp,go,currentDirection,float(distance[0])/10,float(distance[1])/10)
        #        DirectionList.insert(-1,rHorizontalDirection)
                #DirectionList.insert(-1,str(i) + go+" current direction: "+currentDirection+" Left Encoder: " + distance[0] + " Right Encoder: " + distance[1])
#STEPS###################################
def isStepStart(line,i):
    for key in robotLogKeyWords.startSteps:
        index = str.find(line,key)
        if(not index==-1):
            return key
    return None

def isStepEnd(line,i):
    for key in robotLogKeyWords.endSteps:
        index = str.find(line,key)
        if(not index==-1):
            return key
    return None
def LOG_STEP_START_CROSS_BRIDGE(line,i):
    #Step: STEPS_CROSS_BRIDGE_PREPARATIONS, Closest Edge: WEST, Direction: SOUTH
    index = str.find(line,"Step: ")
    if(not index==-1):
        Step = str.split(line[index+len("Step: ")],',')[0].split()[0]

    index = str.find(line,"Closest Edge: ")
    if(not index==-1):
        closestEdge = str.split(line[index+len("Closest Edge: ")],',')[0].split()[0]

    index = str.find(line,"Direction: ")
    if(not index==-1):
        Direction = str.split(line[index+len("Direction: ")],',')[0].split()[0]
    return [Step,closestEdge,Direction]

def getLOG_LOCATION_INIT_ON_START_MOVEMENT(line,i):
    LOG_LOCATION_INIT_ON_START_MOVEMENT = ""
    index = str.find(line,"LOG_LOCATION_INIT_ON_START_MOVEMENT ")
    if(not index==-1):
        LOG_LOCATION_INIT_ON_START_MOVEMENT = str.split(line[index:],':')[1].split()[0]
    return LOG_LOCATION_INIT_ON_START_MOVEMENT

def LOG_STEP_START_CALIBRATION(line,i):
    #Step: STEPS_CALIBRATION_STEP, Calibration Direction: WEST
    index = str.find(line,"Step: ")
    if(not index==-1):
        Step = str.split(line[index+len("Step: "):],',')[0].split()[0]

    index = str.find(line,"Calibration Direction: ")
    if(not index==-1):
        Direction = str.split(line[index+len("Calibration Direction: "):],',')[0].split()[0]
    return [Step,Direction]

def LOG_STEP_START_EDGE_MOVE(line,i):
    #Step: STEPS_MOVE_ON_EDGE, Edge: WEST, Direction: 18000
    index = str.find(line,"Step: ")
    if(not index==-1):
        Step = str.split(line[index+len("Step: ")],',')[0].split()[0]

    index = str.find(line,"Edge: ")
    if(not index==-1):
        Edge = str.split(line[index+len("Edge: ")],',')[0].split()[0]

    index = str.find(line,"Direction: ")
    if(not index==-1):
        Direction = str.split(line[index+len("Direction: ")],',')[0].split()[0]
    return [Step,Edge,Direction]

def stepStartCreate(key,line,i):
        if(key=="LOG_STEP_START"):
            return []
        elif(key=="LOG_STEP_START_CROSS_BRIDGE"):
            [Step,closestEdge,Direction] = LOG_STEP_START_CROSS_BRIDGE(line,i)
        elif(key=="LOG_STEP_START_EDGE_MOVE"):
            [Step,Edge,Direction] = LOG_STEP_START_CROSS_BRIDGE(line,i)
        elif(key=="LOG_STEP_START_CALIBRATION"):
            [Step,Direction] = LOG_STEP_START_CALIBRATION(line,i)

def getLOG_LOCATION_DATA_ENCODERS_DISTANCE(line,i):
    index = str.find(line,"LOG_LOCATION_DATA_ENCODERS_DISTANCE")
    LeftEncoderDistance = ""
    RightEncoderDistance = ""
    if(not index==-1):
        encodersLine = str.split(line,' ')
        LeftEncoderDistance = str.split(encodersLine[8],',')[0].split()[0]
        RightEncoderDistance = encodersLine[13].split()[0].split()[0]
        return [LeftEncoderDistance,RightEncoderDistance]
    return None

def convertInt(num):
    if(num>32767):
        num-=65535
        return (float(num)/32767)*(180)
    return num

#HEADER##################################
def getRobotStatus(line,i):
    status = None
    for key in robotLogKeyWords.StatusKeys:
        index = str.find(line,key)
        if(index==-1):
            continue
        if(key=="LOG_ROBOT_STATUS_1"):
            #Surface type appearance number:
            index = str.find(line,"Current surface type: ")
            if(index==-1):
                return None
            currentSurface = str.split(line[index+len("Current surface type: "):],',')[0].split()[0]

            index = str.find(line,"Surface type appearance number: ")
            if(index==-1):
                return None
            SurfaceNum = str.split(line[index+len("Surface type appearance number: "):],',')[0].split()[0]

            index = str.find(line,"Total desired cleaning area: ")
            if(index==-1):
                return None
            TotalCleaningArea = str.split(line[index+len("Total desired cleaning area: "):],',')[0].split()[0]

            index = str.find(line,"Total area of fully cleaned segments: ")
            if(index==-1):
                return None
            CleanedArea = str.split(line[index+len("Total area of fully cleaned segments: "):],',')[0].split()[0]

            index = str.find(line,"Current segment surface area: ")
            if(index==-1):
                return None
            currentSurfaceArea = str.split(line[index+len("Current segment surface area: "):],',')[0].split()[0]

            return [1,currentSurface,SurfaceNum,TotalCleaningArea,CleanedArea,currentSurfaceArea]
        elif(key=="LOG_ROBOT_STATUS_2"):
            index = str.find(line,"Robot state: ")
            if(index==-1):
                return None
            RobotState = str.split(line[index+len("Robot state: "):],',')[0].split()[0]

            index = str.find(line,"Robot current step: ")
            if(index==-1):
                return None
            RobotCurrentStep = str.split(line[index+len("Robot current step: "):],',')[0].split()[0]
            
            index = str.find(line,"Iteration in step: ")
            if(index==-1):
                return None
            IterationInStep = str.split(line[index+len("Iteration in step: "):],',')[0].split()[0]
            if(int(IterationInStep)>0):
                it = int(IterationInStep) / 2**24.
                IterationInStep = str(int(it))

            index = str.find(line,"Number of fully cleaned segments: ")
            if(index==-1):
                return None
            NumberFullyCleanedSegments = str.split(line[index+len("Number of fully cleaned segments: "):],',')[0].split()[0]

            index = str.find(line,"Expected number of iterations in step: ")
            if(index==-1):
                return None
            ExpectedNumberOfIterations= str.split(line[index+len("Expected number of iterations in step: "):],',')[0].split()[0]
            if(int(ExpectedNumberOfIterations)>0):
                it = int(ExpectedNumberOfIterations) / 2**24.
                ExpectedNumberOfIterations = str(int(it))

            return [2,RobotState,RobotCurrentStep ,NumberFullyCleanedSegments,IterationInStep,ExpectedNumberOfIterations]
        elif(key=="LOG_ROBOT_STATUS_3"):
            index = str.find(line,"Current robot direction: ")
            if(index==-1):
                return None
            CurrentRobotDirection = str.split(line[index+len("Current robot direction: "):],',')[0].split()[0]

            index = str.find(line,"Current robot roll: ")
            if(index==-1):
                return None
            CurrentRoll = convertInt(int(str.split(line[index+len("Current robot roll: "):],',')[0].split()[0]))
            
            index = str.find(line,"Current robot pitch: ")
            if(index==-1):
                return None
            CurrentPitch = convertInt(int(str.split(line[index+len("Current robot pitch: "):],',')[0].split()[0]))

            index = str.find(line,"Battery level (Deci volts): ")
            if(index==-1):
                return None
            Battery = str.split(line[index+len("Battery level (Deci volts): "):],',')[0].split()[0]

            index = str.find(line,"Robot events: ")
            if(index==-1):
                return None
            RobotEvents= str.split(line[index+len("Robot events: "):],',')[0].split()[0]
            if(int(RobotEvents)>0):
                it = int(RobotEvents) / 2**0.
                RobotEvents = str(int(it))

            return [3,CurrentRobotDirection,CurrentRoll,CurrentPitch,Battery,RobotEvents]
#ROTATION#################################
def getTurnDetails(line,i,reverseDetails,rotationDetails,Params,rotation):
    rotationType = getRotationStatus(line,i)
    if(rotationType =="StartRotation"):
        reverseDetails = None
        rotation = True
    elif(rotationType =="MidRotation"):
        rotationDetails = getDirectionDetails(line,i)
    elif(rotationType =="EndRotation"):
        rotationDetails = getDirectionDetails(line,i)
        rotation = False
    elif(rotationType =="Params"):
        Params = getParam(line,i,Params)
    elif(rotationType=="ReverseTurn"):
        reverseDetails = getReverseDetails(line,i)
    return rotation   


def getParam(line,i,Params):
    #Param1: 26896, Param2: 365, Param3: 366, Param4: 0, Param5: -5
    if(not str.find(line,"LOG_GENERAL_DATA")==-1):
        index = str.find(line,"Param1:  ")
        if(index==-1):
            return None
        param1 = str.split(line[index+len("Param1: ")],' ')[0].split()[0]
        index = str.find(line,"Param2:  ")
        if(index==-1):
            return None
        param2 = str.split(line[index+len("Param2: ")],' ')[0].split()[0]
        index = str.find(line,"Param3:  ")
        if(index==-1):
            return None
        param3 = str.split(line[index+len("Param3: ")],' ')[0].split()[0]
        index = str.find(line,"Param4:  ")
        if(index==-1):
            return None
        param4 = str.split(line[index+len("Param4: ")],' ')[0].split()[0]
        index = str.find(line,"Param5:  ")
        if(index==-1):
            return None
        param5 = str.split(line[index+len("Param5: ")],' ')[0].split()[0]
        return [param1,param2,param3,param4,param5] 
    return None

def getRotationStatus(line,i):
    if(not str.find(line,"LOG_LOCATION_INIT_ON_START_MOVEMENT")==-1):
        return "StartRotation"
    if(not str.find(line,"LOG_MOVEMENT_ROTATION_MOVEMENT")==-1 or not str.find(line,"LOG_MOVEMENT_TURN_MOVEMENT_START")==-1):
        return "MidRotation"
    if(not str.find(line,"LOG_MOVEMENT_TURN_IS_FINISHED")==-1):
        return "EndRotation"
    if(not str.find(line,"LOG_GENERAL_DATA")==-1):
        return "Params"
    if(not str.find(line,"LOG_MOVEMENT_REVERSE_MOVEMENT_START")==-1):
        return "ReverseTurn"
    return ""

def getReverseDetails(line,i):
    #Movement Type: REVERSE_MOVEMENT, Direction From: 9009, Direction To: 27009, Forward: 1, Distance (Pulses): 304
    index = str.find(line,"Movement Type: ")
    if(index==-1):
        return None
    rType = str.split(line[index+len("Movement Type: ")],' ')[0].split()[0]
    index = str.find(line,"From: ")
    if(index==-1):
        return None
    rFrom = str.split(line[index+len("From: ")],' ')[0].split()[0]
    index = str.find(line," To: ")
    if(index==-1):
        return None
    rTo = str.split(line[index+len(" To: ")],' ')[0].split()[0]
    index = str.find(line,"Forward: ")
    if(index==-1):
        return None
    Forward = str.split(line[index+len("Forward: ")],' ')[0].split()[0]
    #Distance (Pulses)
    index = str.find(line,"Distance (Pulses)")
    if(index==-1):
        return None
    Pulses = str.split(line[index+len("Distance (Pulses):")],' ')[0].split()[0]
    return [rType,rFrom,rTo,Forward,Pulses]

def getDirectionDetails(line,i):
    #Rotation Type: ROTATION_AUTO_CCW, Direction From: 17859, Direction To: 16000
    index = str.find(line,"Rotation Type: ")
    if(index==-1):
        return None
    rType = str.split(line[index+len("Rotation Type: ")],' ')[0].split()[0]
    index = str.find(line,"From: ")
    if(index==-1):
        return None
    rFrom = str.split(line[index+len("From: ")],' ')[0].split()[0]
    index = str.find(line," To: ")
    if(index==-1):
        return None
    rTo = str.split(line[index+len(" To: ")],' ')[0].split()[0]
    return [rType,rFrom,rTo]


def isReverse(line,i):
    for key in robotLogKeyWords.Reverses:
        if(not str.find(line,key)==-1):
            return True
    return False    

def isTurn(line,i):
    for key in robotLogKeyWords.Rotation:
        if(not str.find(line,key)==-1):
            return True
    return False

def getRobotHDirection(line,i):
    for key in robotLogKeyWords.HorizontalDirection:
        if(not str.find(line,key)==-1):
            return key
    return ""

def getRobotDistanceTraveled(line,i):
    if(not str.find(line,"(millimeter)")==-1):
        dis = str.split(line,"(millimeter)")
        leftDis = str.split(str.split(dis[1],',')[0],' ')[1].strip()
        rightDis = str.split(str.split(dis[2],'\n')[0],' ')[1].strip()
        return [leftDis,rightDis]
    return None

def robotLogLineAnalizer(line,i):
    for key in robotLogKeyWords.KeyWords:
        if(not str.find(line,key)==-1):
            return [line,key]
    for key in robotLogKeyWords.HorizontalDirection:
        if(not str.find(line,key)==-1):
            return [line,key]
    for key in robotLogKeyWords.Rotation:
        if(not str.find(line,key)==-1):
            print(line)
            return [line,key]
    return None

def getTimeStamp(line,i):
    ############
    #DATE + TIME
    timestamp = str.split(line," ")
    date = str.split(timestamp[0],"-")
    #TIME
    time = str.split(timestamp[1],":")
    microseconds = timestamp[2]
    theTime = datetime.datetime(int(date[0]),int(date[1]),int(date[2]),int(time[0]),int(time[1]),int(time[2]),int(microseconds))
    timeStamp = str(theTime.strftime("%d-%m-%Y_%H:%M:%S.%f")).strip()
    ##########
    return timeStamp