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

    # def run_quiz가 QuizGame 클래스 안에 속해 있어야 합니다.
    def run_quiz(self):
        """저장된 퀴즈 데이터를 출력하고 사용자의 정답을 판별합니다."""
        if not self.data.get('quizzes'):
            print("\n❌ 등록된 퀴즈가 없습니다.")
            return

        print("\n" + "-"*40)
        print("🎬 영화 퀴즈를 시작합니다!")
        
        # [4단계 복습] 첫 번째 문제 가져오기
        quiz = self.data['quizzes'][0]
        
        print(f"\n[카테고리: {quiz.get('category', '미분류')}]")
        print(f"질문: {quiz['question']}")
        
        print("\n< 보기 >")
        for i, option in enumerate(quiz['options'], 1):
            print(f"{i}. {option}")
        
        print("\n" + "-"*40)

        # --- [5단계 신규 로직 시작] ---
        
        # 1. 사용자로부터 정답 입력 받기
        # input()은 항상 '문자열'로 받기 때문에 숫자로 비교하려면 int() 변환이 필요함
        user_input = input("👉 정답 번호를 입력하세요: ")
        
        # 2. 정답 판별 로직
        # 사용자가 입력한 값(user_input)과 실제 정답(quiz['answer'])을 비교
        # 데이터의 answer는 숫자형이므로 int(user_input)으로 형변환 후 비교함
        try:
            if int(user_input) == quiz['answer']:
                print(f"\n✅ 정답입니다! ({quiz['description']})")
            else:
                print(f"\n❌ 틀렸습니다. 정답은 {quiz['answer']}번입니다.")
        except ValueError:
            # 숫자가 아닌 문자를 입력했을 경우를 대비한 최소한의 예외 처리
            print("\n⚠️ 숫자 번호로 입력해 주세요!")
            
        print("-" * 40)

def main():
    """
    프로그램의 진입점(Entry Point).
    사용자 인터페이스(CLI)를 제공하고 사용자의 선택에 따라 클래스의 메서드를 호출함.
    """
    # 1. 퀴즈 게임 인스턴스 생성 (이때 내부적으로 load_data가 호출됨)
    game = QuizGame()
    
    # 2. 무한 루프 시작: 사용자가 종료를 선택할 때까지 프로그램은 계속 실행됨
    while True:
        print("\n" + "="*40)
        print("🚀 Git과 함께하는 Python 영화 퀴즈 게임")
        print("="*40)
        print("1. 퀴즈 풀기 시작")
        print("2. 새로운 퀴즈 추가")
        print("3. 현재 퀴즈 목록 보기")
        print("4. 프로그램 종료")
        print("="*40)
        
        # 3. 사용자로부터 메뉴 선택 입력 받음
        choice = input("👉 원하시는 메뉴 번호를 입력하세요: ")
        
        # 4. 입력 값에 따른 조건문 처리 (제어 흐름 설계)
        if choice == '1':
            game.run_quiz() # 퀴즈 실행 메서드 호출
        elif choice == '2':
            print("\n🚧 [퀴즈 추가] 기능을 구현 중입니다.")
        elif choice == '3':
            print("\n🚧 [목록 보기] 기능을 구현 중입니다.")
        elif choice == '4':
            # 루프를 탈출하여 프로그램 종료
            print("\n👋 프로그램을 종료합니다. 이용해 주셔서 감사합니다!")
            break
        else:
            # 1, 2, 3, 4 이외의 입력이 들어왔을 때의 예외 처리
            print("\n⚠️ 잘못된 입력입니다. 1번부터 4번 사이의 숫자를 입력해 주세요.")

if __name__ == "__main__":
    # 스크립트가 직접 실행될 때만 main() 함수를 호출함 (모듈화 고려)
    main()