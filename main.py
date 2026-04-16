from quizgame import QuizGame # 로직 클래스 불러오기

def main():
    """프로그램의 전체 실행 흐름을 제어하는 메인 함수입니다."""
    # 게임 시스템 가동
    game = QuizGame()
    
    while True:
        print("\n" + "="*40)
        print("🚀 Git과 함께하는 Python 영화 퀴즈 게임")
        print("="*40)
        print("1. 퀴즈 풀기 시작")
        print("2. 새로운 퀴즈 추가")
        print("3. 현재 퀴즈 목록 보기")
        print("4. 프로그램 종료")
        print("="*40)
        
        choice = input("👉 원하시는 메뉴 번호를 입력하세요: ")
        
        if choice == '1':
            game.run_quiz()
        elif choice == '2':
            game.add_quiz()
        elif choice == '3':
            game.view_quizzes()
        elif choice == '4':
            print("\n👋 프로그램을 종료합니다. 수고하셨습니다!")
            break
        else:
            print("\n⚠️ 잘못된 입력입니다. 1~4번 사이의 숫자를 입력해 주세요.")

if __name__ == "__main__":
    main()