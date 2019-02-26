# Using deque would be much faster. I am only posting my codes though, and I didn't
# know deque until I looked for solutions on Reddit.

from collections import defaultdict


PLAYERS = 9
LAST_MARBLE = 25


class Marble:
    def __init__(self, value):
        self.value = value
        self.next = None
        self.prev = None


class Game:
    def __init__(self, players_num, last_marble):
        self.players_num = players_num
        self.last_marble = last_marble
        self.current_marble = Marble(0)
        self.current_marble.next = self.current_marble
        self.current_marble.prev = self.current_marble
        self.last_placed_marble = 0
        self.scores = defaultdict(int)

    def get_marble_to_remove(self):
        """Returns the marble 7 marbles counter-clockwise from the current marble"""
        result = self.current_marble
        for i in range(7):
            result = result.prev
        return result

    def add_marble(self):
        self.last_placed_marble += 1
        if self.last_placed_marble % 23 == 0:
            self.scores[self.last_placed_marble % self.players_num] += self.last_placed_marble
            to_remove = self.get_marble_to_remove()
            self.scores[self.last_placed_marble % self.players_num] += to_remove.value
            to_remove.prev.next = to_remove.next
            to_remove.next.prev = to_remove.prev
            self.current_marble = to_remove.next
        else:
            added = Marble(self.last_placed_marble)
            first = self.current_marble.next
            second = first.next
            first.next = added
            second.prev = added
            added.prev = first
            added.next = second
            self.current_marble = added

    def __str__(self):
        result = "[" + str(self.last_placed_marble % self.players_num) + "] "
        i = self.current_marble
        result += "(" + str(i.value) + ") "
        i = i.next
        while i != self.current_marble:
            result += " " + str(i.value) + " "
            i = i.next
        return result

    def play(self):
        """Plays the whole game."""
        if self.last_placed_marble < self.last_marble:
            for i in range(self.last_placed_marble, self.last_marble):
                self.add_marble()

    # takes like 11 seconds
    def play100(self):
        """Plays the whole game with last marble being 100 times larger."""
        if self.last_placed_marble < self.last_marble * 100:
            for i in range(self.last_placed_marble, self.last_marble * 100):
                self.add_marble()

    def get_winning_score(self):
        result = 0
        for score in self.scores.values():
            if score > result:
                result = score
        return result


def main():
    game = Game(PLAYERS, LAST_MARBLE)
    game.play()
    print(game.get_winning_score())  # part 1

    game.play100()
    print(game.get_winning_score())  # part 2


main()
