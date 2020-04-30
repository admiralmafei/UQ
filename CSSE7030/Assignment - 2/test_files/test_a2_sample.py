#!/usr/bin/env python3

"""
PLEASE NOTE:
These are sample tests. Passing all tests does not guarantee complete correctness.
You should also run gui.py once complete to see if you can play the full game, as
well as performing your own tests to ensure you have meet ALL the criteria outlined.

Please make sure to stay up to date for any assignment or test file updates.
"""

import inspect
from typing import Dict, List, Optional, Tuple

from testrunner import AttributeGuesser, OrderedTestCase, TestMaster, skipIfFailed

Position = Tuple[int, int]


class Tile:
    def __init__(self, name: str, selectable: bool = True): pass
    def get_name(self) -> str: pass
    def get_id(self) -> str: pass
    def set_select(self, select: bool): pass
    def can_select(self) -> bool: pass
    def __str__(self) -> str: pass
    def __repr__(self) -> str: pass


class Pipe:
    def __init__(self, name: str, orientation: int = 0, selectable: bool = True): pass
    def get_connected(self, side: str) -> List[str]: pass
    def rotate(self, direction: int): pass
    def get_orientation(self) -> int: pass
    def __str__(self) -> str: pass
    def __repr__(self) -> str: pass


class SpecialPipe:
    def __str__(self) -> str: pass
    def __repr__(self) -> str: pass


class StartPipe:
    def __init__(self, orientation: int = 0): pass
    def get_connected(self, side: int = None) -> List[str]: pass
    def __str__(self) -> str: pass
    def __repr__(self) -> str: pass


class EndPipe:
    def __init__(self, orientation: int = 0): pass
    def get_connected(self, side: int = None) -> List[str]: pass
    def __str__(self) -> str: pass
    def __repr__(self) -> str: pass


class PipeGame:
    def __init__(self, game_file: str = 'game_1.csv'): pass
    def get_board_layout(self) -> List[List[Tile]]: pass
    def get_playable_pipes(self) -> Dict[str, int]: pass
    def change_playable_amount(self, pipe_name: str, number: int): pass
    def get_pipe(self, position: Position) -> Tile: pass
    def set_pipe(self, pipe: Pipe, position: Position): pass
    def pipe_in_position(self, position: Position) -> Optional[Pipe]: pass
    def remove_pipe(self, position: Position): pass
    def position_in_direction(self, direction: str, position: Position) -> Optional[Tuple[str, Position]]: pass
    def end_pipe_positions(self): pass
    def get_starting_position(self) -> Position: pass
    def get_ending_position(self) -> Position: pass
    def check_win(self) -> bool: pass


class A2:
    Tile = Tile
    Pipe = Pipe
    SpecialPipe = SpecialPipe
    StartPipe = StartPipe
    EndPipe = EndPipe
    PipeGame = PipeGame


class TestA2(OrderedTestCase):
    a2: A2


