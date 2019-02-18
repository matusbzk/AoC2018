import re
from datetime import datetime
from enum import Enum
import itertools


start_shift_regex = re.compile("\\[(\\d+)\\-(\\d+)\\-(\\d+) (\\d+):(\\d+)\\] Guard #(\\d+) begins shift")
fall_asleep_regex = re.compile("\\[(\\d+)\\-(\\d+)\\-(\\d+) (\\d+):(\\d+)\\] falls asleep")
wake_up_regex = re.compile("\\[(\\d+)\\-(\\d+)\\-(\\d+) (\\d+):(\\d+)\\] wakes up")


def get_minute(when: datetime, default = 0):
    if when.time().hour != 0:
        return default
    else:
        return when.time().minute


def get_guard(guard_id, guards_dict):
    if guard_id in guards_dict:
        return guards_dict[guard_id]
    guard = Guard(guard_id)
    guards_dict[guard_id] = guard
    return guard


def get_guard_with_most_minutes_asleep(guards_dict):
    most = 0
    most_guard = None
    for guard in guards_dict.values():
        minutes_asleep = guard.minutes_asleep()
        if minutes_asleep > most:
            most = minutes_asleep
            most_guard = guard
    return most_guard


def get_guard_id_and_minute_most_asleep(guards_dict):
    """This is basically the answer for part 2"""
    most = 0
    most_guard_id = None
    most_minute = None
    for guard, mnt in itertools.product(guards_dict.values(), range(60)):
        if guard.sleeping_tracker[mnt] > most:
            most = guard.sleeping_tracker[mnt]
            most_guard_id = guard.id
            most_minute = mnt
    return most_guard_id, most_minute


class Guard:
    def __init__(self, guard_id):
        self.id = guard_id
        self.awake_from_minute = None
        self.sleeping_from_minute = None
        self.sleeping_tracker = [0] * 60

    def begin_shift(self, when: datetime):
        if when.time().hour != 0:
            self.awake_from_minute = 0
        else:
            self.awake_from_minute = when.time().minute

    def end_shift(self, when: datetime):
        minute = get_minute(when, 59)
        if self.sleeping_from_minute is not None:
            for mnt in range(self.sleeping_from_minute, minute):
                self.sleeping_tracker[mnt] += 1
        self.awake_from_minute = None
        self.sleeping_from_minute = None

    def fall_asleep(self, when: datetime):
        minute = get_minute(when, 0)
        self.sleeping_from_minute = minute
        self.awake_from_minute = None

    def wake_up(self, when: datetime):
        minute = get_minute(when, 0)
        for mnt in range(self.sleeping_from_minute, minute):
            self.sleeping_tracker[mnt] += 1
        self.awake_from_minute = minute
        self.sleeping_from_minute = None

    def minutes_asleep(self):
        minutes = 0
        for mnt in self.sleeping_tracker:
            minutes += mnt
        return minutes

    def minute_asleep_most(self):
        most = 0
        most_index = 0
        for i in range(60):
            if most < self.sleeping_tracker[i]:
                most = self.sleeping_tracker[i]
                most_index = i
        return most_index


class EventType(Enum):
    BEGIN_SHIFT = 0
    FALL_ASLEEP = 1
    WAKE_UP = 2


class Event:
    def __init__(self, input_line):
        start_matched = start_shift_regex.match(input_line)
        if start_matched:
            self.when = datetime(int(start_matched.group(1)), int(start_matched.group(2)),
                                 int(start_matched.group(3)), int(start_matched.group(4)),
                                 int(start_matched.group(5)))
            self.event_type = EventType.BEGIN_SHIFT
            self.guard_id = int(start_matched.group(6))
        else:
            fall_asleep_matched = fall_asleep_regex.match(input_line)
            if fall_asleep_matched:
                self.when = datetime(int(fall_asleep_matched.group(1)), int(fall_asleep_matched.group(2)),
                                     int(fall_asleep_matched.group(3)), int(fall_asleep_matched.group(4)),
                                     int(fall_asleep_matched.group(5)))
                self.event_type = EventType.FALL_ASLEEP
                self.guard_id = None
            else:
                wake_up_matched = wake_up_regex.match(input_line)
                if wake_up_matched:
                    self.when = datetime(int(wake_up_matched.group(1)), int(wake_up_matched.group(2)),
                                         int(wake_up_matched.group(3)), int(wake_up_matched.group(4)),
                                         int(wake_up_matched.group(5)))
                    self.event_type = EventType.WAKE_UP
                    self.guard_id = None
                else:
                    raise ValueError("Could not parse line: " + input_line)

    def analyze_event(self, guard_id, guards_dict):
        if self.event_type == EventType.BEGIN_SHIFT:
            guard = get_guard(self.guard_id, guards_dict)
            guard.begin_shift(self.when)
            old_guard = get_guard(guard_id, guards_dict)
            old_guard.end_shift(self.when)
        elif self.event_type == EventType.FALL_ASLEEP:
            self.guard_id = guard_id
            guard = get_guard(guard_id, guards_dict)
            guard.fall_asleep(self.when)
        elif self.event_type == EventType.WAKE_UP:
            self.guard_id = guard_id
            guard = get_guard(guard_id, guards_dict)
            guard.wake_up(self.when)
        else:
            raise ValueError("Could not analyze event: " + self.when)


guards = {}
events = []

with open("input.txt", "r") as puzzle_input:
    for line in puzzle_input:
        event = Event(line)
        events.append(event)

events.sort(key=lambda x: x.when)

current_guard_id = None
for event in events:
    event.analyze_event(current_guard_id, guards)
    current_guard_id = event.guard_id

my_guard: Guard = get_guard_with_most_minutes_asleep(guards)

print(my_guard.id * my_guard.minute_asleep_most())  # part 1

most_asleep_at_minute_guard_id, minute_most_asleep = get_guard_id_and_minute_most_asleep(guards)

print(most_asleep_at_minute_guard_id * minute_most_asleep)  # part 2
