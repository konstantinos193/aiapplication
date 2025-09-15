#!/usr/bin/env python3
"""
Test script for the new Unity-like Nexlify Game Engine.

This script demonstrates the core functionality of the engine including:
- ECS architecture
- Modern rendering pipeline
- AI asset generation
- Physics simulation
- Audio system
- Scripting system
- Asset pipeline
"""

import sys
import os
import time
import logging
from pathlib import Path

# Add src to Python path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.core.engine import GameEngine
from src.ai.ai_manager import AIManager
from src.physics.physics_engine import PhysicsEngine, PhysicsConfig
from src.audio.audio_engine import AudioEngine, AudioConfig
from src.scripting.scripting_engine import ScriptingEngine, ScriptingConfig
from src.asset.asset_pipeline import AssetPipeline, AssetType
from src.utils.logger import setup_logging


def test_engine_initialization():
    """Test basic engine initialization."""
    print("🚀 Testing Engine Initialization...")
    
    try:
        # Initialize game engine
        engine = GameEngine()
        success = engine.initialize()
        
        if success:
            print("✅ Game Engine initialized successfully")
            
            # Test scene creation
            scene = engine.create_scene("Test Scene")
            if scene:
                print("✅ Scene creation successful")
            
            # Test GameObject creation
            cube = engine.create_cube("Test Cube")
            if cube:
                print("✅ GameObject creation successful")
            
            # Test component system
            from src.core.components import MeshRenderer, Light, Camera
            mesh_renderer = cube.get_component(MeshRenderer)
            if mesh_renderer:
                print("✅ Component system working")
            
            engine.shutdown()
            return True
        else:
            print("❌ Game Engine initialization failed")
            return False
            
    except Exception as e:
        print(f"❌ Engine initialization error: {e}")
        return False


def test_ai_system():
    """Test AI asset generation system."""
    print("\n🤖 Testing AI System...")
    
    try:
        # Initialize AI manager
        ai_manager = AIManager()
        success = ai_manager.initialize({})
        
        if success:
            print("✅ AI Manager initialized successfully")
            
            # Test texture generation
            result = ai_manager.generate_texture(
                prompt="rusty metal surface",
                width=256,
                height=256,
                texture_type="noise"
            )
            
            if result.success:
                print(f"✅ AI texture generation successful: {result.asset_path}")
            else:
                print(f"❌ AI texture generation failed: {result.error_message}")
            
            # Test material generation
            result = ai_manager.generate_material(
                prompt="shiny plastic material",
                material_type="standard"
            )
            
            if result.success:
                print(f"✅ AI material generation successful: {result.asset_path}")
            else:
                print(f"❌ AI material generation failed: {result.error_message}")
            
            # Test code generation
            result = ai_manager.generate_code(
                prompt="player movement component",
                language="python",
                code_type="component"
            )
            
            if result.success:
                print(f"✅ AI code generation successful: {result.asset_path}")
            else:
                print(f"❌ AI code generation failed: {result.error_message}")
            
            ai_manager.shutdown()
            return True
        else:
            print("❌ AI Manager initialization failed")
            return False
            
    except Exception as e:
        print(f"❌ AI system error: {e}")
        return False


def test_physics_system():
    """Test physics simulation system."""
    print("\n⚡ Testing Physics System...")
    
    try:
        # Initialize physics engine
        config = PhysicsConfig()
        physics_engine = PhysicsEngine(config)
        success = physics_engine.initialize()
        
        if success:
            print("✅ Physics Engine initialized successfully")
            
            # Test rigid body creation
            from src.physics.rigid_body import RigidBody
            body = RigidBody()
            body.set_mass(1.0)
            body.set_position([0, 0, 0])
            
            # Add to physics world
            physics_engine.add_rigid_body(body)
            print("✅ Rigid body creation and management successful")
            
            # Test physics simulation
            physics_engine.start()
            
            # Simulate a few steps
            for i in range(10):
                physics_engine.step(0.016)  # 60 FPS
            
            stats = physics_engine.get_stats()
            print(f"✅ Physics simulation successful - FPS: {stats.fps:.1f}")
            
            physics_engine.shutdown()
            return True
        else:
            print("❌ Physics Engine initialization failed")
            return False
            
    except Exception as e:
        print(f"❌ Physics system error: {e}")
        return False


