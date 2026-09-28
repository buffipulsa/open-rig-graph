
import unittest

from open_rig_graph.transform import (
    compose_rotation,
    inverse_rotation,
    to_local_rotation,
)


class TestTransformRotation(unittest.TestCase):
    
    def test_rotation_compose_with_inverse_returns_identiy(self):
        
        rotation  = (0.5,0.5,0.5,0.5)
        
        result = compose_rotation(
            parent_rotation=rotation,
            local_rotation=inverse_rotation(
                rotation=rotation
            )
        )
        
        expected = (0.0,0.0,0.0,1.0)
        
        for actual_value, expected_value in zip(result, expected):
            self.assertAlmostEqual(actual_value, expected_value)
            
    def test_world_rotation_converts_back_to_local_rotation(self):
        
        parent_rotation = (0.5,0.5,0.5,0.5)
        local_rotation = (
            0.0,
            0.0,
            0.70710678118,
            0.70710678118,
        )
        
        world_rotation = compose_rotation(
            parent_rotation=parent_rotation,
            local_rotation=local_rotation
        )
        
        result = to_local_rotation(
            parent_rotation=parent_rotation,
            world_rotation=world_rotation
        )
        
        for actual_value, expected_value in zip(result, local_rotation):
            self.assertAlmostEqual(actual_value, expected_value)
            

if __name__ == '__main__':
    unittest.main(verbosity=2)