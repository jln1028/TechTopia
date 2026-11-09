import unittest
from types import SimpleNamespace
from controls import Controls

def event(direction, action='pressed'):
    return SimpleNamespace(direction=direction, action=action)

class ControlTests(unittest.TestCase):
    def test_joystick_direction(self):
        c = Controls()
        for name, expected in [('up',(0,-1)),('down',(0,1)),('left',(-1,0)),('right',(1,0))]:
            self.assertEqual(c.process_events([event(name)]), (expected, False))

    def test_ignore_release_and_held(self):
        c = Controls()
        self.assertEqual(c.process_events([event('up','released'), event('left','held')]), (None,False))

    def test_center_toggles_and_suppresses_movement(self):
        c = Controls()
        self.assertEqual(c.process_events([event('right'),event('middle')]), (None,True))
        self.assertEqual(c.mode, 'tilt')
        self.assertEqual(c.process_events([event('left')]), (None,False))
        self.assertEqual(c.process_events([event('middle')]), (None,True))
        self.assertEqual(c.mode, 'joystick')

    def test_tilt_only_when_selected(self):
        c = Controls()
        self.assertIsNone(c.tilt_move({'x':0.8,'y':0.1}))
        c.process_events([event('middle')])
        self.assertEqual(c.tilt_move({'x':0.8,'y':0.1}), (-1,0))
        self.assertIsNone(c.tilt_move({'x':0.1,'y':0.1}))

if __name__ == '__main__':
    unittest.main()
