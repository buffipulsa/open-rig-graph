
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
        
    def test_parent_rotation_rotates_child_translation(self):
        
        quarter_turn_z = (
            0.0,
            0.0,
            0.70710678118,
            0.70710678118,
        )
        
        entities = {
            'root': Entity(
                id='root',
                parent_id=None,
                local_transform=Transform(
                    rotation=quarter_turn_z
                )
            ),
            'mid': Entity(
                id='mid',
                parent_id='root',
                local_transform=Transform(
                    translation=(2.0,0.0,0.0)
                )
            )
        }
        
        world_transform = evaluate_world_transform(
            entity_id='mid',
            entities=entities
        )
        
        self.assertAlmostEqual(
            world_transform.translation[0], 0.0
        )
        self.assertAlmostEqual(
            world_transform.translation[1], 2.0
        )
        self.assertAlmostEqual(
            world_transform.translation[2], 0.0
        )
        
    def test_parent_scale_affects_child_translation_and_scale(self):
        
        entities = {
            'root': Entity(
                id='root',
                parent_id=None,
                local_transform=Transform(
                    scale=(2.0,3.0,1.0)
                )
            ),
            'mid': Entity(
                id='mid',
                parent_id='root',
                local_transform=Transform(
                    translation=(1.0,1.0,1.0)
                )
            )
        }
        
        world_transform = evaluate_world_transform(
            entity_id='mid',
            entities=entities
        )
        
        self.assertEqual(
            world_transform.translation,
            (2.0,3.0,1.0)
        )
        self.assertEqual(
            world_transform.scale,
            (2.0,3.0,1.0)
        )
        
    def test_hierarchy_cycle_raises_value_error(self):
        
        cyclic_entities = {
            'root': Entity(
                id='root',
                parent_id='end',
                local_transform=Transform()
            ),
            'mid': Entity(
                id='mid',
                parent_id='root',
                local_transform=Transform()
            ),
            'end': Entity(
                id='end',
                parent_id='mid',
                local_transform=Transform()
            )
        }
        
        with self.assertRaisesRegex(
            ValueError,
            'Hierarchy cycle detected'
        ):
            evaluate_world_transform(
                entity_id='end', 
                entities=cyclic_entities
            )
            
    def test_missing_parent_raises_key_error(self):
        
        entities = {
            'end': Entity(
                id='end',
                parent_id='missing',
                local_transform=Transform()
            )
        }
        
        with self.assertRaisesRegex(
            KeyError,
            'references missing parent'
        ):
            evaluate_world_transform(
                entity_id='end',
                entities=entities
            )

        
if __name__ == '__main__':
    unittest.main(verbosity=2)