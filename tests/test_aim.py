
import unittest

from open_rig_graph.aim import compute_aim_rotation


class TestAim(unittest.TestCase):
    
    def test_identity_aim_returns_identity_rotation(self):
        
        rotation = compute_aim_rotation(
            source_position=(0.0,0.0,0.0),
            target_position=(1.0,0.0,0.0),
            up_direction=(0.0,1.0,0.0),
        )
        
        self.assertEqual(rotation, (0.0,0.0,0.0,1.0))
        
    def test_aiming_along_y_returns_expected_rotation(self):

        rotation = compute_aim_rotation(
            source_position=(0.0,0.0,0.0),
            target_position=(0.0,1.0,0.0),
            up_direction=(0.0,0.0,1.0),
        )
        
        expected = (0.5,0.5,0.5,0.5)
        
        for actual_value, expected_value in zip(rotation, expected):
            self.assertAlmostEqual(actual_value, expected_value)
            
    def test_coincident_positions_rase_value_error(self):
        
        with self.assertRaisesRegex(
            ValueError,
            'source position'
        ):
            compute_aim_rotation(
                source_position=(0.0,0.0,0.0),
                target_position=(0.0,0.0,0.0),
                up_direction=(0.0,1.0,0.0),
            )
            
    def test_parallel_up_direction_raises_value_error(self):
        
        with self.assertRaisesRegex(
            ValueError,
            'parallel'
        ):
            compute_aim_rotation(
                source_position=(0.0,0.0,0.0),
                target_position=(1.0,0.0,0.0),
                up_direction=(1.0,0.0,0.0),
            )
        
if __name__ == '__main__':
    
    unittest.main(verbosity=2)