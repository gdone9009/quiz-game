import json  # JSON 형식의 데이터를 처리하기 위한 표준 라이브러리 임포트
import os    # 파일 경로 존재 여부 등 시스템 환경 확인을 위한 라이브러리 임포트

class QuizGame:
    """
    퀴즈 게임의 전체 로직을 관리하는 클래스.
    데이터의 로드, 저장, 게임 실행 등 모든 기능을 캡슐화(Encapsulation)하여 관리함.
    """
    def __init__(self, data_file='state.json'):
        """
        인스턴스 초기화 메서드.
        :param data_file: 퀴즈 데이터가 저장된 JSON 파일의 경로
        """
        self.data_file = data_file
        
        # 프로그램 시작과 동시에 저장된 데이터를 메모리로 불러오는 메서드 호출
        self.load_data()

    def load_data(self):
        """
        하드디스크의 JSON 파일을 읽어 파이썬 객체(Dictionary)로 변환하는 메서드.
        이 과정은 '데이터 영속성(Persistence)'을 구현하는 핵심 단계임.
        """
        # 1. 파일 존재 여부 확인 (방어적 프로그래밍: 파일이 없어서 발생하는 에러 방지)
        if os.path.exists(self.data_file):
            # 2. 파일 열기 (with 문을 사용하여 파일 처리가 끝나면 자동으로 닫히도록 관리)
            with open(self.data_file, 'r', encoding='utf-8') as f:
                # 3. json.load()를 통해 텍스트(JSON)를 파이썬 딕셔너리로 변환(Deserialization)
                self.data = json.load(f)
            
            # 4. 로드 완료 후 현재 상태를 콘솔에 출력하여 디버깅 및 사용자 확인 유도
            print(f"✅ 데이터를 성공적으로 불러왔습니다.")
            print(f"📊 현재 저장된 최고 점수: {self.data.get('high_score', 0)}점")
            print(f"📚 등록된 총 퀴즈 수: {len(self.data.get('quizzes', []))}문항")
        else:
            # 파일이 없을 경우 프로그램이 멈추지 않도록 기본 데이터 구조 초기화
            print("⚠️ 데이터 파일이 존재하지 않습니다. 새로운 환경을 구성합니다.")
            self.data = {"high_score": 0, "quizzes": []}

if __name__ == "__main__":
    # QuizGame 클래스의 인스턴스를 생성하여 프로그램 실행의 기점을 만듦
    game = QuizGame()