class TestDesign(TestA2):
    def test_clean_import(self):
        """ test no prints on import """
        self.assertIsCleanImport(self.a2, msg="You should not be printing on import for a1.py")

    def test_classes_and_functions_defined(self):
        """ test all specified classes and functions defined correctly """
        a2 = AttributeGuesser(self.a2, fail=False)

        self._aggregate_class_and_functions_defined(a2, Tile)
        self._aggregate_class_and_functions_defined(a2, Pipe, Tile)
        self._aggregate_class_and_functions_defined(a2, SpecialPipe, Pipe, Tile)
        self._aggregate_class_and_functions_defined(a2, StartPipe, SpecialPipe, Pipe, Tile)
        self._aggregate_class_and_functions_defined(a2, EndPipe, SpecialPipe, Pipe, Tile)
        self._aggregate_class_and_functions_defined(a2, PipeGame)

        self.aggregate_tests()

    def _aggregate_class_and_functions_defined(self, module, test_class, *classes):
        cls_name = test_class.__name__
        if not self.aggregate(self.assertClassDefined, module, cls_name, tag=cls_name):
            return

        if classes and hasattr(module, classes[0].__name__):
            self.aggregate(self.assertIsSubclass, getattr(module, cls_name), getattr(module, classes[0].__name__))

        classes = (test_class,) + classes
        members = {k: v for cls in classes[::-1] for k, v in inspect.getmembers(cls, predicate=inspect.isfunction)}
        for func_name, func in sorted(members.items()):
            if func_name == '__init__' and SpecialPipe in classes:
                continue

            num_params = len(inspect.signature(func).parameters)
            self.aggregate(self.assertFunctionDefined, getattr(module, cls_name), func_name, num_params,
                           tag=f'{cls_name}.{func_name}')

    def test_doc_strings(self):
        """ test all classes and functions have documentation strings """
        a2 = AttributeGuesser.get_wrapped_object(self.a2)
        ignored = frozenset(('__str__', '__repr__'))
        for func_name, func in inspect.getmembers(a2, predicate=inspect.isfunction):
            if func_name != 'main':
                self.aggregate(self.assertDocString, func)

        for cls_name, cls in inspect.getmembers(a2, predicate=inspect.isclass):
            self.aggregate(self.assertDocString, cls)
            defined = vars(cls)
            for func_name, func in inspect.getmembers(cls, predicate=inspect.isfunction):
                if func_name not in ignored and func_name in defined:
                    self.aggregate(self.assertDocString, func)

        self.aggregate_tests()


@skipIfFailed(TestDesign, TestDesign.test_classes_and_functions_defined.__name__, tag=Tile.__name__)
class TestTile(TestA2):
    def test_get_name(self):
        """ test Tile.get_name """
        tile = self.a2.Tile('#')
        result = tile.get_name()
        self.assertEqual(result, '#')

    def test_get_id(self):
        """ test Tile.get_id """
        tile = self.a2.Tile('#')
        result = tile.get_id()
        self.assertEqual(result, "tile")

    def test_can_select_default(self):
        """ test Tile.can_select defaults True """
        tile = self.a2.Tile('#')
        result = tile.can_select()
        self.assertIs(result, True)

    def test_can_select(self):
        """ test Tile.can_select __init__ set """
        tile = self.a2.Tile('#', False)
        result = tile.can_select()
        self.assertIs(result, False)

    def test_str(self):
        """ test Tile.__str__ defaults True """
        tile = self.a2.Tile('#')
        result = str(tile)
        self.assertEqual(result, "Tile('#', True)")

    def test_repr(self):
        """ test Tile.__repr__ defaults True """
        tile = self.a2.Tile('#')
        result = repr(tile)
        self.assertEqual(result, "Tile('#', True)")


