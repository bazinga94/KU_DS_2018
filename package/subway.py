import pandas as pd
subway_all=pd.read_csv('C:/Users/user/Desktop/자료구조 최종발표 코드/지하철_인접리스트.csv', encoding='euc-kr',engine='python')
line=[0]
line_dic=[0]
roadMap = {}  # 1~8호선 링크드리스트 그래프
fastWay={}
temp_glo=""
move_array=[]

rootSt_save=[]

class Node:
    def __init__(self, name, time):
        self.name = name
        self.time = time
        self.link = None
# LinkedList 클래스 (자료구조) 정의
class LinkedList:
    # 초기화 메소드
    def __init__(self, standard_name):
        temp = Node(standard_name, 0)  # head 역 이름으로 바꿔야함
        self.head = temp
        self.tail = temp
        self.num_of_data = 0  #현재 link에 연결된 노드의 수

    # append 메소드 (insert - 맨 뒤에 노드 추가, tail과 node의 next, 데이터 개수 변경)
    def append(self, name, time):
        new_node = Node(name, time)
        self.tail.link = new_node
        self.tail = new_node
        self.num_of_data += 1

def erase(string):
    idx = string.find("(")
    #print(idx)
    if(idx==-1):
        return string
    else:
        return string[0:idx]
# 괄호 제거

class Subway():
    def __init__(self,x):#x호선
        self.line=subway_all[subway_all["호선"]==str(x)+"호선"].reset_index(drop=True) #x호선 dataframe
        self.dic={}
        for i in range(len(self.line)):#역 갯수
            Llist = LinkedList(erase(self.line.loc[i, "역명"]))
            if i != 0:  # 시작 역
                Llist.append(erase(self.line.loc[i - 1, "역명"]), self.line.loc[i, "시간(분)"])
            if i != (len(self.line) - 1):
                Llist.append(erase(self.line.loc[i + 1, "역명"]), self.line.loc[i + 1, "시간(분)"])
            self.dic[erase(self.line.loc[i, "역명"])] = Llist
        for i in self.dic.keys():
            if i not in roadMap:
                roadMap[i] = {}
            # print("기준역: ", i)
            tempList = self.dic[i].head.link
            for k in range(self.dic[i].num_of_data):
                roadMap[i][tempList.name] = {}
                roadMap[i][tempList.name]["시간"] = tempList.time
                roadMap[i][tempList.name]["호선"] = self.line.loc[0, "호선"]
                # print(tempList.name)
                tempList = tempList.link

def makeSubway():#1~8호선 line, dic 선언
    for x in range(1, 9):  # 일단 한번씩 선언
        line.append(Subway(x).line)  # DataFrame
        line_dic.append(Subway(x).dic)  # dictionary


makeSubway()

#예외 역들 처리
roadMap["구로"]["가산디지털단지"] = {'시간': 2.0, '호선': '1호선'}
roadMap["온수"].pop("구로")

roadMap["성수"]["뚝섬"] = {'시간': 1.0, '호선': '2호선'}
roadMap["성수"]["건대입구"] = {'시간': 2.0, '호선': '2호선'}
roadMap["성수"].pop("시청")

roadMap["시청"]["을지로입구"] = {'시간': 2.0, '호선': '2호선'}
roadMap["시청"].pop("성수")

roadMap["신도림"].pop("신설동")

roadMap["신설동"].pop("신도림")

roadMap["상일동"].pop("강동")

roadMap["강동"].pop("상일동")
roadMap["강동"]["천호"] = {'시간': 2.0, '호선': '5호선'}
roadMap["강동"]["길동"] = {'시간': 2.0, '호선': '5호선'}

roadMap["응암"]["역촌"] = {'시간': 3.0, '호선': '6호선'}
roadMap["응암"].pop("구산")

roadMap["역촌"].pop("응암")

roadMap["불광"].pop("역촌")

roadMap["독바위"].pop("불광")

roadMap["연신내"].pop("독바위")

roadMap["구산"].pop("연신내")

