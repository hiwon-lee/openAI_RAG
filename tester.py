import json
question = "국토교통부 사이트에서 주택청약 관련 PDF 파일을 다운로드하고, 이를 heewon2@ewha.ac.kr주소의 이메일로 전송해줘"
# 이스케이프 처리를 위한 백슬래시 추가
def convert_xml_to_html_entities(xml_str):
    # selector 문자열에서 모든 큰따옴표를 \"로 대체
    selector = xml_str.replace(r'\\', "").replace(r"`xml",'').replace(r"`",'')
    print("hello")
    start_search_pos = 0
    print(selector)

    while True:
        # "Selector=" 위치 찾기
        title_start = selector.find("Selector=", start_search_pos)
        print(title_start)
        if title_start == -1:
            break  # 더 이상 "Selector="가 없으면 종료

        # "Selector=" 뒤의 값을 찾기 위해 시작 위치를 조정
        title_start += 10  # "Selector="의 길이만큼 건너뛰기
        title_end = selector.find("]\">", title_start)
        print(title_end)
        if title_end == -1:
            
          break  # 잘못된 형식이거나 더 이상 닫는 대괄호가 없으면 종료

        # title 속성 값 추출
        title_value = selector[title_start:title_end]
        print(title_value)
        # title 속성 값에서 <와 >를 &lt;와 &gt;, "를 &quot;로 대체
        # title_value = title_value.replace(r"\&quot;", "&quot;").replace("<", "&lt;").replace(">", "&gt;")

        title_value = title_value.replace('\"', "&quot;").replace("<", "&lt;").replace(">", "&gt;")
        # 수정된 title 값을 사용해 selector 문자열 재구성
        print(f"바뀐값 : {title_value}")

        selector = selector[:title_start] + title_value + selector[title_end:]

        # 다음 "Selector="를 찾기 위해 검색 시작 위치 조정
        start_search_pos = title_end

    return selector



# 저장한 JSON 파일을 읽어오는 함수
def read_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
    return data



# file_path = "D:/content/blueAI_createdJson/"+question+".json"
# print(file_path)

# # 1. 저장한 파일을 읽어옴
# json_data = read_json(file_path)

# # 2. Xaml의 값을 가져옴
# xmlVal = json_data.get("Xaml", "")

# # 3. XML 데이터를 HTML 엔티티로 변환
# converted_xml_data = convert_xml_to_html_entities(xmlVal)



# 저장한 JSON 파일을 읽어오는 함수
def read_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
    return data

# JSON 파일을 다시 저장하는 함수
def save_json(file_path, data):
    with open(file_path, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=2)
    print(f"JSON 파일이 {file_path}에 저장되었습니다.")

# 파일 경로 설정 (여기서는 예시로 '/content/blueAI_createdJson/네이버에서 사과를 검색해줘.json'로 가정)
# 파일 경로 설정 (D 드라이브의 content 폴더 내에 위치)
output_directory = "D:/content/blueAI_createdJson/"+question+".json"
# file_path = os.path.join(output_directory, question)
file_path = "D:/content/blueAI_createdJson/"+question+".json"

# 1. 저장한 파일을 읽어옴
json_data = read_json(file_path)

# 2. Xaml의 값을 가져옴
xmlVal = json_data.get("Xaml", "")

# 3. XML 데이터를 HTML 엔티티로 변환
converted_xml_data = convert_xml_to_html_entities(xmlVal)

# 4. 변환된 데이터를 다시 Xaml에 저장
json_data["Xaml"] = converted_xml_data

# 5. 변경된 데이터를 다시 JSON 파일로 저장
save_json(file_path, json_data)