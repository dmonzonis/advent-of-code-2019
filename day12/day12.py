import re


class Moon:
    def __init__(self, x, y, z):
        self.pos = [int(x), int(y), int(z)]
        self.velocity = [0, 0, 0]

    def move(self):
        """Modify the moon's position by its velocity, without changing the velocity."""
        for axis in range(3):
            self.pos[axis] += self.velocity[axis]

    def kinetic_energy(self):
        return sum(abs(i) for i in self.velocity)

    def potential_energy(self):
        return sum(abs(i) for i in self.pos)

    def total_energy(self):
        return self.kinetic_energy() * self.potential_energy()

    def __repr__(self):
        return f"({self.pos[0]}, {self.pos[1]}, {self.pos[2]})"


def apply_gravity(m, n):
    """Applies gravity between two moons m and n, modifying their velocities."""
    for axis in range(3):
        if m.pos[axis] < n.pos[axis]:
            m.velocity[axis] += 1
            n.velocity[axis] -= 1
        elif m.pos[axis] > n.pos[axis]:
            m.velocity[axis] -= 1
            n.velocity[axis] += 1


def apply_all_gravities(moons):
    """Applies gravity between all the moons in the list, modifying their velocities."""
    for i, moon in enumerate(moons):
        for j in range(i + 1, len(moons)):
            apply_gravity(moon, moons[j])


def main():
    with open("input.txt") as f:
        moons = []
        for l in f.readlines():
            matches = re.match(r"<x=(-?\d+), y=(-?\d+), z=(-?\d+)>", l.strip())
            moons.append(Moon(matches.group(1), matches.group(2), matches.group(3)))
    steps = 1000
    for i in range(steps):
        apply_all_gravities(moons)
        for moon in moons:
            moon.move()

    total_energy = sum(m.total_energy() for m in moons)
    print(f"Total energy: {total_energy}")


if __name__ == "__main__":
    main()