roadMap["을지로4가"]["동대문역사문화공원"] = {'시간': 2.0, '호선': '2호선'}
roadMap["동대문역사문화공원"]["을지로4가"] = {'시간': 2.0, '호선': '2호선'}   #2,5호선이 둘다 지남... 5호선 구간은 포기하자 

def newWay():
    for i in roadMap.keys():
        fastWay[i]={"1호선":[0, 99999999, [], 0],      # -> 방문 여부, 최단거리, 경로, 역이 해당 호선에 연결되어 있는지 여부!!
                    "2호선":[0, 99999999, [], 0],
                    "3호선":[0, 99999999, [], 0],
                    "4호선":[0, 99999999, [], 0],
                    "5호선":[0, 99999999, [], 0],
                    "6호선":[0, 99999999, [], 0],
                    "7호선":[0, 99999999, [], 0],
                    "8호선":[0, 99999999, [], 0]}  
        
def findNext():  
    nextPlace = 'noWay'
    min = 99999999
    for i in fastWay.keys():  # i는 역들
        for k in fastWay.get(i).keys():  # k 는 호선들
            if fastWay.get(i)[k][0] == 0 and min > fastWay.get(i)[k][1]:
                nextPlace = i
                min = fastWay.get(i)[k][1]
    return nextPlace

def markingPath(place):  #새로운 place 왕십리, i는 상왕십리 환승을 고려
    for i in roadMap.get(place).keys():    
        tempL = roadMap.get(place).get(i).get("호선") # place -> i 이동 구간의 호선 정보
        fastWay.get(i)[tempL][3] = 1  #연결된 호선임을 표시
        
        if fastWay.get(place)[tempL][3] == 0: # 환승하는 경우!!! 왕십리의 2호선에 연결정보가 없음
            #print("-----환승")
            mintemp = 999999
            st = ""
            for sttemp in fastWay.get(i).keys():    
                if fastWay.get(place)[sttemp][1] < mintemp:
                    mintemp = fastWay.get(place)[sttemp][1]
                    st = sttemp
                
            if fastWay.get(i)[st][0] == 0:# 방문 X!!
                if fastWay.get(i)[tempL][1] >= (fastWay.get(place)[st][1] + roadMap.get(place).get(i).get("시간") + 10):
                
                    fastWay.get(i)[tempL][1] = fastWay.get(place)[st][1] + roadMap.get(place).get(i).get("시간") + 10
                    fastWay.get(i)[tempL][2] = fastWay.get(i)[st][2] + fastWay.get(place)[st][2]
                    fastWay.get(i)[tempL][2].append(i)
                    fastWay.get(i)[tempL][3] = 1

        else:
            if fastWay.get(i)[tempL][0] == 0 and fastWay.get(i)[tempL][1] >= (fastWay.get(place)[tempL][1] + roadMap.get(place).get(i).get("시간")):
                
                fastWay.get(i)[tempL][1] = fastWay.get(place)[tempL][1] + roadMap.get(place).get(i).get("시간")
                fastWay.get(i)[tempL][2] = fastWay.get(i)[tempL][2] + fastWay.get(place)[tempL][2]
                fastWay.get(i)[tempL][2].append(i)
                fastWay.get(i)[tempL][3] = 1  # tempL 호선으로 연결된 역!

def findPath_flask(start, finish):
    newWay()
    for key in fastWay.get(start).keys():  #처음에는 호선을 모르니 일단 전체 dic을 초기화!!
        fastWay.get(start)[key][0]=1#최초 시작점 방문처리
        fastWay.get(start)[key][1]=0#최초 시작점 거리0
        fastWay.get(start)[key][2].append(start)  #시작 경로 추가
        fastWay.get(start)[key][3]=1
        
    markingPath(start)                
    while True:                                             #거리 마킹
        move = findNext() # 다음 가야할곳은 hair
        if move=='noWay':break
        for key in fastWay.get(move).keys():
            fastWay.get(move)[key][0]=1  #vist으로 표시
        markingPath(move)
    for key in fastWay.get(finish).keys():
        if fastWay.get(finish)[key][1] != 99999999:
            path = fastWay.get(finish)[key][2]
            time = fastWay.get(finish)[key][1]
    return path,time

