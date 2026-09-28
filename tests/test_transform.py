
import unittest

from open_rig_graph.transform import compose_rotation, inverse_rotation

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
            

if __name__ == '__main__':
    unittest.main(verbosity=2)