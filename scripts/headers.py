import csv
import json

FILE_INPUT = 'res/Headers.csv'
FILE_OUTPUT_PREFIX = 'res/Headers'

def transform_name(f: str):
	# '-'를 '_'로 바꾸고 소문자를 대문자로 변환
	return f.replace('-', '_').upper()

with open(FILE_INPUT, mode='r', encoding='utf-8') as f:
	reader = csv.reader(f)
	rows = list(reader)

# JSON 데이터를 저장할 딕셔너리
name2env = {}
env2name = {}

common = []
content = []
request = []
response = []
cors = []
ws = []
etc = []

# 두 번째 필드의 값을 변환하여 첫 번째 필드에 입력
for row in rows[1:]:
	env = transform_name(row[0])
	name2env[row[0]] = env
	env2name[env] = row[0]
	if row[1] == 'Common': common.append('{} # {}'.format(row[0], env))
	elif row[1] == 'Content': content.append('{} # {}'.format(row[0], env))
	elif row[1] == 'Request': request.append('{} # {}'.format(row[0], env))
	elif row[1] == 'Response': response.append('{} # {}'.format(row[0], env))
	elif row[1] == 'CORS': cors.append('{} # {}'.format(row[0], env))
	elif row[1] == 'WebSocket': ws.append('{} # {}'.format(row[0], env))
	else: etc.append('{} # {}'.format(row[0], env))

# JSON 파일로 저장
with open('{}.env.json'.format(FILE_OUTPUT_PREFIX), mode='w', encoding='utf-8') as f:
	json.dump(name2env, f, indent=2, ensure_ascii=False)
with open('{}.name.json'.format(FILE_OUTPUT_PREFIX), mode='w', encoding='utf-8') as f:
	json.dump(env2name, f, indent=2, ensure_ascii=False)
with open('{}.common.json'.format(FILE_OUTPUT_PREFIX), mode='w', encoding='utf-8') as f:
	json.dump(common, f, indent=2, ensure_ascii=False)
with open('{}.content.json'.format(FILE_OUTPUT_PREFIX), mode='w', encoding='utf-8') as f:
	json.dump(content, f, indent=2, ensure_ascii=False)
with open('{}.request.json'.format(FILE_OUTPUT_PREFIX), mode='w', encoding='utf-8') as f:
	json.dump(request, f, indent=2, ensure_ascii=False)
with open('{}.response.json'.format(FILE_OUTPUT_PREFIX), mode='w', encoding='utf-8') as f:
	json.dump(response, f, indent=2, ensure_ascii=False)
with open('{}.cors.json'.format(FILE_OUTPUT_PREFIX), mode='w', encoding='utf-8') as f:
	json.dump(cors, f, indent=2, ensure_ascii=False)
with open('{}.ws.json'.format(FILE_OUTPUT_PREFIX), mode='w', encoding='utf-8') as f:
	json.dump(ws, f, indent=2, ensure_ascii=False)
with open('{}.unknown.json'.format(FILE_OUTPUT_PREFIX), mode='w', encoding='utf-8') as f:
	json.dump(etc, f, indent=2, ensure_ascii=False)
