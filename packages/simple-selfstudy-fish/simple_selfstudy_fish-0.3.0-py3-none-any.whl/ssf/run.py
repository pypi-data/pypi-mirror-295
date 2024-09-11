import os
from sklearn.neighbors import KNeighborsClassifier
import random
import pandas as pd

def ping():
    return "pong"

def functionStart():
	# 시작시, 화면에 다음과 같은 내용을 출력
	# """
	#
	#
	# Selfstudy Fish Model
	# 							Version 1.0.0
	#
	#
	# 물고기의 길이를 입력해 주세요. (단위 : cm)
	# Length : 
	## 입력 후
	# 물고기의 무게를 입력해 주세요. (단위 : kg)
	# Weight :
	# """
	#
	## 입력 후
	#
	# selfstudy를 위한 기존 저장된 정보 호출
	# 없을시 임의 랜덤으로 진행
	#
	# selfstudy의 결과를 prediction에 저장하여 확인 질의 진행
	# """
	# 입력하신 정보를 토대로 추론한 물고기의 종류는 {prediction} 으로 예상됩니다.
	# 이 프로그램의 추론이 맞습니까? (yes/no)
	# """
	## 입력 후
	# 테스트 결과를 저장 한 다음, 질의를 이어갈지, 종료할지 문의하는 화면
	# 해당 결과에 따라 화면 변동
	recordData = []
	while(True):
		
		print("""


		Selfstudy Fish Model
									Version 0.2.0


		물고기의 길이를 입력해 주세요. (단위 : cm)

		""")
		length = input("Length : ")
		print("""
		물고기의 무게를 입력해 주세요. (단위 : kg)

		""")
		weight = input("weight : ")
		prediction = selfstudy(length = length, weight = weight)
		while(True):
			print(f"""
			입력하신 정보를 토대로 추론한 물고기의 종류는 {prediction}으로 예상됩니다.
			이 프로그램의 추론이 맞습니까? (yes/no)
			""")
			answer = input()
			if answer == "yes":
				print("""
				추론 성공, 해당 정보를 기록합니다.
				""")
				recordData.append({'length' : length, 'weight' : weight, 'target' : answer})
				break
			elif answer == "no":
				print("""
				추론 실패, 정답을 입력해 주십시오.
				Mullet 	/ 숭어 : 0
				Salmon 	/ 연어 : 1
				Tuna	/ 참치 : 2
				""")
				answer = input()
				recordData.append({'length' : length, 'weight' : weight, 'target' : answer})
				break
			else:
				print("""
				입력 오류
				다시 입력해 주십시오.
				""")


		print("""
		추론을 계속 이어가시겠습니까? yes를 제외한 입력은 모두 종료처리됩니다.
		""")
		answer = input()
		if answer == "yes":
			continue
		else:
			break
	
	save_parquet(recordData = recordData)
	print("""
	Selfstudy Fish Model을 종료합니다.
	""")

def selfstudy(length: float, weight: float):
	# length와 weight를 입력받고 거기에 대한 prediction을 리턴함
	# 호출시 '~/data/fishmodel' 디렉토리를 우선 생성
	# 정상적으로 생성이 되면 데이터가 없는 상태이므로 임의의 값을 반환
	# 디렉토리가 이미 존재해 안에 data.parquet 파일이 존재하는 경우 해당 값을 읽어들여와서
	# 자가학습을 진행함.
	# 자가학습이 완료될 경우 추론값을 반환한다.
	parquetdir = find_dir()
	if parquetdir == -1:
		# 디렉토리 생성
		# 임의의 값 반환
		path = "~/data/fishmodel"
		rpath = os.path.expanduser(path)
		os.makedir(rpath)
		randompredictfish = ["Salmon", "Mullet", "Tuna"]
		return random.choice(randompredictfish)
		
	elif parquetdir == 0:
		# 임의의 값 반환
		randompredictfish = ["Salmon", "Mullet", "Tuna"]
		return random.choice(randompredictfish)

	else:
		# parquet 파일 읽어서 자가학습
		df = pd.read_parquet(parquetdir)
		if len(df) < 11:
			randompredictfish = ["Salmon", "Mullet", "Tuna"]
			return random.choice(randompredictfish)
		df['length'] = df['length'].astype(float)
		df['weight'] = df['weight'].astype(float)
		df['target'] = df['target'].astype(int)


		fishData = df[['length', 'weight']]
		fishTarget = df['target']
		kn = KNeighborsClassifier()
		kn.fit(fishData, fishTarget)

		predictData = kn.predict([[float(length), float(weight)]])
		if predictData == 0: 
			# Mullet / 숭어
			return "Mullet"
		elif predictData == 1: 
			# Salmon / 연어
			return "Salmon"
		else: 
			# Tuna / 참치
			return "Tuna"
	
	
def find_dir():
	# selfstudy에서 호출하는 함수.
	# 호출시 '~/data/fishmodel' 디렉토리를 찾고, data.parquet 파일을 로드해서 리턴한다.
	# 단, 디렉토리가 없는경우 -1을 리턴하고
	# 파일이 없는경우는 0을 리턴한다.
	# data.parquet 파일이 정상적으로 확인되면 해당 경로를 리턴
	path = "~/data/fishmodel/data.parquet"
	rpath = os.path.expanduser(path)
	if not os.path.isdir(os.path.dirname(rpath)):
		return -1
	if not os.path.isfile(rpath):
		return 0
	return rpath

def save_parquet(recordData):
	# 추론 종료시 호출되는 함수
	# 호출시 data.parquet 파일을 찾고 없을경우 생성
	# 입력받은 리스트를 파일 삽입 후 저장
	# 반환값 없음
	
	path = "~/data/fishmodel/data.parquet"
	wpath = os.path.expanduser(path)
	if not os.path.isfile(wpath):
		df = pd.DataFrame(recordData)
		df.to_parquet(wpath)
	else:
		df = pd.DataFrame(recordData)
		e_df = pd.read_parquet(wpath)
		u_df = pd.concat([e_df, df], ignore_index = True)
		u_df.to_parquet(wpath)




functionStart()
