# COMP9021 19T3 - Rachid Hamadi
# Assignment 2 *** Due Sunday Week 10


# IMPORT ANY REQUIRED MODULE


class MazeError(Exception):
    def __init__(self, message):
        self.message = message


class Maze:
    def __init__(self, filename):
        pre_len = 0
        file_object = open(filename)
        self.__file = filename[:-3] + 'tex'
        self.__matrix = []
        self.__wallSet = []
        self.__spaceSet = []
        self.__pillar = []
        self.__xPoint = []
        self.__bannedPoint = []
        self.__path_point = []
        self.__path_route = []
        for line in file_object.readlines():
            len_temp = 0
            line_temp = []
            line = line.strip()
            if line is '':
                continue
            for character in line:
                if character is not ' ':
                    if character.isdecimal() is False or int(character) > 3:
                        raise MazeError('Incorrect input.')
                    line_temp.append(int(character))
                    len_temp += 1
            if pre_len == 0:
                pre_len = len_temp
            else:
                if len_temp != pre_len:
                    raise MazeError('Incorrect input.')
            self.__matrix.append(line_temp)
            file_object.close()
        if len(self.__matrix) < 2 or len(self.__matrix[0]) < 2 or len(self.__matrix) > 41 or len(self.__matrix[0]) > 31:
            raise MazeError('Incorrect input.')
        line = 0
        edge_num = [0, 0]
        while line < len(self.__matrix):
            if self.__matrix[line][-1] == 1 or self.__matrix[line][-1] == 3:
                raise MazeError('Input does not represent a maze.')
            line += 1
        line = 0
        while line < len(self.__matrix[-1]):
            if self.__matrix[-1][line] == 2 or self.__matrix[-1][line] == 3:
                raise MazeError('Input does not represent a maze.')
            line += 1
        self.__analyze()

    def __colour_changes(self, k, matrix):
        x = y = 1
        sign = 0
        parts = []
        while x < len(matrix):
            while y < len(matrix[0]):
                if matrix[x][y] == 1:
                    matrix[x][y] = k
                    parts.append([x, y])
                    sign = 1
                    break
                y += 1
            if sign == 1:
                break
            x += 1
            y = 1
        else:
            return False
        sign = 0
        while 1:
            x = parts[sign][0]
            y = parts[sign][1]
            if matrix[x - 1][y] == 1:
                matrix[x - 1][y] = k
                if [x - 1, y] not in parts:
                    parts.append([x - 1, y])
            if matrix[x + 1][y] == 1:
                matrix[x + 1][y] = k
                if [x + 1, y] not in parts:
                    parts.append([x + 1, y])
            if matrix[x][y - 1] == 1:
                matrix[x][y - 1] = k
                if [x, y - 1] not in parts:
                    parts.append([x, y - 1])
            if matrix[x][y + 1] == 1:
                matrix[x][y + 1] = k
                if [x, y + 1] not in parts:
                    parts.append([x, y + 1])
            sign += 1
            if sign >= len(parts):
                break

    def __colour_shapes(self, matrix):
        k = 2
        while 1:
            if self.__colour_changes(k, matrix) is False:
                return k - 2
            k += 1

    def __wall_set(self):
        self.__wallSet.append([0] * (2 + 2 * len(self.__matrix[0])))
        self.__wallSet.append([0] * (2 + 2 * len(self.__matrix[0])))
        for line in self.__matrix:
            self.__wallSet.append([0, 0])
            self.__wallSet.append([0, 0])
            character_sign = 1
            for character in line:
                if character == 0:
                    self.__wallSet[-2] += [0, 0]
                    self.__wallSet[-1] += [0, 0]
                elif character == 1:
                    self.__wallSet[-3][character_sign] = 1
                    self.__wallSet[-3][character_sign + 1] = 1
                    self.__wallSet[-3][character_sign + 2] = 1
                    self.__wallSet[-2] += [0, 0]
                    self.__wallSet[-1] += [0, 0]
                elif character == 2:
                    self.__wallSet[-3][character_sign] = 1
                    self.__wallSet[-2][-1] = 1
                    self.__wallSet[-2] += [0, 0]
                    self.__wallSet[-1][-1] = 1
                    self.__wallSet[-1] += [0, 0]
                elif character == 3:
                    self.__wallSet[-3][character_sign] = 1
                    self.__wallSet[-3][character_sign + 1] = 1
                    self.__wallSet[-3][character_sign + 2] = 1
                    self.__wallSet[-2][-1] = 1
                    self.__wallSet[-2] += [0, 0]
                    self.__wallSet[-1][-1] = 1
                    self.__wallSet[-1] += [0, 0]
                character_sign += 2
        del (self.__wallSet[-1])
        line = 0
        while line < len(self.__wallSet):
            del (self.__wallSet[line][-1])
            line += 1
        return self.__colour_shapes(self.__wallSet)

    def __gates_count(self):
        count = 0
        for character in self.__matrix[0][:-1]:
            if character != 1 and character != 3:
                count += 1
        for character in self.__matrix[-1][:-1]:
            if character != 1:
                count += 1
        for line in self.__matrix[:-1]:
            if line[0] != 2 and line[0] != 3:
                count += 1
            if line[-1] != 2:
                count += 1
        return count

    def __space_convert(self):
        line = 0
        while line < len(self.__wallSet):
            self.__spaceSet.append([])
            if line == 0 or line == len(self.__wallSet) - 1:
                self.__spaceSet[line] = [None] * len(self.__wallSet[line])
            else:
                character = 0
                while character < len(self.__wallSet[0]):
                    if character == 0 or character == len(self.__wallSet[line]) - 1:
                        character_temp = None
                    elif self.__wallSet[line][character] != 0:
                        character_temp = 0
                    else:
                        character_temp = 1
                    self.__spaceSet[line].append(character_temp)
                    character += 1
            line += 1

    def __space_analyze_method(self, space, matrix, sign=0):
        space_analyze = []
        for temp in range(0, space):
            space_analyze.append([0, [], []])  # 出入口,[该块中有多个去向的点坐标]，[该块中所有点坐标]
        line = 0
        while line < len(matrix):
            character = 0
            while character < len(matrix[line]):
                if matrix[line][character] is None:
                    matrix[line][character] = 1
                character += 1
            line += 1
        line = 1
        while line < len(matrix) - 1:
            character = 1
            while character < len(matrix[line]) - 1:
                wall_count = 0
                near_count = 0
                out_count = 0
                if matrix[line][character] > 1:
                    if matrix[line - 1][character] == 1:
                        if ((line / 2).is_integer() and (character == 1 or character == len(matrix[line]) - 2)) \
                                or ((character / 2).is_integer() and (line == 1 or line == len(matrix) - 2)):
                            space_analyze[matrix[line][character] - 2][0] += 1
                        out_count += 1
                    elif matrix[line - 1][character] == matrix[line][character]:
                        near_count += 1
                    elif matrix[line - 1][character] == 0 and (line / 2).is_integer() and (character / 2).is_integer():
                        wall_count += 1
                    if matrix[line + 1][character] == 1:
                        if ((line / 2).is_integer() and (character == 1 or character == len(matrix[line]) - 2)) \
                                or ((character / 2).is_integer() and (line == 1 or line == len(matrix) - 2)):
                            space_analyze[matrix[line][character] - 2][0] += 1
                        out_count += 1
                    elif matrix[line + 1][character] == matrix[line][character]:
                        near_count += 1
                    elif matrix[line + 1][character] == 0 and (line / 2).is_integer() and (character / 2).is_integer():
                        wall_count += 1
                    if matrix[line][character - 1] == 1:
                        if ((line / 2).is_integer() and (character == 1 or character == len(matrix[line]) - 2)) \
                                or ((character / 2).is_integer() and (line == 1 or line == len(matrix) - 2)):
                            space_analyze[matrix[line][character] - 2][0] += 1
                        out_count += 1
                    elif matrix[line][character - 1] == matrix[line][character]:
                        near_count += 1
                    elif matrix[line][character - 1] == 0 and (line / 2).is_integer() and (character / 2).is_integer():
                        wall_count += 1
                    if matrix[line][character + 1] == 1:  # 前面四个是判断出口个数
                        if ((line / 2).is_integer() and (character == 1 or character == len(matrix[line]) - 2)) \
                                or ((character / 2).is_integer() and (line == 1 or line == len(matrix) - 2)):
                            space_analyze[matrix[line][character] - 2][0] += 1
                        out_count += 1
                    elif matrix[line][character + 1] == matrix[line][character]:
                        near_count += 1
                    elif matrix[line][character + 1] == 0 and (line / 2).is_integer() and (character / 2).is_integer():
                        wall_count += 1
                    if matrix[line - 1][character - 1] == matrix[line][character]:
                        near_count += 1
                    if matrix[line + 1][character - 1] == matrix[line][character]:
                        near_count += 1
                    if matrix[line - 1][character + 1] == matrix[line][character]:
                        near_count += 1
                    if matrix[line + 1][character + 1] == matrix[line][character]:
                        near_count += 1
                    if (line == 1 or line == len(matrix) - 2) or (character == 1 or character == len(matrix[line]) - 2):
                        if (near_count == 3 and out_count == 2) or (near_count == 5 and out_count == 1):
                            if ((line - 1) / 2).is_integer() and ((character - 1) / 2).is_integer():
                                if [(line - 1) / 2, (character - 1) / 2] not in self.__pillar:
                                    self.__pillar.append([int((line - 1) / 2), int((character - 1) / 2)])
                    if near_count == 8 and ((line - 1) / 2).is_integer() and ((character - 1) / 2).is_integer():
                        if [(line - 1) / 2, (character - 1) / 2] not in self.__pillar:
                            self.__pillar.append([int((line - 1) / 2), int((character - 1) / 2)])
                    if wall_count == 3:
                        self.__xPoint.append([line, character])
                    if (line / 2).is_integer() and (character / 2).is_integer():
                        if wall_count < 2:
                            space_analyze[matrix[line][character] - 2][1].append(
                                [int(line / 2) - 1, int(character / 2) - 1])
                        space_analyze[matrix[line][character] - 2][2].append([line, character])
                character += 1
            line += 1
        return space_analyze

    def __space_set(self):
        self.__space_convert()
        space = self.__colour_shapes(self.__spaceSet)
        space_analyze = self.__space_analyze_method(space, self.__spaceSet, 1)
        for line in space_analyze:
            if line[0] == 0:
                self.__bannedPoint += line[2]
        self.__bannedPoint = list(tuple(self.__bannedPoint))
        x_point_temp = self.__xPoint[0:]
        for point in x_point_temp:
            temp_out = 1
            temp_line = point[0]
            temp_character = point[1]
            while temp_out == 1:
                temp_out = 0
                pre_temp = [temp_line, temp_character]
                if pre_temp[0] + 1 < len(self.__spaceSet) and self.__spaceSet[pre_temp[0] + 1][pre_temp[1]] != 0:
                    if [pre_temp[0] + 2, pre_temp[1]] not in self.__xPoint:
                        if pre_temp not in self.__xPoint:
                            self.__xPoint.append(pre_temp)
                        temp_line = temp_line + 2
                        temp_character = temp_character
                        temp_out += 1
                if pre_temp[1] + 1 < len(self.__spaceSet[0]) and self.__spaceSet[pre_temp[0]][pre_temp[1] + 1] != 0:
                    if [pre_temp[0], pre_temp[1] + 2] not in self.__xPoint:
                        if pre_temp not in self.__xPoint:
                            self.__xPoint.append(pre_temp)
                        temp_line = temp_line
                        temp_character = temp_character + 2
                        temp_out += 1
                if pre_temp[0] - 1 > 0 and self.__spaceSet[pre_temp[0] - 1][pre_temp[1]] != 0:
                    if [pre_temp[0] - 2, pre_temp[1]] not in self.__xPoint:
                        if pre_temp not in self.__xPoint:
                            self.__xPoint.append(pre_temp)
                        temp_line = temp_line - 2
                        temp_character = temp_character
                        temp_out += 1
                if pre_temp[1] - 1 > 0 and self.__spaceSet[pre_temp[0]][pre_temp[1] - 1] != 0:
                    if [pre_temp[0], pre_temp[1] - 2] not in self.__xPoint:
                        if pre_temp not in self.__xPoint:
                            self.__xPoint.append(pre_temp)
                        temp_line = temp_line
                        temp_character = temp_character - 2
                        temp_out += 1
                if temp_out > 1:
                    self.__xPoint = self.__xPoint[:-1]
                    break
        character = 0
        while character < len(self.__xPoint):
            if self.__xPoint[character] in self.__bannedPoint:
                del (self.__xPoint[character])
            else:
                character += 1
        line = 0
        space_temp = []
        while line < len(self.__spaceSet):
            character = 0
            space_temp.append([])
            while character < len(self.__spaceSet[line]):
                if [line, character] in self.__xPoint:
                    space_temp[line].append(1)
                    if len(self.__spaceSet) - 1 > line > 1 and [line - 2, character] in self.__xPoint and \
                            self.__spaceSet[line - 1][character] != 0:
                        space_temp[line - 1][character] = 1
                    if len(self.__spaceSet[0]) - 1 > character > 1 and [line, character - 2] in self.__xPoint and \
                            self.__spaceSet[line][character - 1] != 0:
                        space_temp[line][character - 1] = 1
                else:
                    space_temp[line].append(0)
                character += 1
            line += 1
        inner_parts = self.__colour_shapes(space_temp)

        accessible_area = 0
        line = 0
        one_way_check = []
        while line < len(space_analyze):
            if space_analyze[line][0] == 2:
                character = 0
                while character < len(space_analyze[line][2]):
                    if space_analyze[line][2][character] in self.__xPoint:
                        del (space_analyze[line][2][character])
                    else:
                        character += 1
                one_way_check.append(space_analyze[line][2])
            if space_analyze[line][0] > 0:
                accessible_area += 1
            line += 1
        line = 0
        while line < len(one_way_check):
            not_route_sign = 0
            if len(one_way_check[line]) < 3:
                line += 1
                continue
            character = 0
            while character < len(one_way_check[line]):
                available_count = 0
                x_temp = int(one_way_check[line][character][0] / 2) - 1
                y_temp = int(one_way_check[line][character][1] / 2) - 1
                if [x_temp, y_temp] in self.__pillar:
                    not_route_sign = 1
                    break
                if [x_temp + 1, y_temp] in self.__pillar:
                    not_route_sign = 1
                    break
                if [x_temp, y_temp + 1] in self.__pillar:
                    not_route_sign = 1
                    break
                if [x_temp + 1, y_temp + 1] in self.__pillar:
                    not_route_sign = 1
                    break
                x_temp = (x_temp + 1) * 2
                y_temp = (y_temp + 1) * 2
                if self.__spaceSet[x_temp - 1][y_temp] != 0 and [x_temp - 2, y_temp] not in self.__xPoint:
                    available_count += 1
                if self.__spaceSet[x_temp + 1][y_temp] != 0 and [x_temp + 2, y_temp] not in self.__xPoint:
                    available_count += 1
                if self.__spaceSet[x_temp][y_temp - 1] != 0 and [x_temp, y_temp - 2] not in self.__xPoint:
                    available_count += 1
                if self.__spaceSet[x_temp][y_temp + 1] != 0 and [x_temp, y_temp + 2] not in self.__xPoint:
                    available_count += 1
                if available_count != 2:
                    not_route_sign = 1
                    break
                character += 1
            if not_route_sign == 1:
                del (one_way_check[line])
                if len(one_way_check) == 0:
                    break
            else:
                line += 1
        one_way_route = len(one_way_check)
        line = 0
        while line < len(one_way_check):
            one_way_check[line].sort()
            self.__path_point.append(one_way_check[line])
            line += 1
        character = 0
        while character < len(self.__xPoint):
            self.__xPoint[character] = [int(self.__xPoint[character][0] / 2 - 1),
                                        int(self.__xPoint[character][1] / 2 - 1)]
            character += 1
        character = 0
        while character < len(self.__bannedPoint):
            self.__bannedPoint[character] = [int(self.__bannedPoint[character][0] / 2 - 1),
                                             int(self.__bannedPoint[character][1] / 2 - 1)]
            character += 1
        return [len(self.__bannedPoint), accessible_area, inner_parts, one_way_route]

    @staticmethod
    def __space_vert_back(matrix):
        line = 0
        while line < len(matrix):
            character = 0
            while character < len(matrix[line]):
                if matrix[line][character] > 1:
                    matrix[line][character] = 1
                if line == 0 or line == len(matrix) - 1:
                    matrix[line][character] = None
                if character == 0 or character == len(matrix[line]) - 1:
                    matrix[line][character] = None
                character += 1
            line += 1

        return matrix

    def __analyze(self):
        result_1 = self.__gates_count()
        result_2 = self.__wall_set()
        [result_3, result_4, result_5, result_6] = self.__space_set()
        self.__results = [result_1, result_2, result_3, result_4, result_5, result_6]

    def analyse(self):
        [result_1, result_2, result_3, result_4, result_5, result_6] = self.__results
        if result_1 == 0:
            print('The maze has no gate.')
        elif result_1 == 1:
            print('The maze has a single gate.')
        else:
            print('The maze has ' + str(result_1) + ' gates.')
        if result_2 == 0:
            print('The maze has no wall.')
        elif result_2 == 1:
            print('The maze has walls that are all connected.')
        else:
            print('The maze has ' + str(result_2) + ' sets of walls that are all connected.')
        if result_3 == 0:
            print('The maze has no inaccessible inner point.')
        elif result_3 == 1:
            print('The maze has a unique inaccessible inner point.')
        else:
            print('The maze has ' + str(result_3) + ' inaccessible inner points.')
        if result_4 == 0:
            print('The maze has no accessible area.')
        elif result_4 == 1:
            print('The maze has a unique accessible area.')
        else:
            print('The maze has ' + str(result_4) + ' accessible areas.')
        if result_5 == 0:
            print('The maze has no accessible cul-de-sac.')
        elif result_5 == 1:
            print('The maze has accessible cul-de-sacs that are all connected.')
        else:
            print('The maze has ' + str(result_5) + ' sets of accessible cul-de-sacs that are all connected.')
        if result_6 == 0:
            print('The maze has no entry-exit path with no intersection not to cul-de-sacs.')
        elif result_6 == 1:
            print('The maze has a unique entry-exit path with no intersection not to cul-de-sacs.')
        else:
            print('The maze has ' + str(result_6) + ' entry-exit paths with no intersections not to cul-de-sacs.')

    def __walls_draw(self):
        draw = '\n    \\draw '
        walls_draw = '\n% Walls'
        line = 0
        while line < len(self.__matrix):
            character = 0
            sign = 0
            while character < len(self.__matrix[line]):
                if self.__matrix[line][character] == 1 or self.__matrix[line][character] == 3:
                    if sign == 0:
                        start = (character, line)
                        sign = 1
                else:
                    if sign == 1:
                        end = (character, line)
                        walls_draw += draw + ''.join(str(start).split()) + ' -- ' + ''.join(str(end).split()) + ';'
                        sign = 0
                character += 1
            line += 1
        character = 0
        while character < len(self.__matrix[0]):
            line = 0
            sign = 0
            while line < len(self.__matrix):
                if self.__matrix[line][character] == 2 or self.__matrix[line][character] == 3:
                    if sign == 0:
                        start = (character, line)
                        sign = 1
                else:
                    if sign == 1:
                        end = (character, line)
                        walls_draw += draw + ''.join(str(start).split()) + ' -- ' + ''.join(str(end).split()) + ';'
                        sign = 0
                line += 1
            character += 1
        return walls_draw

    def __pillars_draw(self):
        draw = '\n    \\fill[green] '
        pillars_draw = '\n% Pillars'
        for point in self.__pillar:
            [y, x] = point
            pillars_draw += draw + ''.join(str(tuple([x, y])).split()) + ' circle(0.2);'
        return pillars_draw

    def __inners_draw(self):
        inners_draw = '\n% Inner points in accessible cul-de-sacs'
        draw = '\n    \\node at '
        self.__xPoint.sort()
        for point in self.__xPoint:
            [y, x] = point
            inners_draw += draw + ''.join(str(tuple([x + 0.5, y + 0.5])).split()) + ' {};'
        return inners_draw

    def __draw_door(self, x, y, space):  # l:0 r:1,u:2,d:3
        if self.__spaceSet[x][y] == self.__spaceSet[x - 1][y] and self.__spaceSet[x - 2][y] == 1:
            space[x - 1][y] = space[x - 2][y] = 1
        if self.__spaceSet[x][y] == self.__spaceSet[x + 1][y] and self.__spaceSet[x + 2][y] == 1:
            space[x + 1][y] = space[x + 2][y] = 1
        if self.__spaceSet[x][y] == self.__spaceSet[x][y - 1] and self.__spaceSet[x][y - 2] == 1:
            space[x][y - 1] = space[x][y - 2] = 1
        if self.__spaceSet[x][y] == self.__spaceSet[x][y + 1] and self.__spaceSet[x][y + 2] == 1:
            space[x][y + 1] = space[x][y + 2] = 1
        return space

    def __entry_exit_draw(self):
        entry_exit_draw = '\n% Entry-exit paths without intersections'
        draw = "\n    \\draw[dashed, yellow] "
        line = 0
        while line < len(self.__spaceSet):
            character = 0
            self.__path_route.append([])
            while character < len(self.__spaceSet[0]):
                self.__path_route[-1].append(0)
                character += 1
            line += 1
        for line in self.__path_point:
            for character in line:
                self.__path_route[character[0]][character[1]] = 1
                self.__path_route = self.__draw_door(character[0], character[1], self.__path_route)
                if character[0] > 2 and self.__spaceSet[character[0] - 1][character[1]] != 0 \
                        and [character[0] - 2, character[1]] in line:
                    self.__path_route[character[0] - 1][character[1]] = 1
                if character[1] > 2 and self.__spaceSet[character[0]][character[1] - 1] != 0 \
                        and [character[0], character[1] - 2] in line:
                    self.__path_route[character[0]][character[1] - 1] = 1

        sign = 0
        line = 0
        while line < len(self.__path_route):
            character = 0
            while character < len(self.__path_route[line]):
                if self.__path_route[line][character] != 0 and character < len(self.__path_route[line]) - 1 and \
                        self.__path_route[line][character + 1] != 0:
                    if sign == 0:
                        start = (character * 0.5 - 0.5, line * 0.5 - 0.5)
                        sign = 1
                else:
                    if sign == 1:
                        end = (character * 0.5 - 0.5, line * 0.5 - 0.5)
                        entry_exit_draw += draw + ''.join(str(start).split()) + ' -- ' + ''.join(str(end).split()) + ';'
                        sign = 0
                character += 1
            line += 1
        sign = 0
        line = 0
        while line < len(self.__path_route[0]):
            character = 0
            while character < len(self.__path_route):
                if self.__path_route[character][line] != 0 and character < len(self.__path_route) - 1 and \
                        self.__path_route[character + 1][line] != 0:
                    if sign == 0:
                        start = (line * 0.5 - 0.5, character * 0.5 - 0.5)
                        sign = 1
                else:
                    if sign == 1:
                        end = (line * 0.5 - 0.5, character * 0.5 - 0.5)
                        entry_exit_draw += draw + ''.join(str(start).split()) + ' -- ' + ''.join(str(end).split()) + ';'
                        sign = 0
                character += 1
            line += 1
        return entry_exit_draw

    def display(self):
        latex = '''\\documentclass[10pt]{article}
\\usepackage{tikz}
\\usetikzlibrary{shapes.misc}
\\usepackage[margin=0cm]{geometry}
\\pagestyle{empty}
\\tikzstyle{every node}=[cross out, draw, red]

\\begin{document}

\\vspace*{\\fill}
\\begin{center}
\\begin{tikzpicture}[x=0.5cm, y=-0.5cm, ultra thick, blue]'''
        latex += self.__walls_draw()
        latex += self.__pillars_draw()
        latex += self.__inners_draw()
        latex += self.__entry_exit_draw()
        latex += '''\n\\end{tikzpicture}
\\end{center}
\\vspace*{\\fill}

\\end{document}\n'''
        fp = open(self.__file, 'w')
        fp.write(latex)
        fp.close()
