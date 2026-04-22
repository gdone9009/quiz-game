import sys
from quizgame import QuizGame # 로직 클래스 불러오기

def main():
    """프로그램의 전체 실행 흐름을 제어하는 메인 함수입니다."""
    # 게임 시스템 가동
    game = QuizGame()
    
    try:
        while True:
            print("\n" + "="*40)
            print("🚀 Git과 함께하는 Python 영화 퀴즈 게임")
            print("="*40)
            print(" 1. 퀴즈 풀기 시작")
            print(" 2. 새로운 퀴즈 추가")
            print(" 3. 현재 퀴즈 목록 보기")
            print(" 4. 퀴즈 삭제하기 (Bonus)")
            print(" 5. 전체 점수 히스토리 확인 (Bonus)")
            print(" 6. 프로그램 종료")
            print("="*40)
            
            # [요구사항] 앞뒤 공백 제거 처리
            choice = input("👉 원하시는 메뉴 번호를 입력하세요: ").strip()
            
            if choice == '1':
                game.run_quiz()
            elif choice == '2':
                game.add_quiz()
            elif choice == '3':
                game.view_quizzes()
            elif choice == '4':
                game.delete_quiz()  # 보너스: 삭제 기능
            elif choice == '5':
                game.view_history() # 보너스: 히스토리 기능
            elif choice == '6':
                print("\n👋 프로그램을 안전하게 종료합니다. 수고하셨습니다!")
                game.save_data()    # 종료 전 최종 저장
                break
            elif not choice:
                print("\n⚠️ 입력값이 없습니다. 메뉴 번호를 입력해 주세요.")
            else:
                print("\n⚠️ 잘못된 입력입니다. 1~6번 사이의 숫자를 입력해 주세요.")

    except (KeyboardInterrupt, EOFError):
        # [요구사항] Ctrl+C 또는 강제 종료 발생 시 처리
        print("\n\n⚠️ 비정상 종료가 감지되었습니다.")
        print("💾 데이터를 안전하게 저장하고 프로그램을 종료합니다.")
        game.save_data()
        sys.exit(0)

if __name__ == "__main__":
    main()