import json
import os
from quiz import Quiz # quiz.py에서 Quiz 클래스를 가져옴

class QuizGame:
    """
    [컨트롤러 클래스]
    데이터의 로드/저장, 게임 진행, 퀴즈 추가 및 목록 보기 등 전체 흐름을 관리합니다.
    """
    def __init__(self, data_file='state.json'):
        self.data_file = data_file
        self.quizzes = []      # Quiz 객체들을 담을 리스트
        self.high_score = 0    # 최고 점수 기록 변수
        self.load_data()       # 시작과 동시에 기존 데이터 로드

    def load_data(self):
        """[2단계/7단계] JSON 파일을 읽어 메모리에 로드하고 객체로 변환합니다."""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.high_score = data.get('high_score', 0)
                    # [중요] 딕셔너리 형태의 데이터를 Quiz 클래스의 인스턴스로 변환합니다.
                    self.quizzes = [Quiz(**q) for q in data.get('quizzes', [])]
                print(f"✅ 데이터 로드 완료 (최고 점수: {self.high_score}점)")
            except Exception as e:
                print(f"❌ 로딩 중 오류 발생: {e}")
        else:
            print("⚠️ 데이터 파일이 없어 새로운 리스트를 생성합니다.")

    def save_data(self):
        """[7단계] 현재의 퀴즈 리스트와 최고 점수를 JSON 파일로 영구 저장합니다."""
        # 객체 상태인 퀴즈들을 다시 저장 가능한 딕셔너리 형태로 변환합니다.
        quiz_list = [vars(q) for q in self.quizzes]
        data_to_save = {
            "high_score": self.high_score,
            "quizzes": quiz_list
        }
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(data_to_save, f, ensure_ascii=False, indent=2)
        print("💾 파일에 안전하게 저장되었습니다.")

    def run_quiz(self):
        """[6/8/11단계] 퀴즈를 출제하고 정답을 판별하는 메인 로직입니다."""
        if not self.quizzes:
            print("\n❌ 등록된 퀴즈가 없습니다. 먼저 추가해 주세요.")
            return

        print("\n" + "="*40)
        print("🎬 영화 퀴즈 게임을 시작합니다!")
        print("="*40)
        
        score = 0
        total = len(self.quizzes)

        for idx, quiz in enumerate(self.quizzes, 1):
            print(f"\n[문제 {idx} / {total}] 카테고리: {quiz.category}")
            print(f"질문: {quiz.question}")
            
            # 보기 출력
            for i, option in enumerate(quiz.options, 1):
                print(f"{i}. {option}")
            
            # [8단계] 유효한 입력이 들어올 때까지 무한 반복 (예외 처리)
            while True:
                user_input = input("\n👉 정답 번호를 입력하세요 (1~4): ")
                try:
                    choice = int(user_input)
                    if 1 <= choice <= len(quiz.options): break
                    else: print(f"⚠️ 1~{len(quiz.options)} 사이의 숫자를 입력해 주세요.")
                except ValueError:
                    print("⚠️ 잘못된 입력입니다. '숫자'만 입력해 주세요.")

            # [11단계] 정답 판별 및 피드백 (정답/오답 모두 힌트 제공)
            if quiz.is_correct(choice):
                print(f"✅ 정답입니다!")
                score += 1
            else:
                print(f"❌ 틀렸습니다. 정답은 {quiz.answer}번입니다.")
            
            print(f"💡 추가 설명(힌트): {quiz.description}")
            print("-" * 40)

        # 최종 점수 계산 및 최고 기록 갱신 (7단계 연결)
        final_percentage = int((score / total) * 100)
        self.finalize_game(final_percentage)

    def finalize_game(self, final_percentage):
        """[7단계] 게임 종료 후 점수를 비교하여 최고 점수를 업데이트합니다."""
        print(f"\n🏁 종료! 최종 점수: {final_percentage}점")
        if final_percentage > self.high_score:
            print("🎊 축하합니다! 새로운 최고 기록입니다!")
            self.high_score = final_percentage
            self.save_data()
        else:
            print(f"현재 최고 기록: {self.high_score}점")

    def add_quiz(self):
        """[9단계] 사용자가 직접 새로운 문제를 추가하는 기능입니다."""
        print("\n➕ 새로운 퀴즈 추가")
        category = input("카테고리: ")
        question = input("질문: ")
        options = [input(f"보기 {i}: ") for i in range(1, 5)]
        
        while True:
            try:
                answer = int(input("정답 번호 (1~4): "))
                if 1 <= answer <= 4: break
            except ValueError: print("⚠️ 숫자만 입력하세요.")
        
        description = input("정답 해설(힌트): ")

        # 새 퀴즈 객체 생성 후 리스트에 추가
        new_quiz_data = {
            "id": len(self.quizzes) + 1,
            "category": category,
            "question": question,
            "options": options,
            "answer": answer,
            "description": description
        }
        self.quizzes.append(Quiz(**new_quiz_data))
        self.save_data()
        print("✅ 퀴즈가 성공적으로 추가되었습니다.")

    def view_quizzes(self):
        """[10단계] 현재 저장된 모든 퀴즈 목록을 표 형식으로 보여줍니다."""
        if not self.quizzes:
            print("\n❌ 저장된 퀴즈가 없습니다.")
            return

        print("\n" + "=" * 50)
        print(f"{'ID':<4} | {'카테고리':<10} | {'퀴즈 질문'}")
        print("-" * 50)
        for q in self.quizzes:
            print(f"{q.id:<4} | {q.category:<10} | {q.question}")
        print("=" * 50)