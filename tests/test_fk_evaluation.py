
import unittest

from open_rig_graph.entity import Entity
from open_rig_graph.evaluation import (
    evaluate_world_transform,
    evaluate_world_transforms,
)
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
        
    def test_fk_chain_accumulates_local_translations(self):
        
        entities = {
            'root': Entity(
                id='root',
                parent_id=None,
                local_transform=Transform(
                    translation=(10.0,0.0,0.0)
                )
            ),
            'mid': Entity(
                id='mid',
                parent_id='root',
                local_transform=Transform(
                    translation=(2.0,0.0,0.0)
                )
            ),
            'end': Entity(
                id='end',
                parent_id='mid',
                local_transform=Transform(
                    translation=(3.0,0.0,0.0)
                )
            ),
        }
        
        world_transforms = evaluate_world_transforms(
            entities=entities
        )
        
        self.assertEqual(
            world_transforms['root'].translation,
            (10.0,0.0,0.0)
        )
        
        self.assertEqual(
            world_transforms['mid'].translation,
            (12.0,0.0,0.0)
        )
        
        self.assertEqual(
            world_transforms['end'].translation,
            (15.0,0.0,0.0)
        )
        
if __name__ == '__main__':
    unittest.main(verbosity=2)