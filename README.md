# JunmyeongBot
![Framework1](https://user-images.githubusercontent.com/48518274/124345635-24843480-dc15-11eb-83e5-c3ff8257d2ea.png)



## 1. 목적

**2020년**

1. 학내공지 확인
   - 접근성이 떨어지는 학내 공지를 대체하여 telegram으로 확인할 수 있도록 함.
2. 개발 관련 기술에 대한 지식 확보
   - API call
   - Web crawling
   - etc..(ex. Telegram chatbot handler)
-------

**2021년**

3. NLP기술에 대한 practical한 이해(새로운 목표)
   - 2021년부터 NLP관련 학습을 시작하면서, NLP에 대한 이해를 높일 필요가 있음을 알게 됨.
   - huggingface 라이브러리 + pytorch를 이용한 모델 학습, 테스트 과정 등을 구현.
   - 특히, 대표적 응용 task인 챗봇이 가장 적절할 것이라고 생각하였음.
4. 모델 서빙에 대한 사전 학습
   - 모델 서빙에 대해 찍먹하는 수준으로 구현해보고 싶었음.
   - BentoML, Flask를 연동하는 방법 등이 있었지만, 현재로서 가장 간편하다고 생각되는 torchserve로 서빙하기로 결정하였음.
5. ~~이야기해줄 친구 만들기~~

## 2. 사용 기술
- 챗봇 프레임워크 : Telegram
  - [Python 텔레그램 봇](https://github.com/python-telegram-bot/python-telegram-bot) 라이브러리 기반으로 구현
- crawling관련 : Beautifulsoup 사용
- LM : GPT-2
  - SKI-AI의 KoGPT-2를 한국어 상담심리 데이터셋으로 fine-tuning하여 사용하였음.
- 모델 서빙 : torchserve
  - torchserve 공식 웹사이트, 튜토리얼 기반으로 서빙하였음.
  - AWS의 p2.xlarge 인스턴스를 사용하여 GPU기반 추론을 실시하도록 했다.



## 3. 작동 데모





## 4. TO-DO
- [ ] serving관련 지식 공부해서 더 확장성있는 코드 만들기
- [ ] 더 큰 한국어 대화 데이터셋을 이용해서 더 현실감있는 답변 생성할 수 있도록 GPT tuning
- [ ] 학내공지 crawling외에도 다양한 기능을 지원할 수 있도록 만들자


## 5. 참고 자료

- [한승운님의 coronabot 제작기](https://velog.io/@swhan9404/series/telegram-corona)
- [AWS Lambda 활용 사례](https://aws.amazon.com/ko/blogs/korea/serverless-architecture-by-korean-developers/)
- [전체 공지 API 만들기](https://jojoldu.tistory.com/308?fbclid=IwAR1CBbcV1ONgskOFRXznf8sUgdpMm0V1cGIUHCjJUX61Dwe6PUTUKlxBbqM)
- [개발 환경 셋팅](https://stackoverflow.com/questions/54198412/developing-using-pycharm-in-docker-container-on-aws-instance)
- https://exagen.tistory.com/notice/63

