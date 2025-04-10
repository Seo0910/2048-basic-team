import random

# 보드 크기 설정 (4x4)
SIZE = 4

# 1. 보드 초기화 함수
def init_board():
    # 0으로 채운 4x4 보드를 생성
    board = [[0] * SIZE for _ in range(SIZE)]
    # 시작할 때 숫자 2개를 임의 위치에 배치하지 않고 고정 위치에 배치 (단순화)
    board[0][0] = 2
    board[1][1] = 2
    return board

# 2. 보드를 콘솔에 출력하는 함수
def print_board(board):
    for row in board:
        print(row)  # 간단히 리스트 형태로 출력

# 3. 왼쪽으로 숫자를 밀어주는 함수 (합치기 기능은 없음)
def move_left(board):
    for i in range(SIZE):
        # 0이 아닌 숫자만 남기고 앞으로 모으기
        new_row = [num for num in board[i] if num != 0]
        # 남은 칸은 0으로 채우기
        new_row += [0] * (SIZE - len(new_row))
        # 변경된 행을 다시 보드에 반영
        board[i] = new_row

# 4. 메인 게임 루프
def play():
    board = init_board()
    print("초기 보드:")
    print_board(board)

    while True:
        cmd = input("a(← 입력): ")  # 방향 입력 (지금은 좌측 이동만 지원)
        if cmd != 'a':
            print("좌측 이동(a)만 지원됩니다.")  # 방향 제한
            continue
        move_left(board)  # 좌측으로 숫자 이동
        print("이동 후 보드:")
        print_board(board)  # 변경된 보드 출력

# 5. 프로그램 실행 진입점
if __name__ == '__main__':
    play()