@skipIfFailed(TestDesign, TestDesign.test_classes_and_functions_defined.__name__, tag=Pipe.__name__)
class TestPipe(TestA2):
    def test_get_name(self):
        """ test Pipe.get_name """
        pipe = self.a2.Pipe("straight")
        result = pipe.get_name()
        self.assertEqual(result, "straight")

    def test_get_id(self):
        """ test Pipe.get_id """
        pipe = self.a2.Pipe("straight")
        result = pipe.get_id()
        self.assertEqual(result, "pipe")

    def test_str(self):
        """ test Pipe.__str__ defaults True """
        pipe = self.a2.Pipe("straight")
        result = str(pipe)
        self.assertEqual(result, "Pipe('straight', 0)")

    def test_repr(self):
        """ test Pipe.__repr__ defaults True """
        pipe = self.a2.Pipe("straight")
        result = repr(pipe)
        self.assertEqual(result, "Pipe('straight', 0)")

    def test_get_orientation_default(self):
        """ test Pipe.get_orientation defaults 0 """
        pipe = self.a2.Pipe("straight")
        result = pipe.get_orientation()
        self.assertEqual(result, 0)

    def test_get_orientation(self):
        """ test Pipe.get_orientation __init__ set """
        pipe = self.a2.Pipe("straight", 1)
        result = pipe.get_orientation()
        self.assertEqual(result, 1)

    def test_rotate_once(self):
        """ test Pipe.rotate once """
        pipe = self.a2.Pipe("straight")
        ret = pipe.rotate(1)
        result = pipe.get_orientation()
        self.assertEqual(result, 1)
        self.assertIsNone(ret, "Pipe.rotate should not return")

    @skipIfFailed(test_name=test_rotate_once.__name__)
    def test_full_rotation(self):
        """ test Pipe.rotate 4 times """
        pipe = self.a2.Pipe("straight")
        pipe.rotate(1)
        pipe.rotate(1)
        pipe.rotate(1)
        pipe.rotate(1)
        result = pipe.get_orientation()
        self.assertEqual(result, 0)

    def test_get_connected_straight_0_N(self):
        """ test Pipe.get_connected straight 0 'N' """
        pipe = self.a2.Pipe("straight")
        result = pipe.get_connected('N')
        self.assertListEqual(result, ['S'])

    def test_get_connected_straight_0_E(self):
        """ test Pipe.get_connected straight 0 'E' """
        pipe = self.a2.Pipe("straight")
        result = pipe.get_connected('E')
        self.assertListEqual(result, [])

    def test_get_connected_straight_0_S(self):
        """ test Pipe.get_connected straight 0 'S' """
        pipe = self.a2.Pipe("straight")
        result = pipe.get_connected('S')
        self.assertListEqual(result, ['N'])

    def test_get_connected_straight_rotate_1_E(self):
        """ test Pipe.get_connected straight rotate 1 'E' """
        pipe = self.a2.Pipe("straight")
        pipe.rotate(1)
        result = pipe.get_connected('E')
        self.assertListEqual(result, ['W'])


@skipIfFailed(TestDesign, TestDesign.test_classes_and_functions_defined.__name__, tag=SpecialPipe.__name__)
class TestSpecialPipe(TestA2):
    def test_get_id(self):
        """ test SpecialPipe.get_id """
        pipe = self.a2.SpecialPipe("start")
        result = pipe.get_id()
        self.assertEqual(result, "special_pipe")

    def test_get_name(self):
        """ test SpecialPipe.get_name """
        pipe = self.a2.SpecialPipe("start")
        result = pipe.get_name()
        self.assertEqual(result, "start")

    def test_get_orientation_default(self):
        """ test SpecialPipe.get_orientation defaults 0 """
        pipe = self.a2.SpecialPipe("start")
        result = pipe.get_orientation()
        self.assertEqual(result, 0)

    def test_get_orientation(self):
        """ test SpecialPipe.get_orientation __init__ set """
        pipe = self.a2.SpecialPipe("start", 1)
        result = pipe.get_orientation()
        self.assertEqual(result, 1)

    def test_str(self):
        """ test SpecialPipe.__str__ """
        pipe = self.a2.SpecialPipe("start")
        result = str(pipe)
        self.assertEqual(result, "SpecialPipe(0)")

    def test_repr(self):
        """ test SpecialPipe.__repr__ """
        pipe = self.a2.SpecialPipe("start")
        result = repr(pipe)
        self.assertEqual(result, "SpecialPipe(0)")


