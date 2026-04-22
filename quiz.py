class Quiz:
    """
    [데이터 모델 클래스]
    하나의 퀴즈 문제에 대한 정보(질문, 보기, 정답, 해설)를 담는 객체입니다.
    """
    def __init__(self, **data):
        # 딕셔너리 데이터를 받아와서 각 속성에 할당합니다.
        self.id = data.get('id')
        self.category = data.get('category', '미분류')
        self.question = data.get('question')
        self.options = data.get('options', [])
        self.answer = data.get('answer')
        self.description = data.get('description', '')

    def is_correct(self, user_answer):
        """사용자가 입력한 번호와 실제 정답 번호를 비교하여 결과를 반환합니다."""
        return int(user_answer) == self.answer
    
    def get_summary(self):
        """삭제 목록이나 전체 목록을 보여줄 때 사용할 요약 텍스트입니다."""
        return f"[{self.category}] {self.question}"

    def to_dict(self):
        """객체 상태를 다시 JSON으로 저장하기 위해 딕셔너리로 변환합니다."""
        return {
            "id": self.id,
            "category": self.category,
            "question": self.question,
            "options": self.options,
            "answer": self.answer,
            "description": self.description
        }
