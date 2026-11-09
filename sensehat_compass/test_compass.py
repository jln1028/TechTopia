import unittest
from compass_core import cardinal, arrow_pixels, numeric_frames, compass_frame, next_mode

class CompassTests(unittest.TestCase):
    def test_cardinal_boundaries(self):
        cases = [(0,'N'),(22.49,'N'),(22.5,'NE'),(67.5,'E'),(112.5,'SE'),(157.5,'S'),(202.5,'SW'),(247.5,'W'),(292.5,'NW'),(337.5,'N'),(360,'N'),(-90,'W')]
        for angle, expected in cases:
            with self.subTest(angle=angle): self.assertEqual(cardinal(angle), expected)

    def test_arrow_points_north_for_zero(self):
        pixels = arrow_pixels(0)
        self.assertEqual(len(pixels),64)
        self.assertEqual(pixels[0*8+3], (255,0,0))
        self.assertEqual(pixels[3*8+3], (255,0,0))

    def test_arrow_points_east_for_ninety(self):
        pixels = arrow_pixels(90)
        self.assertEqual(pixels[3*8+7], (255,0,0))

    def test_numeric_frames(self):
        self.assertEqual(numeric_frames(0), ['000'])
        self.assertEqual(numeric_frames(359.6), ['000'])
        self.assertEqual(numeric_frames(91.4), ['091'])

    def test_frame_is_valid_rgb(self):
        for angle in range(0,360,15):
            for mode in ('arrow','cardinal','numeric'):
                frame=compass_frame(angle, mode)
                self.assertEqual(len(frame),64)
                self.assertTrue(all(len(c)==3 and all(0<=x<=255 for x in c) for c in frame))

    def test_joystick_mode_cycle(self):
        self.assertEqual(next_mode("arrow"), "cardinal")
        self.assertEqual(next_mode("cardinal"), "numeric")
        self.assertEqual(next_mode("numeric"), "arrow")
        self.assertEqual(next_mode("arrow", -1), "numeric")

    def test_invalid_mode(self):
        with self.assertRaises(ValueError): compass_frame(0,'other')

if __name__=='__main__': unittest.main()
