from typing import List, Set
from pygame.math import Vector2 as Vec2
from .entities import Hunter, Hare, BaseEntity, Projectile, Wolf, Llama
from .world import World
from .utils import rand_vec2
from .hud import Hud


class EntityManager:
    def __init__(self, world: World, hud: Hud):
        self.world = world
        self.hud = hud
        self.hunter: Hunter = Hunter(world.rand_pos())
        self.hares: List[Hare] = [Hare(world.rand_pos()) for _ in range(10)]
        # self.hares = []
        self.wolves: List[Wolf] = [Wolf(world.rand_pos()) for _ in range(4)]
        self.llamas: List[Llama] = [Llama(world.rand_pos()) for _ in range(4)]
        self.projectiles: List[Projectile] = []

    def update(self, dt: float, world: World):
        self.hunter.avoid_borders(world)
        self.hunter.update(dt)

        died_proj = set()  # Proj. to be removed from scene
        died_entities = set()

        for hare in self.hares:
            hare.wander()
            hare.avoid_borders(world)
            # hare.flee_target(self.hunter.pos)
            hare.apply_behavior(hare.flee_target, self.hares)
            hare.apply_behavior(hare.flee_target, self.wolves)
            hare.update(dt)
            self._proj_collision(hare, died_entities, died_proj)

        for wolf in self.wolves:
            wolf.wander()
            wolf.avoid_borders(world)
            # wolf.apply_behavior(wolf.seek_target, self.hares)
            wolf.seek_target(self.hunter.pos)
            self._proj_collision(wolf, died_entities, died_proj)
            wolf.update(dt)

        for llama in self.llamas:
            llama.wander()
            llama.flock(self.llamas)
            hare.apply_behavior(hare.flee_target, self.wolves)
            self._proj_collision(llama, died_entities, died_proj)
            llama.update(dt)

        for proj in self.projectiles:
            proj.update(dt)
            if not self.world.bound_rect.collidepoint(proj.pos.x, proj.pos.y):
                died_proj.add(proj)

        if died_entities:
            print(died_entities)
            self.hud.play_damage()

        for proj in died_proj:
            self.projectiles.remove(proj)

    def follow_mouse(self, pos: Vec2):
        self.hunter.seek_target(pos)

    def hunter_shoot(self):
        self.projectiles.append(Projectile(self.hunter))

    def _proj_collision(self, ent: BaseEntity, died_ent: Set[BaseEntity],
                        died_proj: Set[Projectile]):
        colls = ent.collision(self.projectiles)
        if colls:
            died_ent.add(ent)
            # Removind only 1st bullet to allow to pass
            died_proj.add(colls[0])

    def get_all_entities(self) -> List[BaseEntity]:
        return self.hares + self.wolves + self.llamas + self.projectiles + [
            self.hunter
        ]
