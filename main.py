import json
import os

class QuizGame:
    def __init__(self, data_file='state.json'):
        self.data_file = data_file
        self.load_data()

    def load_data(self):
        """JSON 파일에서 데이터를 읽어옵니다."""
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r', encoding='utf-8') as f:
                self.data = json.load(f)
        else:
            print("❌ 데이터 파일을 찾을 수 없습니다.")
            self.data = {"high_score": 0, "quizzes": []}

    def save_data(self):
        """최고 점수 등 변경된 데이터를 저장합니다."""
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)

    # --- [업데이트된 기능: 퀴즈 추가] ---
    def add_quiz(self):
        print("\n➕ 새로운 퀴즈를 추가합니다.")
        question = input("질문 내용: ")
        options = []
        for i in range(1, 5):
            opt = input(f"보기 {i}: ")
            options.append(opt)
        
        while True:
            try:
                answer = int(input("정답 번호 (1-4): "))
                if 1 <= answer <= 4: break
                else: print("⚠️ 1~4 사이의 숫자를 입력하세요.")
            except ValueError:
                print("⚠️ 숫자만 입력 가능합니다.")
        
        description = input("정답 해설: ")
        
        new_quiz = {
            "id": len(self.data['quizzes']) + 1,
            "question": question,
            "options": options,
            "answer": answer,
            "description": description
        }
        
        self.data['quizzes'].append(new_quiz)
        self.save_data()
        print("✅ 퀴즈가 성공적으로 추가되었습니다!")

    def run_quiz(self):
        """메인 기능을 실행합니다."""
        if not self.data['quizzes']:
            print("❌ 등록된 퀴즈가 없습니다. 퀴즈를 먼저 추가해주세요.")
            return

        print(f"\n📝 퀴즈를 시작합니다! (총 {len(self.data['quizzes'])}문제)")
        score = 0
        
        for idx, q in enumerate(self.data['quizzes'], 1):
            print("-" * 40)
            print(f"[문제 {idx}]")
            print(q['question'])
            for i, opt in enumerate(q['options'], 1):
                print(f"{i}. {opt}")
            
            try:
                user_ans = int(input("\n정답 입력: "))
                if user_ans == q['answer']:
                    print("✅ 정답입니다! " + f"({q['description']})")
                    score += 1
                else:
                    print(f"❌ 틀렸습니다. 정답은 {q['answer']}번입니다.")
            except ValueError:
                print("⚠️ 숫자만 입력해 주세요! 이번 문제는 건너뜜.")

        self.show_result(score)

    def show_result(self, score):
        total = len(self.data['quizzes'])
        final_score = int((score / total) * 100)
        print("=" * 40)
        print(f"🏆 결과: {total}문제 중 {score}문제 정답! ({final_score}점)")
        if final_score > self.data['high_score']:
            print("🎉 새로운 최고 점수입니다!")
            self.data['high_score'] = final_score
            self.save_data()
        else:
            print(f"현재 최고 기록: {self.data['high_score']}점")
        print("=" * 40)

def main():
    game = QuizGame()
    while True:
        print("\n🚀 Git과 함께하는 Python 첫 발자국")
        print("1. 퀴즈 풀기")
        print("2. 퀴즈 추가") # 메뉴 추가
        print("3. 프로그램 종료")
        choice = input("선택: ")
        if choice == '1':
            game.run_quiz()
        elif choice == '2':
            game.add_quiz() # 기능 호출
        elif choice == '3':
            print("👋 종료합니다.")
            break
        else:
            print("알 수 없는 메뉴입니다.")

if __name__ == "__main__":
    main()