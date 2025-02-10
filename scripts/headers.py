import csv
import json

def transform(f: str):
	# '-'를 '_'로 바꾸고 소문자를 대문자로 변환
	return f.replace('-', '_').upper()

def process_csv(i, o):
	with open(i, mode='r', encoding='utf-8') as f:
		reader = csv.reader(f)
		rows = list(reader)

	# JSON 데이터를 저장할 딕셔너리
	_ = {}
	common = {}
	request = {}
	response = {}
	etc = {}

	# 두 번째 필드의 값을 변환하여 첫 번째 필드에 입력
	for row in rows[1:]:
		row[0]= transform(row[1])
		_[row[0]] = row[1]
		if row[2] == 'Common': common[row[0]] = row[1]
		elif row[2] == 'Request': request[row[0]] = row[1]
		elif row[2] == 'Response': response[row[0]] = row[1]
		else: etc[row[0]] = row[1]

	# 변경된 내용을 다시 저장
	with open('{}.csv'.format(o), mode='w', newline='', encoding='utf-8') as f:
		writer = csv.writer(f)
		writer.writerows(rows)

	# JSON 파일로 저장
	with open('{}.json'.format(o), mode='w', encoding='utf-8') as f:
		json.dump(_, f, indent=2, ensure_ascii=False)
	with open('{}.Common.json'.format(o), mode='w', encoding='utf-8') as f:
		json.dump(common, f, indent=2, ensure_ascii=False)
	with open('{}.Request.json'.format(o), mode='w', encoding='utf-8') as f:
		json.dump(request, f, indent=2, ensure_ascii=False)
	with open('{}.Response.json'.format(o), mode='w', encoding='utf-8') as f:
		json.dump(response, f, indent=2, ensure_ascii=False)
	with open('{}.Unknown.json'.format(o), mode='w', encoding='utf-8') as f:
		json.dump(etc, f, indent=2, ensure_ascii=False)

# CSV 파일 처리
process_csv('res/Headers.csv', 'res/Headers.new')