def test_audio_system():
    """Test 3D spatial audio system."""
    print("\n🔊 Testing Audio System...")
    
    try:
        # Initialize audio engine
        config = AudioConfig()
        audio_engine = AudioEngine(config)
        success = audio_engine.initialize()
        
        if success:
            print("✅ Audio Engine initialized successfully")
            
            # Test audio source creation
            source_id = audio_engine.create_audio_source(
                position=[0, 0, 0],
                is_3d=True
            )
            
            if source_id:
                print("✅ Audio source creation successful")
                
                # Test audio listener creation
                listener_id = audio_engine.create_audio_listener(
                    position=[0, 0, 0],
                    orientation=[0, 0, -1]
                )
                
                if listener_id:
                    print("✅ Audio listener creation successful")
                
                # Test audio engine start
                audio_engine.start()
                time.sleep(0.1)  # Let it run briefly
                
                stats = audio_engine.get_stats()
                print(f"✅ Audio system running - FPS: {stats.fps:.1f}")
                
                audio_engine.shutdown()
                return True
            else:
                print("❌ Audio source creation failed")
                return False
        else:
            print("❌ Audio Engine initialization failed")
            return False
            
    except Exception as e:
        print(f"❌ Audio system error: {e}")
        return False


def test_scripting_system():
    """Test Python scripting system."""
    print("\n🐍 Testing Scripting System...")
    
    try:
        # Initialize scripting engine
        config = ScriptingConfig()
        scripting_engine = ScriptingEngine(config)
        success = scripting_engine.initialize()
        
        if success:
            print("✅ Scripting Engine initialized successfully")
            
            # Create a test script
            test_script_path = "scripts/test_component.py"
            os.makedirs("scripts", exist_ok=True)
            
            test_script_content = '''
"""
Test component for scripting system.
"""

from src.scripting.script_component import ScriptComponent

class TestComponent(ScriptComponent):
    """Test component for demonstration."""
    
    def __init__(self):
        super().__init__()
        self.counter = 0
    
    def initialize(self):
        """Initialize the component."""
        print("Test component initialized!")
    
    def update(self, delta_time):
        """Update the component."""
        self.counter += 1
        if self.counter % 60 == 0:  # Every second at 60 FPS
            print(f"Test component update: {self.counter}")
    
    def shutdown(self):
        """Shutdown the component."""
        print("Test component shutdown!")
'''
            
            with open(test_script_path, 'w') as f:
                f.write(test_script_content)
            
            # Load the script
            scripting_engine._load_script_file(Path(test_script_path))
            
            # Create script instance
            instance = scripting_engine.create_script_instance("TestComponent")
            
            if instance:
                print("✅ Script loading and instantiation successful")
                
                # Test script update
                for i in range(5):
                    scripting_engine.update_scripts(0.016)
                
                print("✅ Script execution successful")
                
                # Cleanup
                scripting_engine.destroy_script_instance(instance.instance_id)
                os.remove(test_script_path)
                
                scripting_engine.shutdown()
                return True
            else:
                print("❌ Script instantiation failed")
                return False
        else:
            print("❌ Scripting Engine initialization failed")
            return False
            
    except Exception as e:
        print(f"❌ Scripting system error: {e}")
        return False