#여기서부터 혼잡도 관련 코드
def can_I_sit(day,name, time): #앉을확률 계산

    congestion_data = pd.read_csv('C:/Users/user/Desktop/자료구조 최종발표 코드/혼잡도 현황(2015년).csv',encoding='euc-kr', engine='python') #혼잡도 관련 정보(1-4호선)

    name_list=congestion_data[['역명']]
    if len(name_list[name_list['역명']==name]):
        pass
    else:
        return "해당 역의 혼잡도 정보가 없습니다"
    
    congestion_data=congestion_data[congestion_data['사용일']==day]
    name_list=congestion_data[['역명']]
    
    congestion_data=congestion_data[congestion_data['역명']==name]
    
    to_where_f=congestion_data['구분'].tolist()[0]
    first=congestion_data[time].tolist()[0] #각 열차마다 2가지 방향이 있으므로 first, second로 구분해준다.

    to_where_s=congestion_data['구분'].tolist()[1]
    second=congestion_data[time].tolist()[1]

    result_1 = to_where_f +"인 열차의 혼잡도는" +str(first)+"입니다."
    result_2 = to_where_s +"인 열차의 혼잡도는" +str(second)+"입니다."

    #혼잡도 관련 계산
    pre_human= first*1.6 #현재 열차의 사람 수 
    can_seat=round((42-(pre_human))/42 *100,2) #round():소수점 2자리로 , 앉을 수 있는 확률
    can_hand= round((92-(pre_human-42))/92 *100,2) # 손잡이를 잡을 수 있는 확률

    if can_seat>=0:
        result_1=to_where_f +"인 열차에서 앉을 확률은" +str(can_seat)+"입니다."
    elif can_hand>=0:
        result_1=to_where_f +"인 열차에서 손잡이라도 잡을 확률은" +str(can_hand)+"입니다."
    else:
        result_1=to_where_f +"에서 그냥 서서 가십시오."

    pre_human= second*1.6
    can_seat=round((42-(pre_human))/42 *100,2)
    can_hand=round((92-(pre_human-42))/92 *100,2)

    if can_seat>=0:
        result_2=to_where_s +"인 열차에서 앉을 확률은" +str(can_seat)+"입니다."
    elif can_hand>=0:
        result_2=to_where_s +"인 열차에서 손잡이라도 잡을 확률은" +str(can_hand)+"입니다."
    else:
        result_2=to_where_s +"에서 그냥 서서 가십시오."
    
    return result_1+" "+result_2

from datetime import datetime #현재시간을 받아오기 위함.

def percent_flask(start):
    now=datetime.now()
    now_day = now.weekday() # 월==0
    now_hour=now.hour

    if now_day<6:
        now_day_str="평일"
    elif now_day==5:
        now_day_str="토요일"
    else:
        now_day_str="일요일"
    time=now_hour #자료형 int
    if time>5 and time<24:
        time=str(now_hour)+":00"
        return can_I_sit(now_day_str,start,time)
    elif time==0:
        time="0:00"
        return can_I_sit(now_day_str,start,time)
    else:
        return "열차가 없습니다.."

lat_lng_data=pd.read_csv('C:/Users/user/Desktop/자료구조 최종발표 코드/서울시 역코드로 지하철역 위치 조회 (1).csv',encoding='utf-8',engine='python',header=None,skiprows=1)
#역 정보가 담긴 csv파일을 읽어옴

lat_lng_data=lat_lng_data[[1,7,8]] # 전철역명=1, X좌표=7, Y좌표=8

#경도위도 보내주는 함수
def save_path(path):
    X_Y=[] 

    for x in path:
        dict={} #경도 위도의 정보를 담는 dictionary 

        try:
            lat=lat_lng_data.loc[lat_lng_data[1]==x,7].tolist()[0] #역 하나에 여러 호선이 존재하는데, 역 위치는 같으므로 첫번째 정보를 저장
            lng=lat_lng_data.loc[lat_lng_data[1]==x,8].tolist()[0]
        except IndexError:
            return "해당역 위치 정보가 존재하지않습니다."

        dict['lat']=lat
        dict['lng']=lng

        X_Y.append(dict)
    return str(X_Y).replace('\'','')
