
import unittest

from open_rig_graph.aim import (
    apply_aim_rotation,
    compute_aim_rotation,
    evaluate_aim_constraints,
)
from open_rig_graph.constraints import AimConstraint
from open_rig_graph.transform import Transform


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
            
    def test_apply_aim_rotation_preserves_translation_and_scale(self):
        
        transform = Transform(
            translation=(2.0,3.0,4.0),
            scale=(2.0,3.0,4.0)
        )
        
        result = apply_aim_rotation(
            transform=transform,
            target_position=(2.0,4.0,4.0),
            up_direction=(0.0,0.0,1.0)
        )
        
        self.assertEqual(result.translation, transform.translation)
        self.assertEqual(result.scale, transform.scale)
        self.assertNotEqual(result.rotation, transform.rotation)

    def test_evaluate_aim_constraint_returns_constrained_world_transform(self):
        
        world_transforms = {
            'driven': Transform(
                translation=(2.0,3.0,4.0),
                scale=(2.0,3.0,4.0)
            ),
            'target': Transform(
                translation=(2.0,4.0,4.0)
            )
        }

        constraint = AimConstraint(
            driven_id='driven',
            target_id='target',
            up_direction=(0.0,0.0,1.0)
        )
        
        result = evaluate_aim_constraints(
            constraint=constraint,
            world_transforms=world_transforms
        )
        
        self.assertEqual(result.translation, (2.0,3.0,4.0))
        self.assertEqual(result.scale, (2.0,3.0,4.0))
        
        expected_rotation = (0.5,0.5,0.5,0.5)
        
        for actual_value, expected_value in zip(
            result.rotation,
            expected_rotation
        ):
            self.assertAlmostEqual(
                actual_value, expected_value
            )
            
    def test_missing_driven_entity_raises_key_error(self):
        
        constraint = AimConstraint(
            driven_id='missing',
            target_id='target'
        )
        
        world_transforms = {
            'target': Transform(
                translation=(1.0,0.0,0.0)
            )
        }
        
        with self.assertRaisesRegex(
            KeyError,
            "Unknown driven entity"
        ):
            evaluate_aim_constraints(
                constraint=constraint,
                world_transforms=world_transforms
            )
            
    def test_missing_target_entity_raises_key_error(self):
        
        constraint = AimConstraint(
            driven_id='driven',
            target_id='missing'
        )
        
        world_transforms = {
            'driven': Transform()
        }
        
        with self.assertRaisesRegex(
            KeyError,
            "Unknown target entity"
        ):
            evaluate_aim_constraints(
                constraint=constraint,
                world_transforms=world_transforms
            )

        
if __name__ == '__main__':
    
    unittest.main(verbosity=2)