from random import randint
from kikan import engine, Entity, Vector
from kikan.entity import EmptyObject, Pixel, Texture, StepSides
from kikan.utils import Logger


def random_position():
    return Vector(
        randint(-engine.screen.screen.width // 2, engine.screen.screen.width // 2),
        randint(-engine.screen.screen.height // 2, engine.screen.screen.height // 2),
    )


class Snake(Entity):
    Texture = Texture([[Pixel("@")]])

    def __init__(self):
        super().__init__(Vector(0, 0), self.Texture)
        self.velocity_factor = 3
        self.velocity = Vector(0, 1) * self.velocity_factor
        self.parts = [SnakeTailPart(Vector(0, i)) for i in range(-1, -3, -1)]
        self.dp = Vector(0, 0)

    def on_input(self, key):
        match key:
            case "up":
                self.velocity = Vector(0, 1)
            case "down":
                self.velocity = Vector(0, -1)
            case "right":
                self.velocity = Vector(1, 0)
            case "left":
                self.velocity = Vector(-1, 0)
        self.velocity *= self.velocity_factor

    def on_pre_update(self, dt):
        if self.prev_pos != None:
            self.position = self.prev_pos * 1

        if (
            abs(self.position.x) >= engine.screen.screen.width / 2
            or abs(self.position.y) >= engine.screen.screen.height / 2
        ):
            GameManager.stop_game()

        # for i in range(len(self.parts) - 1):
        #     current, next = self.parts[i], self.parts[i + 1]
        #     cp, np = current.position, next.position
        #     d = cp + current.velocity * dt - np - next.velocity * dt
        #     if abs(d.x) >= 0.5:
        #         ...
        #         # Logger.print(f"{current} {next} bad {d}")
        #         next.velocity = (
        #             Vector(int(math.copysign(1, d.x)), 0) * self.velocity_factor
        #         )
        #     elif abs(d.y) >= 0.5:
        #         next.velocity = (
        #             Vector(0, int(math.copysign(1, d.y))) * self.velocity_factor
        #         )
        #         # Logger.print(f"{current} {next} too bad {d}")

        # Logger.print(f"parts {[part.position for part in self.parts]}")

        self.parts.insert(0, SnakeTailPart(self.position))
        self.parts[-1].destroy()
        self.parts.pop()

        # if (
        #     abs(
        #         dx := (cp.x + current.velocity.x * dt - np.x - next.velocity.x * dt)
        #     )
        #     >= 0.25
        #     and abs(
        #         dy := (cp.y + current.velocity.y * dt - np.y - next.velocity.y * dt)
        #     )
        #     >= 0.25
        # ):
        #     if abs(dx) > abs(dy):  # x difference bigger than y one
        #         next.velocity = Vector(int(math.copysign(1, dx)), 0)
        #     else:  # vice versa
        #         next.velocity = Vector(0, int(math.copysign(1, dy)))
        #     next.velocity *= self.velocity_factor

    def on_update(self, dt):
        self.prev_pos = self.position * 1
        self.position = Vector(int(self.position.x), int(self.position.y))
        Logger.print(f"parts {self.position, self.prev_pos}")

    def on_collision(self, other):
        if other is not self.parts[0] and isinstance(other, SnakeTailPart):
            # engine.stop()
            ...
        elif isinstance(other, Apple):
            apple.is_eaten = True
            self.velocity_factor += 0.5
            self.add_part()

    def add_part(self):
        self.parts.append(SnakeTailPart(self.position))


class SnakeTailPart(Entity):
    VerticalTexture = Texture([[Pixel("|")]])
    HorizonalTexture = Texture([[Pixel("-")]])
    CornerTexture = Texture([[Pixel("+")]])

    def __init__(self, position):
        super().__init__(position, "*")

    def on_pre_update(self, dt):
        if self.prev_pos != None:
            self.position = self.prev_pos * 1

    def on_update(self, dt):
        self.prev_pos = self.position * 1
        self.position = Vector(int(self.position.x), int(self.position.y))


class Apple(Entity):
    def __init__(self):
        super().__init__(Vector(-5, 0), Texture([[Pixel("o", (255, 0, 0))]]))
        self.is_eaten = False

    def respawn(self):
        parts_coords = [i.position for i in snake.parts]
        self.position = random_position()
        while self.position in parts_coords:
            self.position = random_position()
        self.is_eaten = False


class GameManager(EmptyObject):
    @classmethod
    def on_update(cls, dt):
        if apple.is_eaten:
            apple.respawn()
        engine.screen.display_string(-40, 10, f"Score: {len(snake.parts)}")

    @staticmethod
    def stop_game():
        engine.stop()


snake = Snake()
apple = Apple()

engine.start()

print(len(snake.parts))
