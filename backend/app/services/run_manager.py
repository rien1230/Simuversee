# Manages the clock and notebook (start, stop, step and stop).
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, Optional, Literal
import time
import uuid
from backend.app.sim.model import SimModel
from backend.app.services.event_logger import EventLogger

# Status can only be these.
RunStatus = Literal["idle", "running", "paused", "stopped"]

@dataclass
class RunManager:

    # Owns:
    # - the clock (SimModel)
    # - the notebook (EventLogger) and provides the 4 buttons:
    # - start, pause, step, stop
    seed: int
    #generated run id if user doesn't give one makes a new random unique identifier.
    run_id: str = field(default_factory=lambda: uuid.uuid4().hex[:10])
    status: RunStatus = "idle"
    model: SimModel = field(init=False)
    logger: EventLogger = field(init=False)

    def __post_init__(self) -> None:
        # Creates the clock with seed used by user.
        self.model = SimModel(seed=self.seed)
        # Creates the notebook.
        self.logger = EventLogger(run_id=self.run_id)

    def start(self) -> None:
        #Doesn't allow restarting if user pressed stop.
        if self.status == "stopped":
            raise RuntimeError("Run is stopped. Create a new RunManager for a new run.")
        self.status = "running"

    def pause(self) -> None:
        # If stopped, pausing doesn't matter simulation ends.
        if self.status == "stopped":
            return
        self.status = "paused"

    def stop(self) -> None:
        self.status = "stopped"

    def step(self) -> Dict[str, Any]:
        # Can't progress as simulation ends.
        if self.status == "stopped":
            raise RuntimeError("Run is stopped. Create a new RunManager for a new run.")
        # Asks clock to advance to [tick+1] tick and return diff tick
        diff = self.model.step()
        # Writes to diff tick and returns to replay file as one JSON line.
        self.logger.log(diff)
        return diff
 # Optional for users
 # Only stops and pauses when user clicks stop or pause button so can run a certain amount of tick or run at a controlled amount of time.
    def run_loop(self, max_steps: Optional[int] = None, tick_hz: Optional[float] = None) -> None:

        if self.status != "running":
            raise RuntimeError("Call start() before run_loop().")

        steps_done = 0
        sleep_s = (1.0 / tick_hz) if (tick_hz and tick_hz > 0) else 0.0

        while self.status == "running":
            self.step()
            steps_done += 1

            if max_steps is not None and steps_done >= max_steps:
                # Auto-pause after N ticks (useful for debugging)
                self.pause()
                break

            if sleep_s > 0:
                time.sleep(sleep_s)
