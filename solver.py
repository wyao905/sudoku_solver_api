class Solution:
    def __init__(self, puzzle):
        self.board = puzzle
        self.empty_spaces = []
        self.rows = []
        self.cols = [[], [], [], [], [], [], [], [], []]
        self.sqrs = [[[], [], []], [[], [], []], [[], [], []]]
        self.complete = False
        self.__parse_board(puzzle)

        
    def solve(self):
        board = self.board
   
        empty_spaces = [*self.empty_spaces]
        rows = [*self.rows]
        cols = [*self.cols]
        sqrs = [*self.sqrs]
        result = self.__recurse(empty_spaces, rows, cols, sqrs)
        if result == 'no_solution':
            return False
        else:
            return True
    
    
    def verify(self):
        for i in range(9):
            row_result = self.__check_section(self.rows[i])
            col_result = self.__check_section(self.cols[i])

            for j in range(1, 10):
                if row_result[j] > 1 or col_result[j] > 1:
                    return False
        
        for k in range(3):
            for l in range(3):
                sqr_result = self.__check_section(self.sqrs[k][l])

                for m in range(1, 10):
                    if sqr_result[m] > 1:
                        return False
        
        return True


    def __recurse(self, empty_spaces, rows, cols, sqrs, first = True):
        while len(empty_spaces) != 0:
            pos = empty_spaces[0]
            potential_solutions = self.__generate_potential_solutions(pos, rows, cols, sqrs)
            if len(potential_solutions) == 0 and not first:
                return None
            else:
                while len(potential_solutions) != 0 and not self.complete:
                    value = potential_solutions.pop(0)
                    updated_empty_spaces = empty_spaces[1:]
                    updated_rows = [*rows[:pos[0]], [*rows[pos[0]][:pos[1]], value, *rows[pos[0]][pos[1] + 1:]], *rows[pos[0] + 1:]]
                    updated_cols = [*cols[:pos[1]], [*cols[pos[1]][:pos[0]], value, *cols[pos[1]][pos[0] + 1:]], *cols[pos[1] + 1:]]
                    updated_sqrs = [*sqrs[:int(pos[0] / 3)], [*sqrs[int(pos[0] / 3)][:int(pos[1] / 3)], [*sqrs[int(pos[0] / 3)][int(pos[1] / 3)][:(pos[0] * 3) + pos[1]], value, *sqrs[int(pos[0] / 3)][int(pos[1] / 3)][(pos[0] * 3) + pos[1] + 1:]], *sqrs[int(pos[0] / 3)][int(pos[1] / 3) + 1:]], *sqrs[int(pos[0] / 3) + 1:]]
                    self.__recurse(updated_empty_spaces, updated_rows, updated_cols, updated_sqrs, False)

                if self.complete:
                    self.board[empty_spaces[0][0]][empty_spaces[0][1]] = value
    
                if not self.complete and first:
                    return 'no_solution'
                else:
                    return None

        self.complete = True
        
    
    def __parse_board(self, puzzle):
        for row_id, row in enumerate(puzzle):
            for col_id, space in enumerate(row):
                if space == 0:
                    self.empty_spaces.append([row_id, col_id])
                
                self.sqrs[int(row_id / 3)][int(col_id / 3)].append(space)
            
                self.cols[col_id].append(space)
                
            self.rows.append(row)


    def __generate_potential_solutions(self, pos, rows, cols, sqrs):
        potential_solutions = []
        row = rows[pos[0]]
        col = cols[pos[1]]
        sqr = sqrs[int(pos[0] / 3)][int(pos[1] / 3)]

        num_in_row = self.__check_section(row)
        num_in_col = self.__check_section(col)
        num_in_sqr = self.__check_section(sqr)

        for i in range(1, 10):
            if num_in_row[i] == 0 and num_in_col[i] == 0 and num_in_sqr[i] == 0:
                potential_solutions.append(i)
        
        return potential_solutions

    
    def __check_section(self, section):
        tracker = {1: 0,
                   2: 0,
                   3: 0,
                   4: 0,
                   5: 0,
                   6: 0,
                   7: 0,
                   8: 0,
                   9: 0}

        for space in section:
            if space == 0:
                pass
            else:
                tracker[space] += 1
        else:
            return tracker