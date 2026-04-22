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
        """데이터를 불러오고, 필수 항목이 없으면 기본값으로 복구합니다."""
        if not os.path.exists(self.data_file):
            self.set_default_data()
            return

        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
                # [여기가 핵심] 필수 키(history, quizzes)가 없으면 강제로 복구 모드 진입
                if 'history' not in data or 'quizzes' not in data:
                    print("⚠️ 필수 데이터(history)가 누락되어 복구 절차를 시작합니다.")
                    self.set_default_data()
                    return

                self.high_score = data.get('high_score', 0)
                self.history = data.get('history', [])
                self.quizzes = [Quiz(**q) for q in data.get('quizzes', [])]
            print(f"✅ 데이터 로드 완료 (최고 기록: {self.high_score}점)")

        except (json.JSONDecodeError, KeyError, Exception) as e:
            print(f"❌ 데이터 손상 감지: {e}")
            self.set_default_data()

    def save_data(self):
        """현재 상태를 JSON으로 저장할 때 history 필드를 반드시 포함합니다."""
        quiz_list = [vars(q) for q in self.quizzes]
        data_to_save = {
            "high_score": self.high_score,
            "history": getattr(self, 'history', []), # 이 부분이 'history'라는 글자를 만듭니다.
            "quizzes": quiz_list
        }
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(data_to_save, f, ensure_ascii=False, indent=2)

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
        self.finalize_game(final_percentage, score, total) # 인자 3개 전달

    def finalize_game(self, final_percentage, score, total):
        """게임 종료 후 점수를 기록하고 최고 점수를 업데이트합니다."""
        from datetime import datetime
        
        # [수정] 현재 기록 생성
        new_record = {
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "total_questions": total,
            "correct_answers": score,
            "score": final_percentage
        }
        
        # [수정] history 리스트가 없으면 생성하고 기록 추가
        if not hasattr(self, 'history'):
            self.history = []
        self.history.append(new_record)
        
        print(f"\n🏁 종료! 최종 점수: {final_percentage}점")
        
        # 최고 점수 갱신 로직
        if final_percentage > self.high_score:
            print("🎊 축하합니다! 새로운 최고 기록입니다!")
            self.high_score = final_percentage
        else:
            print(f"현재 최고 기록: {self.high_score}점")
            
        # [중요] 반드시 save_data를 호출하여 파일에 물리적으로 저장
        self.save_data()

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

    def delete_quiz(self):
        """[보너스] 선택한 번호의 퀴즈를 삭제하고 파일에 저장합니다."""
        self.view_quizzes()
        if not self.quizzes: return

        while True:
            try:
                target_id = int(input("\n🗑️ 삭제할 퀴즈의 ID를 입력하세요 (취소: 0): "))
                if target_id == 0: break
                
                # ID가 일치하는 퀴즈 찾아서 삭제
                original_count = len(self.quizzes)
                self.quizzes = [q for q in self.quizzes if q.id != target_id]
                
                if len(self.quizzes) < original_count:
                    self.save_data()
                    print(f"✅ {target_id}번 퀴즈가 삭제되었습니다.")
                    break
                else:
                    print("⚠️ 해당 ID의 퀴즈를 찾을 수 없습니다.")
            except ValueError:
                print("⚠️ 숫자만 입력해 주세요.")

    def view_history(self):
        """[보너스] 전체 게임 기록(히스토리)을 표 형식으로 출력합니다."""
        if not hasattr(self, 'history') or not self.history:
            print("\n📜 아직 게임 기록이 없습니다. 첫 게임을 시작해 보세요!")
            return

        print("\n" + "=" * 60)
        print(f"{'일시':<20} | {'문항 수':<7} | {'맞춘 개수':<7} | {'점수'}")
        print("-" * 60)
        
        # 최근 기록이 위로 오도록 역순으로 출력
        for h in reversed(self.history):
            date = h.get('date', 'N/A')
            total = h.get('total_questions', 0)
            correct = h.get('correct_answers', 0)
            score = h.get('score', 0)
            print(f"{date:<20} | {total:<8} | {correct:<9} | {score}점")
        print("=" * 60)

    def set_default_data(self):
        """
        [요구사항] 데이터 파일이 없거나 손상된 경우, 
        기본 퀴즈 5개와 초기 점수/히스토리를 설정하고 저장합니다.
        """
        self.high_score = 0
        self.history = []  # 보너스 미션용 히스토리 초기화
        
        # 기본 퀴즈 데이터 (선생님이 정하신 영화 주제)
        default_quizzes = [
            {
                "id": 1, "category": "영화",
                "question": "전 세계 흥행 1위 영화 <아바타> 1편의 나비족 손가락 개수는?",
                "options": ["3개", "4개", "5개", "6개"], "answer": 2,
                "description": "인간은 5개이지만, 나비족은 4개입니다."
            },
            {
                "id": 2, "category": "시리즈",
                "question": "넷플릭스 <오징어 게임> 주인공 성기훈의 마지막 참가 번호는?",
                "options": ["001번", "199번", "218번", "456번"], "answer": 4,
                "description": "456억 원의 주인공, 마지막 참가자였죠!"
            },
            {
                "id": 3, "category": "영화",
                "question": "영화 <어벤져스: 엔드게임> 명대사 '나는 너를 ____만큼 사랑해'의 숫자는?",
                "options": ["100", "1000", "3000", "5000"], "answer": 3,
                "description": "아이언맨의 희생과 사랑을 상징하는 숫자입니다."
            },
            {
                "id": 4, "category": "영화",
                "question": "제임스 본드(007 시리즈)가 부여받은 살인면허 번호는?",
                "options": ["001", "003", "007", "009"], "answer": 3,
                "description": "이름보다 유명한 제임스 본드의 코드네임입니다."
            },
            {
                "id": 5, "category": "영화",
                "question": "영화 <해리포터>에서 호그와트행 열차를 타기 위한 승강장 번호는?",
                "options": ["9와 1/4", "9와 2/4", "9와 3/4", "10번"], "answer": 3,
                "description": "9번과 10번 승강장 사이 벽으로 뛰어드세요!"
            }
        ]
        
        # 딕셔너리 데이터를 Quiz 객체 리스트로 변환 (self.quizzes에 할당)
        self.quizzes = [Quiz(**q) for q in default_quizzes]
        
        # 생성된 기본 데이터를 파일로 즉시 저장하여 파일 구조를 '정상화'함
        self.save_data()
        print("💡 기본 퀴즈 데이터(5문항) 및 표준 스키마가 생성되었습니다.")