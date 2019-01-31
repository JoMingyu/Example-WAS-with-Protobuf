# Protobuf-Practice
Protobuf는 구글에서 만든 serialized format인데, proto라는 언어로 스키마를 작성해서 따로 파일로 관리하고, 이걸 컴파일해서 DTO 뚝딱 만들고 합니다. 괜찮아 보이길래 한번 써보고 싶어서 샘플 WAS를 만드는 레포입니다. 본인의 [Flask-Large-Application-Example](https://github.com/JoMingyu/Flask-Large-Application-Example) 기반으로 작업하고, request/response 메시지 관리는 protobuf 씁니다.

- Python
- Flask
- pipenv
- Peewee & MySQL
- Protobuf

## WAS
요만큼 만들겠습니다.

- 회원가입
- 로그인
- 글 작성
- 글 목록 불러오기

테스트 안짤겁니다.

## 아 이렇게 하는거구나
1. 일단 protobuf compiler를 설치한다. [ㄱㄱ](https://github.com/protocolbuffers/protobuf/releases)
2. 원하는 곳에다가 .proto 파일을 만든다. [튜토리얼](https://developers.google.com/protocol-buffers/docs/pythontutorial) 보면서 대충 때려맞추면 됨.
3. protobuf compiler로 컴파일을 한다. 여기서는 `protoc --python_out=. post.proto`같은 식으로 했음.
4. 그럼 파이썬 모듈이 생긴다! .proto파일 이름 뒤에 `_pb2`가 붙는 형식. `user.proto` -> `user_pb2.py`
5. 거기 있는 클래스 가지고 지지고볶고 하면 된다.
```python
from flask_jwt_extended import create_access_token
from app.views.user.user_pb2 import SignupRequest
from app.views.user.user_pb2 import AuthResponse

# Deserialize
instance = SignupRequest()
instance.ParseFromString(b'\n\x03abc\x12\x03def\x1a\x06mingyu')
print(instance.id, instance.pw, instance.name)  # abc def mingyu

# Serialize
response = AuthResponse(
    accessToken=create_access_token(...)
)
print(response.SerializeToString())  # b'\n\x8f\x02eyJ0eXAiOiJKV1QiLCJhbGciOiJ...'

```

## 아니 이건 좀;;;
- protobuf3에선 required가 사라졌다.
- protobuf 3.6.1버전은 DDL load failed가 뜬다. tensorflow에 이슈가 많이 올라와 있음.
- type hinting을 어떻게 해야 할지 모르겠다. 컴파일하고 나면 그냥 간단한 형태의 DTO가 정의되는 줄 알았건만 리플렉션하고 뭐하고 난리났다. 이건 좀 디깅해봐야할 것 같다.
- serialize하고 난 후의 proto message는 사람이 읽을 수가 없다. 그냥 보기 어려운 걸 떠나서 JSON처럼 타이핑으로 테스트용 데이터를 만들 수가 없음. 굳이 소스코드 레벨에서 message 객체 만들고 serialize해서 복사해야 함;; Protobuf message generator online 이런거 있으면 좋겠다.
- validation 용도로 스키마를 작성하고 싶은데, 방법이 없을까? int 타입에 min value/max value, string 타입에 regex같은거 넣을 수 있으면 좋을텐데. 내가 못 찾는건가..
- content type 표준이 없다. 여기서는 `application/vnd.google.protobuf` 쓰고 있음.
- protoc 컴파일 귀찮다.. ㅜㅜ

## 결론
1. .proto 파일 갖다가 컴파일 돌리면 DTO 만들어주는 건 아이디어 진짜 좋다고 생각했다. 특히 안드로이드에서도 된다는게..
2. validation rule을 넣을 수 있는 방법이 있으면 좋을 것 같다. 그렇게 되면 정말 .proto 파일 정의하는 거 하나만으로 DTO + 요청 데이터 validation + 주석 좀 달고 API 문서로도 써먹을 수 있을듯.
3. 개발팀에서 이걸 쓴다고 한다면 러닝커브가 무조건 생길텐데, 러닝커브 때문에 protobuf를 쓰는 걸 포기할 정도는 아닐 것 같다.
4. 근데 굳이 protobuf에 익숙해지려고 노력하고 싶지는 않다. 기대가 컸어서 그런건진 몰라도 WAS 관점에서는 좀 아쉬웠다.
5. flask에서 쓰기 좋게 쪼만한 라이브러리 하나 만들어야겠다.
