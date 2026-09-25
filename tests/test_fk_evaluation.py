
import unittest

from open_rig_graph.entity import Entity
from open_rig_graph.evaluation import evaluate_world_transform
from open_rig_graph.transform import Transform


class TestFkEvaluation(unittest.TestCase):
    def test_root_world_transform_equals_local_transform(self):
        
        root_transform = Transform(
            translation=(10.0,0.0,0.0)
        )
        
        entities = {
            'root': Entity(
                id='root',
                parent_id=None,
                local_transform=root_transform
            )
        }
        
        result = evaluate_world_transform(
            entity_id='root',
            entities=entities
        )
        
        self.assertEqual(
            result,
            root_transform
        )
        
if __name__ == '__main__':
    unittest.main(verbosity=2)