@skipIfFailed(TestDesign, TestDesign.test_classes_and_functions_defined.__name__, tag=StartPipe.__name__)
class TestStartPipe(TestA2):
    def test_get_name(self):
        """ test StartPipe.get_name """
        pipe = self.a2.StartPipe()
        result = pipe.get_name()
        self.assertEqual(result, "start")

    def test_get_id(self):
        """ test StartPipe.get_id """
        pipe = self.a2.StartPipe()
        result = pipe.get_id()
        self.assertEqual(result, "special_pipe")

    def test_str(self):
        """ test StartPipe.__str__ """
        pipe = self.a2.StartPipe()
        result = str(pipe)
        self.assertEqual(result, "StartPipe(0)")

    def test_repr(self):
        """ test StartPipe.__repr__ """
        pipe = self.a2.StartPipe()
        result = repr(pipe)
        self.assertEqual(result, "StartPipe(0)")

    def test_get_orientation_default(self):
        """ test StartPipe.get_orientation defaults 0 """
        pipe = self.a2.StartPipe()
        result = pipe.get_orientation()
        self.assertEqual(result, 0)

    def test_get_orientation(self):
        """ test StartPipe.get_orientation __init__ set """
        pipe = self.a2.StartPipe(1)
        result = pipe.get_orientation()
        self.assertEqual(result, 1)

    def test_get_connected_0(self):
        """ test StartPipe.get_connected orientation 0 """
        pipe = self.a2.StartPipe()
        result = pipe.get_connected()
        self.assertEqual(result, ['N'])

    def test_get_connected_1(self):
        """ test StartPipe.get_connected orientation 1 """
        pipe = self.a2.StartPipe(1)
        result = pipe.get_connected()
        self.assertEqual(result, ['E'])


@skipIfFailed(TestDesign, TestDesign.test_classes_and_functions_defined.__name__, tag=EndPipe.__name__)
class TestEndPipe(TestA2):
    def test_get_name(self):
        """ test EndPipe.get_name """
        pipe = self.a2.EndPipe()
        result = pipe.get_name()
        self.assertEqual(result, "end")

    def test_get_id(self):
        """ test EndPipe.get_id """
        pipe = self.a2.EndPipe()
        result = pipe.get_id()
        self.assertEqual(result, "special_pipe")

    def test_str(self):
        """ test EndPipe.__str__ """
        pipe = self.a2.EndPipe()
        result = str(pipe)
        self.assertEqual(result, "EndPipe(0)")

    def test_repr(self):
        """ test EndPipe.__repr__ """
        pipe = self.a2.EndPipe()
        result = repr(pipe)
        self.assertEqual(result, "EndPipe(0)")

    def test_get_orientation_default(self):
        """ test EndPipe.get_orientation defaults 0 """
        pipe = self.a2.EndPipe()
        result = pipe.get_orientation()
        self.assertEqual(result, 0)

    def test_get_orientation(self):
        """ test EndPipe.get_orientation __init__ set """
        pipe = self.a2.EndPipe(1)
        result = pipe.get_orientation()
        self.assertEqual(result, 1)

    def test_get_connected_0(self):
        """ test EndPipe.get_connected orientation 0 """
        pipe = self.a2.EndPipe()
        result = pipe.get_connected()
        self.assertEqual(result, ['S'])

    def test_get_connected_1(self):
        """ test EndPipe.get_connected orientation 1 """
        pipe = self.a2.EndPipe(1)
        result = pipe.get_connected()
        self.assertEqual(result, ['W'])


