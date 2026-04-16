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
        """저장된 모든 퀴즈를 순차적으로 출제하고 최종 점수를 계산합니다."""
        if not self.data.get('quizzes'):
            print("\n❌ 등록된 퀴즈가 없습니다.")
            return

        print("\n" + "="*40)
        print("🎬 영화 퀴즈 게임을 시작합니다!")
        print("="*40)
        
        score = 0  # 맞춘 개수를 저장할 변수 초기화
        quizzes = self.data['quizzes']
        total = len(quizzes)  # 전체 문제 수

        # 1. for 루프를 사용하여 모든 문제를 하나씩 순회
        for idx, quiz in enumerate(quizzes, 1):
            print(f"\n[문제 {idx} / {total}]")
            print(f"카테고리: {quiz.get('category', '미분류')}")
            print(f"질문: {quiz['question']}")
            
            print("\n< 보기 >")
            for i, option in enumerate(quiz['options'], 1):
                print(f"{i}. {option}")
            
            # 2. 사용자 입력 및 정답 확인
            # --- [8단계 핵심: 유효한 입력이 들어올 때까지 반복] ---
            while True:
                user_input = input("\n👉 정답 번호를 입력하세요 (1~4): ")
                
                try:
                    # 1. 정수 변환 시도 (문자 입력 시 ValueError 발생)
                    choice_num = int(user_input)
                    
                    # 2. 숫자 범위 유효성 검사 (보기 번호 안에 있는지 확인)
                    if 1 <= choice_num <= len(quiz['options']):
                        # 유효한 입력이므로 반복문 탈출
                        break
                    else:
                        print(f"⚠️ {1}번부터 {len(quiz['options'])}번 사이의 숫자를 입력해 주세요.")
                except ValueError:
                    # 숫자가 아닌 문자가 들어왔을 때의 처리
                    print("⚠️ 잘못된 입력입니다. '숫자'만 입력할 수 있습니다.")
            
            # 3. 정답 판별 (이미 검증된 choice_num 사용)
            # [11단계] 정답 판별 및 피드백 로직 개선
            if choice_num == quiz['answer']:
                print(f"✅ 정답입니다!")
                score += 1
            else:
                # 틀렸을 때 정답 번호를 알려주고 바로 아래에서 해설(힌트)을 출력
                print(f"❌ 틀렸습니다. 정답은 {quiz['answer']}번입니다.")
            
            # 정답/오답 여부에 관계없이 해당 문제에 대한 보충 설명(힌트)을 제공
            # 이는 사용자가 틀린 문제에 대해 즉각적인 피드백을 얻게 함으로써 학습 효과를 높임
            print(f"💡 추가 설명(힌트): {quiz['description']}")
            
            print("-" * 40)

        # 3. 최종 결과 출력 (점수 계산)
        final_percentage = int((score / total) * 100)
        print(f"\n종료! 당신의 최종 점수는 {final_percentage}점입니다.")
        print(f"총 {total}문제 중 {score}문제를 맞히셨습니다.")

        # (6단계 최종 결과 출력 코드 바로 뒤에 추가하였음)
        self.finalize_game(final_percentage)

    def save_data(self):
        """
        [7단계] 변경된 데이터(최고 점수 등)를 JSON 파일에 영구적으로 저장합니다.
        메모리상의 딕셔너리를 물리적 파일로 옮기는 '직렬화(Serialization)' 과정입니다.
        """
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                # ensure_ascii=False: 한글이 깨지지 않게 저장
                # indent=2: 가독성을 위해 들여쓰기 적용
                json.dump(self.data, f, ensure_ascii=False, indent=2)
            print("💾 데이터가 안전하게 저장되었습니다.")
        except Exception as e:
            print(f"❌ 저장 중 오류 발생: {e}")

    def finalize_game(self, final_percentage):
        """
        [7단계] 게임 종료 후 점수를 비교하고 필요시 최고 점수를 갱신합니다.
        """
        current_high = self.data.get('high_score', 0)
        
        print(f"\n현재 점수: {final_percentage}점 / 기존 최고 점수: {current_high}점")
        
        # 현재 점수가 기록보다 높으면 데이터 갱신 및 파일 저장
        if final_percentage > current_high:
            print("🎊 축하합니다! 새로운 최고 기록입니다!")
            self.data['high_score'] = final_percentage
            self.save_data() # 변경된 내용을 파일에 기록
        else:
            print("💡 최고 기록 경신에 실패했습니다. 조금 더 분발해 보세요!")

    def add_quiz(self):
        """
        [9단계] 사용자가 새로운 퀴즈를 입력하여 시스템에 추가하는 기능입니다.
        입력받은 데이터를 구조화하여 리스트에 추가하고 파일에 저장합니다.
        """
        print("\n" + "+" * 40)
        print("➕ 새로운 영화 퀴즈 추가")
        print("+" * 40)

        # 1. 정보 입력 받기
        category = input("카테고리 (예: 영화, 배우, 명대사): ")
        question = input("퀴즈 질문을 입력하세요: ")
        
        options = []
        for i in range(1, 5):
            opt = input(f"보기 {i}번: ")
            options.append(opt)
            
        # 2. 정답 번호 유효성 검사 (8단계에서 배운 try-except 활용)
        while True:
            try:
                answer = int(input("정답 번호 (1~4): "))
                if 1 <= answer <= 4:
                    break
                else:
                    print("⚠️ 1에서 4 사이의 숫자를 입력해 주세요.")
            except ValueError:
                print("⚠️ 숫자만 입력 가능합니다.")
                
        description = input("정답에 대한 간단한 해설: ")

        # 3. 데이터 구조화 (딕셔너리 생성)
        new_quiz = {
            "id": len(self.data['quizzes']) + 1,  # 자동 ID 부여
            "category": category,
            "question": question,
            "options": options,
            "answer": answer,
            "description": description
        }

        # 4. 리스트에 추가 및 파일 저장 (7단계 save_data 재사용)
        self.data['quizzes'].append(new_quiz)
        self.save_data()
        print("\n✅ 새로운 퀴즈가 성공적으로 추가되었습니다!")

    def view_quizzes(self):
        """
        [10단계] 현재 시스템에 저장된 모든 퀴즈의 목록을 출력합니다.
        데이터 리스트를 순회하며 주요 정보를 가독성 있게 표현합니다.
        """
        quizzes = self.data.get('quizzes', [])
        
        if not quizzes:
            print("\n❌ 저장된 퀴즈가 없습니다.")
            return

        print("\n" + "=" * 50)
        print(f"{'ID':<4} | {'카테고리':<8} | {'퀴즈 질문'}")
        print("-" * 50)

        for q in quizzes:
            # f-string의 정렬 기능을 사용하여 표(Table) 형식으로 출력
            print(f"{q['id']:<4} | {q.get('category', '미분류'):<8} | {q['question']}")
        
        print("=" * 50)
        print(f"총 {len(quizzes)}개의 퀴즈가 저장되어 있습니다.")

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
            game.add_quiz() # 구현 중 메시지 대신 메서드 호출로 변경
        elif choice == '3':
            game.view_quizzes() # 구현 중 메시지 대신 메서드 호출
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