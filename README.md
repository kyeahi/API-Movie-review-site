<!-- # movie
## movie
### movie
movie**movie**movie

- 점으로나올려나
-----------------------------
![](https://steemit.com/images/favicons/apple-touch-icon-57x57.png) 이러고 쓰면?

[이거링크](https://github.com/kyeahi/movie/blob/master/board/forms.py)
 -->



<!-- https://file.mk.co.kr/meet/neds/2021/06/image_readtop_2021_535745_16226846584668330.jpg -->




# 👶프로젝트 소개
- 영화인들을 위한 커뮤니티
- 누구나 해당 영화에대한 평가나 소개등 자유로운 커뮤니티를 할 수 있도록 구현해 놓은 사이트 입니다. 

-------------------------------
## 🤦‍♀️ERD구조
<img src="http://222.100.67.12/Python/img/ERD최종.png" width="450px" height="300px" title="px(픽셀) 크기 설정" alt="RubberDuck"></img><br/>

-------------------------------

## 🎈 형상관리 프로그램

- Git, GitHub
　
-------------------------------

## 🛠사용기술 및 프로그램

- Django
- python
- Pycharm
- MySQL
- REST API
- HTTP통신
- ORM
- HTML
- CSS
- JS

----------------------------------

## 🥨구현 기능
- 회원가입
- 로그인
- 회원 비밀번호 변경
- 회원탈퇴
- 이메일 인증
- 카카오 소셜 로그인
- 구글애널리틱스(방문자 수 출력 기능)
- 커맨트 작성 기능
- 커맨트 수정 및 삭제 기능
- 커맨트 좋아요 기능
- 영화 포스터, 감독, 줄거리, 출연배우 출력
- 영화 좋아요 기능
- 지도 출력



----------------------------------

## ✔ 역할분담


#### 김세진
- 유저 어플리케이션 구현
- 카카오 이메일인증 API
- 백앤드 동작 검수
- 프로젝트 개발환경 구축


#### 송봉기
- 보드 어플리케이션
   구현
- 구글 애널리틱스 API
- 백앤드 동작 검수
- 데이터셋 구축



#### 김선민
- 보드, 커맨트, 유저
  어플리케이션 구현
- 구글 맵 API
- 프론트앤드 구현
- 프론트앤드 동작 검수




#### 김예빈
- 이메일 인증 API
- 보드 어플리케이션 구현
- PPT 작성
- Git 프로젝트 형상관리 
- 백앤드 품질관리



----------------------------------

## 🔥 문제점 및 해결방안


#### 김세진
- 유저 어플리케이션 부분을 맡으면서 함수와 장고 라이브러리 폼을 활용하는것에 어려움이 있었지만, 디버깅을 이용한 오류수정과정을 통해 점진적으로 코딩능력을 개선해나가며 해결했다.
- 그중에 카카오 API 소셜로그인 구현이 가장 어려웠는데 카카오개발자의 문서를 참고하고 데이터 베이스 활용법을 공부하여계정과 데이터 베이스의 연동을 구현할 수 있었다.

#### 송봉기
- 구글 애널리틱스를 구현하면서 어려움이 있었다. 특히 웹상에 적용 정보가 많지 않아 실제 사용화면을 볼 수 없었다. 그렇기 때문에 동작원리 등의 개념을 이해하고 활용하기가 다소  힘들었고, 상황에 맞는 적절한 함수 대입이 어려웠다. 
- 하지만, 다양한 적용방법을 열심히 모색하고, 팀원들과의 협업으로 끝내 문제를 해결하였다.

#### 김선민
- 파이썬에서 구성한 클래스를 DB모델에 Mirgration 하는 과정에서 Migrate가 동작하지 않는 문제가 발생했다. 파이썬의 Mirgration정보제거 방법과 MySQLDB의 django Migration 정보제거 방법을 공부하여 해결하였다.
- Json으로 실시간 좋아요 기능을 구현할 때 DB에는 정보가 들어가지만 HTML 출력기능이 실시간으로 동작하지 않는 문제가 발생하였다. Json 개발자 홈페이지에서 사용법을 공부하고 HTML 동작 연동과정을 디버깅하며 코드 전체를 검수하며 해결하였다.
- 댓글을 작성한 게시글에 댓글이 바로 출력되지 않는 문제가 발생하였다. 객체간 관계형성에 대한 공부를 하고 DB모델 검수하였다. 또한 파이썬함수와 HTML간의 변수 전달과정을 검토하여 해결하였다.
- DB에 이미지를 넣을 수 없는 점, 사용하고픈 이미지를 어느 환경에서든 출력하게 만드는 부분에 문제가 발생하였다. 집 컴퓨터에 웹서버를 열어 원격으로 이미지를 저장하고, DB에 URL을 저장하여 출력하게 하였다.

#### 김예빈
- 이메일 인증 API 부분을 구현하면서 문서를 직접 읽고 코드를 구현하는 점이 제일 흥미로우면서도 어려웠다. 이틀 내내 붙잡고 있었던 것 같다. 게다가 DB와 웹 오류가 자주 발생하였는데, 설상가상으로 코드 데이터가 날라가서 더욱 어려워졌다.
- 하지만 차근차근 문서를 다시 읽어보며 문제를 해결하고자했다. 코드의 문제는 토큰 값을 프런트앤드로 넘겨줄 때, DB에 없는 값을 불러오려고 했던 것이었다. 그래서 인증번호 토큰 값이 일치하면 그 이후에 DB에 이메일을 저장하고, 폼에서 입력한 값과 일치하면 이후에 프런트앤드로 값이 넘어가서 정상적으로 실행하도록 구현하였다. request와 get, redirect 함수가 많이 헷갈렸다. 하지만 이번 기회에 문서를 보며 공부를 하여서 함수의 의미에 대해 잘 알게되었다.



----------------------------------

## ✔ requirments
asgiref==3.4.1
Django==4.0.1
mysqlclient==2.1.0
Pillow==9.0.0
sqlparse==0.4.2
tzdata==2021.5

----------------------------------


## 👓참조
해당 프로젝트는 왓차피디아 사이트를 참조해서 학습용으로 만든 프로젝트입니다
이 코드를 활용하여 이득을 취하거나 무단 배포할 경우 법적으로 문제될 수 있습니다.