@skipIfFailed(TestDesign, TestDesign.test_classes_and_functions_defined.__name__, tag=PipeGame.__name__)
class TestPipeGame(TestA2):

    @skipIfFailed(TestTile, TestTile.test_repr.__name__)
    @skipIfFailed(TestPipe, TestPipe.test_repr.__name__)
    @skipIfFailed(TestStartPipe, TestStartPipe.test_repr.__name__)
    @skipIfFailed(TestEndPipe, TestEndPipe.test_repr.__name__)
    def test_get_board_layout(self):
        """ test PipeGame.get_board_layout default """
        game = self.a2.PipeGame()
        result = game.get_board_layout()
        expected = "[[Tile('tile', True), Tile('tile', True), Tile('tile', True), Tile('tile', True), Tile('tile', True), Tile('tile', True)], [StartPipe(1), Tile('tile', True), Tile('tile', True), Tile('tile', True), Tile('tile', True), Tile('tile', True)], [Tile('tile', True), Tile('tile', True), Tile('tile', True), Pipe('junction-t', 0), Tile('tile', True), Tile('tile', True)], [Tile('tile', True), Tile('tile', True), Tile('tile', True), Tile('tile', True), Tile('locked', False), Tile('tile', True)], [Tile('tile', True), Tile('tile', True), Tile('tile', True), Tile('tile', True), EndPipe(3), Tile('tile', True)], [Tile('tile', True), Tile('tile', True), Tile('tile', True), Tile('tile', True), Tile('tile', True), Tile('tile', True)]]"
        # repr is used for comparison because it allows for less implemented and easier to validate correctness
        self.assertEqual(repr(result), expected)

    def test_get_playable_pipes(self):
        """ test PipeGame.get_playable_pipes default """
        game = self.a2.PipeGame()
        result = game.get_playable_pipes()
        expected = {'straight': 1, 'corner': 1, 'cross': 1, 'junction-t': 1, 'diagonals': 1, 'over-under': 1}
        self.assertDictEqual(result, expected)

    @skipIfFailed(test_name=test_get_playable_pipes.__name__)
    def test_change_playable_amount_increase(self):
        """ test PipeGame.change_playable_amount increase """
        game = self.a2.PipeGame()
        ret = game.change_playable_amount('straight', 2)
        result = game.get_playable_pipes()
        expected = {'straight': 3, 'corner': 1, 'cross': 1, 'junction-t': 1, 'diagonals': 1, 'over-under': 1}
        self.assertDictEqual(result, expected)
        self.assertIsNone(ret, "PipeGame.change_playable_amount should not return")

    @skipIfFailed(test_name=test_get_playable_pipes.__name__)
    def test_change_playable_amount_decrease(self):
        """ test PipeGame.change_playable_amount decrease """
        game = self.a2.PipeGame()
        ret = game.change_playable_amount('straight', -1)
        result = game.get_playable_pipes()
        expected = {'straight': 0, 'corner': 1, 'cross': 1, 'junction-t': 1, 'diagonals': 1, 'over-under': 1}
        self.assertDictEqual(result, expected)
        self.assertIsNone(ret, "PipeGame.change_playable_amount should not return")

    @skipIfFailed(test_name=test_get_playable_pipes.__name__)
    def test_set_pipe_updates_playable_pipes(self):
        """ test PipeGame.set_pipe updates playable pipes """
        game = self.a2.PipeGame()
        straight = self.a2.Pipe('straight')
        ret = game.set_pipe(straight, (0, 0))
        result = game.get_playable_pipes()
        expected = {'straight': 0, 'corner': 1, 'cross': 1, 'junction-t': 1, 'diagonals': 1, 'over-under': 1}
        self.assertDictEqual(result, expected)
        self.assertIsNone(ret, "PipeGame.set_pipe should not return")

    def test_set_pipe_updates_board_layout(self):
        """ test PipeGame.set_pipe updates board layout """
        game = self.a2.PipeGame()
        straight = self.a2.Pipe('straight')
        ret = game.set_pipe(straight, (0, 0))
        result = game.get_board_layout()
        expected = "[[Pipe('straight', 0), Tile('tile', True), Tile('tile', True), Tile('tile', True), Tile('tile', True), Tile('tile', True)], [StartPipe(1), Tile('tile', True), Tile('tile', True), Tile('tile', True), Tile('tile', True), Tile('tile', True)], [Tile('tile', True), Tile('tile', True), Tile('tile', True), Pipe('junction-t', 0), Tile('tile', True), Tile('tile', True)], [Tile('tile', True), Tile('tile', True), Tile('tile', True), Tile('tile', True), Tile('locked', False), Tile('tile', True)], [Tile('tile', True), Tile('tile', True), Tile('tile', True), Tile('tile', True), EndPipe(3), Tile('tile', True)], [Tile('tile', True), Tile('tile', True), Tile('tile', True), Tile('tile', True), Tile('tile', True), Tile('tile', True)]]"
        self.assertEqual(repr(result), expected)
        self.assertIsNone(ret, "PipeGame.set_pipe should not return")

    @skipIfFailed(test_name=test_set_pipe_updates_playable_pipes.__name__)
    def test_remove_pipe_updates_playable_pipe(self):
        """ test PipeGame.remove_pipe updates board layout """
        game = self.a2.PipeGame()
        straight = self.a2.Pipe('straight')
        game.set_pipe(straight, (0, 0))
        ret = game.remove_pipe((0, 0))
        result = game.get_playable_pipes()
        expected = {'straight': 1, 'corner': 1, 'cross': 1, 'junction-t': 1, 'diagonals': 1, 'over-under': 1}
        self.assertDictEqual(result, expected)
        self.assertIsNone(ret, "PipeGame.remove_pipe should not return")

    @skipIfFailed(test_name=test_set_pipe_updates_board_layout.__name__)
    def test_remove_pipe_updates_board_layout(self):
        """ test PipeGame.remove_pipe updates board layout """
        game = self.a2.PipeGame()
        straight = self.a2.Pipe('straight')
        game.set_pipe(straight, (0, 0))
        ret = game.remove_pipe((0, 0))
        result = game.get_board_layout()
        expected = "[[Tile('tile', True), Tile('tile', True), Tile('tile', True), Tile('tile', True), Tile('tile', True), Tile('tile', True)], [StartPipe(1), Tile('tile', True), Tile('tile', True), Tile('tile', True), Tile('tile', True), Tile('tile', True)], [Tile('tile', True), Tile('tile', True), Tile('tile', True), Pipe('junction-t', 0), Tile('tile', True), Tile('tile', True)], [Tile('tile', True), Tile('tile', True), Tile('tile', True), Tile('tile', True), Tile('locked', False), Tile('tile', True)], [Tile('tile', True), Tile('tile', True), Tile('tile', True), Tile('tile', True), EndPipe(3), Tile('tile', True)], [Tile('tile', True), Tile('tile', True), Tile('tile', True), Tile('tile', True), Tile('tile', True), Tile('tile', True)]]"
        self.assertEqual(repr(result), expected)
        self.assertIsNone(ret, "PipeGame.set_pipe should not return")

    def test_position_in_direction_E_0_0(self):
        """ test PipeGame.position_in_direction E (0, 0) """
        game = self.a2.PipeGame()
        result = game.position_in_direction('E', (0, 0))
        self.assertEqual(result, ('W', (0, 1)))

    @skipIfFailed(test_name=test_position_in_direction_E_0_0.__name__)
    def test_position_in_direction_N_invalid(self):
        """ test PipeGame.position_in_direction N (0, 0) invalid  """
        game = self.a2.PipeGame()
        result = game.position_in_direction('N', (0, 0))
        self.assertIsNone(result)

    @skipIfFailed(test_name=test_position_in_direction_E_0_0.__name__)
    def test_pipe_in_position_empty(self):
        """ test PipeGame.pipe_in_position empty """
        game = self.a2.PipeGame()
        result = game.pipe_in_position((0, 0))
        self.assertIsNone(result)

    @skipIfFailed(test_name=test_set_pipe_updates_board_layout.__name__)
    def test_pipe_in_position(self):
        """ test PipeGame.pipe_in_position """
        game = self.a2.PipeGame()
        straight = self.a2.Pipe('straight')
        game.set_pipe(straight, (0, 0))
        result = game.pipe_in_position((0, 0))
        self.assertIs(result, straight)

    def test_get_starting_position(self):
        """ test PipeGame.get_starting_position """
        game = self.a2.PipeGame()
        result = game.get_starting_position()
        self.assertEqual(result, (1, 0))

    def test_get_ending_position(self):
        """ test PipeGame.get_ending_position """
        game = self.a2.PipeGame()
        result = game.get_ending_position()
        self.assertEqual(result, (4, 4))


def main():
    test_cases = [
        TestDesign,
        TestTile,
        TestPipe,
        TestSpecialPipe,
        TestStartPipe,
        TestEndPipe,
        TestPipeGame
    ]

    master = TestMaster(max_diff=None,
                        timeout=1,
                        include_no_print=True,
                        scripts=[
                            ('a2', 'a2.py')
                        ])
    master.run(test_cases)


if __name__ == '__main__':
    main()