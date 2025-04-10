import random
import os

# 보드 크기 (4x4)
SIZE = 4

# 보드 초기화 함수
def init_board():
    # 0으로 채워진 4x4 보드 생성
    board = [[0] * SIZE for _ in range(SIZE)]
    # 시작할 때 숫자 2개 추가
    add_new_tile(board)
    add_new_tile(board)
    return board

# 보드를 터미널에 출력
def print_board(board):
    # 콘솔 화면 클리어 (Windows와 Unix 계열 대응)
    os.system('cls' if os.name == 'nt' else 'clear')
    for row in board:
        print('+----' * SIZE + '+')  # 행 구분선
        # 각 칸에 숫자를 가운데 정렬하여 출력
        print(''.join(f'|{num:^4}' if num != 0 else '|    ' for num in row) + '|')
    print('+----' * SIZE + '+')  # 마지막 줄 구분선

# 보드의 빈 칸 중 하나에 2 또는 4 추가
def add_new_tile(board):
    # 0인 칸(빈 칸) 위치들을 리스트로 저장
    empty = [(i, j) for i in range(SIZE) for j in range(SIZE) if board[i][j] == 0]
    if not empty:
        return
    i, j = random.choice(empty)  # 랜덤한 빈 칸 선택
    board[i][j] = random.choice([2, 4])  # 새 숫자 추가

# 한 줄(리스트)을 왼쪽으로 밀면서 숫자를 합치는 함수
def merge_left(row):
    # 0을 제거한 숫자만 모음
    new_row = [num for num in row if num != 0]
    merged = []
    skip = False
    for i in range(len(new_row)):
        if skip:
            skip = False
            continue
        # 연속된 숫자가 같으면 합쳐서 추가
        if i + 1 < len(new_row) and new_row[i] == new_row[i+1]:
            merged.append(new_row[i] * 2)
            skip = True  # 다음 숫자는 건너뜀
        else:
            merged.append(new_row[i])
    # 나머지는 0으로 채워서 길이를 4로 맞춤
    return merged + [0] * (SIZE - len(merged))

# 보드를 지정된 방향으로 이동시키는 함수
def move(board, direction):
    moved = False
    for i in range(SIZE):
        if direction in ('a', 'd'):  # 좌, 우 방향 처리
            row = board[i][:]
            if direction == 'd':  # 오른쪽이면 반전
                row.reverse()
            new_row = merge_left(row)  # 병합
            if direction == 'd':
                new_row.reverse()  # 다시 원래 방향으로 복원
            if board[i] != new_row:
                board[i] = new_row
                moved = True
        else:  # 상, 하 방향 처리
            col = [board[j][i] for j in range(SIZE)]  # 열 추출
            if direction == 's':  # 아래면 반전
                col.reverse()
            new_col = merge_left(col)
            if direction == 's':
                new_col.reverse()
            # 변경된 열을 보드에 다시 넣음
            for j in range(SIZE):
                if board[j][i] != new_col[j]:
                    board[j][i] = new_col[j]
                    moved = True
    return moved

# 이동 가능한 상태인지 확인하는 함수 (게임 종료 판단용)
def can_move(board):
    for i in range(SIZE):
        for j in range(SIZE):
            if board[i][j] == 0:
                return True  # 빈 칸이 있으면 이동 가능
            # 인접한 숫자가 같으면 병합 가능
            for dx, dy in ((0, 1), (1, 0)):
                ni, nj = i + dx, j + dy
                if ni < SIZE and nj < SIZE and board[i][j] == board[ni][nj]:
                    return True
    return False  # 이동 불가 = 게임 오버

# 게임 메인 루프
def play():
    board = init_board()
    while True:
        print_board(board)
        move_input = input("Move (w/a/s/d): ").lower()
        if move_input not in ('w', 'a', 's', 'd'):
            print("Invalid input. Use w/a/s/d.")
            continue
        # 방향 입력 → 이동 → 새 숫자 추가
        if move(board, move_input):
            add_new_tile(board)
        else:
            print("No tiles moved. Try a different direction.")
        # 이동 불가하면 게임 종료
        if not can_move(board):
            print_board(board)
            print("Game Over!")
            break

# 프로그램 실행 시작점
if __name__ == '__main__':
    play()
