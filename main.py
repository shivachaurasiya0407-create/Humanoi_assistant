import asyncio
import logging
import signal
import sys
from core.system_manager import manager
from core.event_bus import bus
from core.state_manager import state
from api.server import start_api_server

# Create logs directory if it doesn't exist before logging setup
import os
if not os.path.exists("logs"):
    os.makedirs("logs")

# Configure root logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("logs/system.log")
    ]
)
logger = logging.getLogger("Main")

async def shutdown(sig, loop):
    """Cleanup tasks on shutdown."""
    logger.info(f"Received exit signal {sig.name}...")
    await manager.stop()
    
    tasks = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]
    [t.cancel() for t in tasks]
    
    logger.info(f"Cancelling {len(tasks)} outstanding tasks")
    await asyncio.gather(*tasks, return_exceptions=True)
    loop.stop()

def handle_exception(loop, context):
    msg = context.get("exception", context["message"])
    logger.error(f"Caught exception: {msg}")
    asyncio.create_task(bus.emit("system_error", {"error": str(msg)}))

async def main():
    """Main System Entry Point."""
    loop = asyncio.get_running_loop()
    
    # Note: loop.add_signal_handler is NOT supported on Windows
    # We will use a try-finally block and handle KeyboardInterrupt at the entry point instead.
    
    loop.set_exception_handler(handle_exception)

    try:
        # 1. Initialize Core State & Pipeline
        from core.ai_runtime_state import runtime_state
        from core.live_event_pipeline import pipeline
        from core.performance_manager import performance_manager
        from core.recovery_manager import RecoveryManager
        
        # 2. Initialize Intelligence Layer
        from core.ai_brain import ai_brain
        from core.intent_analyzer import intent_analyzer
        from core.workflow_orchestrator import workflow_orchestrator
        from core.failsafe_manager import failsafe_manager
        
        # 3. Initialize Humanoid Layer
        from core.digital_body_state import body_state
        from core.human_awareness_engine import human_awareness
        from core.continuous_observer import observer
        from core.proactive_assistant import assistant
        
        # 4. Initialize Ecosystem & Evolution Layer
        from core.self_optimization_engine import optimization_engine
        from core.evolution_engine import evolution_engine
        from ecosystem.device_manager import device_manager
        from core.self_repair_engine import self_repair
        
        # 5. Initialize Autonomous Entity Layer
        from core.consciousness_state import mind_state
        from core.communication_hub import comm_hub
        from core.multi_agent_orchestrator import orchestrator
        from core.goal_engine import goal_engine
        
        # 6. Initialize Platform Layer
        from ai_platform.platform_core import platform_core
        from ai_platform.api_gateway import gateway
        from monitoring.platform_monitor import platform_monitor
        
        # 7. Initialize Universal Ecosystem Layer
        from network.universal_message_bus import universal_bus
        from universal.universal_ai_core import universal_core
        from universal.distributed_consciousness_engine import distributed_consciousness
        from universal.universal_orchestrator import universal_orchestrator
        
        # 8. Initialize AGI Research Layer (FINAL)
        from agi.cognitive_reasoning_engine import reasoning_engine
        from agi.world_understanding_model import world_model
        from agi.meta_learning_engine import meta_learning
        
        recovery_manager = RecoveryManager(manager)
        
        # 9. Start Background Simulators & Observers
        asyncio.create_task(body_state.start_sim())
        asyncio.create_task(observer.start())
        asyncio.create_task(human_awareness.run_loop())
        asyncio.create_task(optimization_engine.run_optimization_loop())
        asyncio.create_task(platform_monitor.start())
        await platform_core.initialize()
        await universal_core.synchronize_global_state()
        
        # 10. Start Performance & Recovery Managers
        await performance_manager.start()
        await recovery_manager.start()
        
        # 3. Initialize System Manager
        await manager.initialize()
        
        # 4. Start all modules
        await manager.start()
        
        # 5. Start API & WebSocket Server
        logger.info("🚀 Starting API and WebSocket server...")
        await start_api_server()
        
    except (asyncio.CancelledError, KeyboardInterrupt):
        logger.info("Shutdown signal received...")
    except Exception as e:
        logger.error(f"Critical System Failure: {e}")
    finally:
        # Graceful shutdown of all modules
        await manager.stop()
        logger.info("System shutdown complete.")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