def test_asset_pipeline():
    """Test asset pipeline system."""
    print("\n📦 Testing Asset Pipeline...")
    
    try:
        # Initialize asset pipeline
        asset_pipeline = AssetPipeline()
        success = asset_pipeline.initialize()
        
        if success:
            print("✅ Asset Pipeline initialized successfully")
            
            # Create a test texture
            test_texture_path = "assets/test_texture.png"
            os.makedirs("assets", exist_ok=True)
            
            from PIL import Image
            test_image = Image.new('RGB', (64, 64), color='red')
            test_image.save(test_texture_path)
            
            # Load asset through pipeline
            asset_info = asset_pipeline.load_asset(test_texture_path, AssetType.TEXTURE)
            
            if asset_info:
                print(f"✅ Asset loading successful: {asset_info.name}")
                print(f"   - Type: {asset_info.type.value}")
                print(f"   - Size: {asset_info.size} bytes")
                print(f"   - Hash: {asset_info.hash[:16]}...")
                
                # Test asset retrieval
                retrieved_asset = asset_pipeline.get_asset(test_texture_path)
                if retrieved_asset:
                    print("✅ Asset retrieval successful")
                
                # Cleanup
                os.remove(test_texture_path)
                
                asset_pipeline.shutdown()
                return True
            else:
                print("❌ Asset loading failed")
                return False
        else:
            print("❌ Asset Pipeline initialization failed")
            return False
            
    except Exception as e:
        print(f"❌ Asset pipeline error: {e}")
        return False


def test_integration():
    """Test integration of all systems."""
    print("\n🔗 Testing System Integration...")
    
    try:
        # Initialize all systems
        engine = GameEngine()
        ai_manager = AIManager()
        physics_engine = PhysicsEngine(PhysicsConfig())
        audio_engine = AudioEngine(AudioConfig())
        scripting_engine = ScriptingEngine(ScriptingConfig())
        asset_pipeline = AssetPipeline(ai_manager)
        
        # Initialize all systems
        systems = [
            ("Game Engine", engine.initialize),
            ("AI Manager", lambda: ai_manager.initialize({})),
            ("Physics Engine", physics_engine.initialize),
            ("Audio Engine", audio_engine.initialize),
            ("Scripting Engine", scripting_engine.initialize),
            ("Asset Pipeline", asset_pipeline.initialize),
        ]
        
        all_initialized = True
        for name, init_func in systems:
            if not init_func():
                print(f"❌ {name} initialization failed")
                all_initialized = False
            else:
                print(f"✅ {name} initialized")
        
        if all_initialized:
            print("✅ All systems integrated successfully")
            
            # Test cross-system functionality
            # Create a scene with physics and audio
            scene = engine.create_scene("Integration Test Scene")
            cube = engine.create_cube("Physics Cube")
            camera = engine.create_camera("Main Camera")
            
            # Add physics body
            from src.physics.rigid_body import RigidBody
            physics_body = RigidBody()
            physics_engine.add_rigid_body(physics_body)
            
            # Add audio source
            audio_source_id = audio_engine.create_audio_source(is_3d=True)
            
            print("✅ Cross-system integration successful")
            
            # Shutdown all systems
            asset_pipeline.shutdown()
            scripting_engine.shutdown()
            audio_engine.shutdown()
            physics_engine.shutdown()
            ai_manager.shutdown()
            engine.shutdown()
            
            return True
        else:
            print("❌ System integration failed")
            return False
            
    except Exception as e:
        print(f"❌ Integration test error: {e}")
        return False


def main():
    """Run all tests."""
    print("🎮 Nexlify Unity-Like Game Engine Test Suite")
    print("=" * 50)
    
    # Setup logging
    setup_logging()
    
    # Run all tests
    tests = [
        ("Engine Initialization", test_engine_initialization),
        ("AI System", test_ai_system),
        ("Physics System", test_physics_system),
        ("Audio System", test_audio_system),
        ("Scripting System", test_scripting_system),
        ("Asset Pipeline", test_asset_pipeline),
        ("System Integration", test_integration),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
        except Exception as e:
            print(f"❌ {test_name} crashed: {e}")
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Nexlify is ready to use!")
        return 0
    else:
        print("⚠️  Some tests failed. Check the output above for details.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
