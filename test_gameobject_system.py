#!/usr/bin/env python3
"""
Test script for the new GameObject system.

This script tests the basic functionality of the GameObject system:
- Creating GameObjects
- Adding components
- Scene management
- Basic operations
"""

import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from core import GameObject, Scene, Component, TransformComponent
from core.components import MeshRenderer, Light, Camera, Collider
from utils.logger import get_logger

def test_gameobject_creation():
    """Test basic GameObject creation."""
    print("🧪 Testing GameObject creation...")
    
    # Create a GameObject
    cube = GameObject("Test Cube")
    print(f"✅ Created GameObject: {cube}")
    
    # Check default transform
    print(f"   Position: {cube.transform.position}")
    print(f"   Rotation: {cube.transform.rotation}")
    print(f"   Scale: {cube.transform.scale}")
    
    # Modify transform
    cube.transform.set_position(1.0, 2.0, 3.0)
    cube.transform.set_rotation(45.0, 90.0, 0.0)
    cube.transform.set_scale(2.0, 2.0, 2.0)
    
    print(f"   Modified Position: {cube.transform.position}")
    print(f"   Modified Rotation: {cube.transform.rotation}")
    print(f"   Modified Scale: {cube.transform.scale}")
    
    return cube

def test_component_system():
    """Test the component system."""
    print("\n🧪 Testing Component system...")
    
    # Create a GameObject
    obj = GameObject("Component Test Object")
    
    # Add components
    mesh_renderer = MeshRenderer()
    light = Light("point")
    camera = Camera()
    collider = Collider("box")
    
    obj.add_component(mesh_renderer)
    obj.add_component(light)
    obj.add_component(camera)
    obj.add_component(collider)
    
    print(f"✅ Added {len(obj.components)} components to {obj.name}")
    
    # Check components
    print(f"   Has MeshRenderer: {obj.has_component(MeshRenderer)}")
    print(f"   Has Light: {obj.has_component(Light)}")
    print(f"   Has Camera: {obj.has_component(Camera)}")
    print(f"   Has Collider: {obj.has_component(Collider)}")
    
    # Get specific component
    camera_comp = obj.get_component(Camera)
    if camera_comp:
        print(f"   Camera FOV: {camera_comp.fov}")
    
    return obj

def test_hierarchy():
    """Test GameObject hierarchy."""
    print("\n🧪 Testing GameObject hierarchy...")
    
    # Create parent
    parent = GameObject("Parent")
    parent.transform.set_position(0, 0, 0)
    
    # Create children
    child1 = GameObject("Child 1")
    child1.transform.set_position(1, 0, 0)
    
    child2 = GameObject("Child 2")
    child2.transform.set_position(-1, 0, 0)
    
    grandchild = GameObject("Grandchild")
    grandchild.transform.set_position(0, 1, 0)
    
    # Build hierarchy
    parent.add_child(child1)
    parent.add_child(child2)
    child1.add_child(grandchild)
    
    print(f"✅ Created hierarchy:")
    print(f"   Parent: {parent.name} ({len(parent.children)} children)")
    print(f"   Child 1: {child1.name} ({len(child1.children)} children)")
    print(f"   Child 2: {child2.name} ({len(child2.children)} children)")
    print(f"   Grandchild: {grandchild.name} (parent: {grandchild.parent.name})")
    
    # Test path
    print(f"   Grandchild path: {grandchild.get_path()}")
    
    return parent

def test_scene_management():
    """Test scene management."""
    print("\n🧪 Testing Scene management...")
    
    # Create scene
    scene = Scene("Test Scene")
    print(f"✅ Created scene: {scene.name}")
    
    # Create GameObjects
    cube = GameObject("Scene Cube")
    sphere = GameObject("Scene Sphere")
    light = GameObject("Scene Light")
    
    # Add components
    cube.add_component(MeshRenderer())
    cube.add_component(Collider("box"))
    
    sphere.add_component(MeshRenderer())
    sphere.add_component(Collider("sphere"))
    
    light.add_component(Light("point"))
    
    # Add to scene
    scene.add_object(cube)
    scene.add_object(sphere)
    scene.add_object(light)
    
    print(f"✅ Added {scene.get_object_count()} objects to scene")
    print(f"   Root objects: {len(scene.get_root_objects())}")
    
    # Test selection
    scene.select_object(cube)
    selected = scene.get_selected_objects()
    print(f"   Selected objects: {len(selected)}")
    if selected:
        print(f"   First selected: {selected[0].name}")
    
    # Test finding objects
    found_cube = scene.find_object("Scene Cube")
    if found_cube:
        print(f"   Found cube: {found_cube.name}")
    
    return scene

def test_serialization():
    """Test GameObject serialization."""
    print("\n🧪 Testing GameObject serialization...")
    
    # Create a GameObject with components
    obj = GameObject("Serialization Test")
    obj.transform.set_position(10, 20, 30)
    obj.transform.set_rotation(45, 90, 180)
    obj.transform.set_scale(2.5, 2.5, 2.5)
    
    obj.add_component(MeshRenderer("test_mesh.obj", "test_material.mat"))
    obj.add_component(Light("spot", [1.0, 0.5, 0.0], 2.0))
    
    # Serialize
    data = obj.serialize()
    print(f"✅ Serialized GameObject:")
    print(f"   Name: {data['name']}")
    print(f"   Position: {data['transform']['position']}")
    print(f"   Components: {len(data['components'])}")
    
    # Deserialize
    new_obj = GameObject.deserialize(data)
    print(f"✅ Deserialized GameObject:")
    print(f"   Name: {new_obj.name}")
    print(f"   Position: {new_obj.transform.position}")
    print(f"   Components: {len(new_obj.components)}")
    
    return obj

def main():
    """Run all tests."""
    print("🚀 Testing Nexlify GameObject System")
    print("=" * 50)
    
    try:
        # Run tests
        test_gameobject_creation()
        test_component_system()
        test_hierarchy()
        test_scene_management()
        test_serialization()
        
        print("\n" + "=" * 50)
        print("✅ All tests completed successfully!")
        print("🎉 GameObject system is working correctly!")
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
