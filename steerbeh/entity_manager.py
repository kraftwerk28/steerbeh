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
        self.wolves: List[Wolf] = [Wolf(world.rand_pos()) for _ in range(4)]
        self.wolves = []
        self.llamas: List[Llama] = [Llama(world.rand_pos()) for _ in range(8)]
        self.projectiles: List[Projectile] = []

    def update(self, dt: float, world: World):
        self.hunter.avoid_borders(world)
        self.hunter.update(dt)

        died_proj = set()  # Proj. to be removed from scene
        died_entities = set()
        entities = self.get_all_entities()
        rects = [e.hitbox for e in entities]

        for hare in self.hares:
            hare.wander()
            hare.avoid_borders(world)
            hare.flee_target(self.hunter.pos)
            hare.apply_behavior(hare.flee_target, self.hares)
            hare.apply_behavior(hare.flee_target, self.wolves)
            hare.apply_behavior(hare.flee_target, self.llamas)
            hare.update(dt)

        for wolf in self.wolves:
            wolf.wander()
            wolf.avoid_borders(world)
            wolf.apply_behavior(wolf.seek_target, self.hares)
            wolf.apply_behavior(wolf.seek_target, self.llamas)
            wolf.seek_target(self.hunter.pos)
            for coll_idx in wolf.hitbox.collidelistall(rects):
                ent = entities[coll_idx]
                if type(ent) in Wolf.killable_entities:
                    died_entities.add(ent)
            wolf.update(dt)

        for llama in self.llamas:
            llama.wander()
            llama.avoid_borders(world)
            llama.flock(self.llamas)
            llama.apply_behavior(llama.flee_target, self.wolves)
            llama.update(dt)

        for proj in self.projectiles:
            proj.update(dt)
            coll = proj.hitbox.collidelistall(rects)
            for coll_idx in proj.hitbox.collidelistall(rects):
                ent = entities[coll_idx]
                if type(ent) not in (Projectile, Hunter):
                    died_proj.add(proj)
                    died_entities.add(ent)
            if not self.world.bound_rect.collidepoint(proj.pos.x, proj.pos.y):
                died_proj.add(proj)

        for ent in entities:
            if (not world.bound_rect.contains(ent.hitbox)
                    and type(ent) != Projectile):
                died_entities.add(ent)

        if died_entities:
            self.cleanup_entities(died_entities)
            self.hud.play_damage()

        for proj in died_proj:
            self.projectiles.remove(proj)

    def follow_mouse(self, pos: Vec2):
        self.hunter.seek_target(pos)

    def hunter_shoot(self):
        self.projectiles.append(Projectile(self.hunter))

    def cleanup_entities(self, died_entities: Set[BaseEntity]):
        for e in died_entities:
            ty = type(e)
            if ty == Hare:
                self.hares.remove(e)
            if ty == Llama:
                self.llamas.remove(e)
            elif ty == Wolf:
                self.wolves.remove(e)

    def get_all_entities(self,
                         with_hunter=True,
                         with_projectiles=True) -> List[BaseEntity]:
        res = self.hares + self.wolves + self.llamas
        if with_hunter:
            res.append(self.hunter)
        if with_projectiles:
            res += self.projectiles
        return res
