# Modified version of the local VFX rendering server.
Because Conductor supports setting up custom scripts, reusing the script from the CeonVFX local rendering server.

Workflow:
Prepare the args as commands for conductor tasks

- Receive the render settings args (from the Ceonstock task)
- Build the tasks containing the 'command' which will be passed to the conductor API

- - The 'command' uses our custom run_render_hython script to handle setting output resolution.
