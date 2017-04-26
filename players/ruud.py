from game import moves
from game.mazefield_attributes import Start, Path, Finish, Wall
from players.player import Player
from heapq import heappush, heappop
from os import abort

directions = [moves.RIGHT, moves.UP, moves.LEFT, moves.DOWN]


def look_at(surroundings, direction):
    return {
        moves.RIGHT: surroundings.right,
        moves.UP: surroundings.up,
        moves.LEFT: surroundings.left,
        moves.DOWN: surroundings.down
    }[direction]


def offset(direction):
    return {
        moves.RIGHT: (1, 0),
        moves.UP: (0, 1),
        moves.LEFT: (-1, 0),
        moves.DOWN: (0, -1)
    }[direction]


def directions_where(surroundings, expected):
    return [d for d in directions if look_at(surroundings, d) is expected]


def add(p, q):
    (px, py) = p
    (qx, qy) = q
    return (px + qx, py + qy)


class Ruud(Player):
    name = "Ruud"

    def __init__(self):
        self.maze = {
            (0, 0): Start
        }
        self.position = (0, 0)
        self.current_route = []


    def observe(self, surroundings):
        for d in directions:
            self.maze[add(self.position, offset(d))] = look_at(surroundings, d)

    def route_to_nearest_unknown(self):
        heap = [(0, self.position)]
        done = {self.position: self.position}
        done_moves = {}
        goal = None

        while heap:
            cost, pos = heappop(heap)
            for d in directions:
                dpos = add(pos, offset(d))
                at = self.maze.get(dpos)

                if dpos in done:
                    continue

                done[dpos] = pos
                done_moves[dpos] = d

                if at is None:
                    goal = dpos
                    break
                elif at is Path:
                    heappush(heap, (cost + 1, dpos))

            if goal:
                break

        assert goal is not None, 'Maze must have exit.'

        route = []
        while goal != self.position:
            route.append(done_moves[goal])
            goal = done[goal]

        return route

    def turn(self, surroundings):
        # If we can reach the finish, go there.
        for d in directions_where(surroundings, Finish):
            return d

        self.observe(surroundings)
        move = self.route_to_nearest_unknown().pop()
        self.position = add(self.position, offset(move))
        return move
