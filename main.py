import numpy as np
import genesis as gs

gs.init(backend=gs.gpu)

scene = gs.Scene(
    viewer_options = gs.options.ViewerOptions(
        camera_pos    = (3, -1, 1.5),
        camera_lookat = (0.0, 0.0, 0.5),
        camera_fov    = 30,
        max_FPS       = 60,
    ),
    sim_options = gs.options.SimOptions(
        dt = 0.01,
    ),
    show_viewer = False,
    renderer = gs.renderers.Rasterizer(),
)

# plane
plane = scene.add_entity(
    gs.morphs.Plane(),
)

# soft deformable dough object
dough = scene.add_entity(
    material=gs.materials.MPM.ElastoPlastic(
        E=1e4,
        nu=0.3,
    ),
    morph=gs.morphs.Sphere(
        pos=(0.65, 0.0, 0.15),
        radius=0.1,
    ),
    surface=gs.surfaces.Default(
        color=(1.0, 1.0, 1.0),
        vis_mode='particle',
    ),
)

# robot arm
franka = scene.add_entity(
    gs.morphs.MJCF(file='xml/franka_emika_panda/panda.xml'),
)

# camera
cam = scene.add_camera(
    res=(320, 240),
    pos=(3.5, 0.0, 2.5),
    lookat=(0, 0, 0.5),
    fov=30,
    GUI=True,
)

scene.build()
cam.start_recording()

motors_dof = np.arange(7)
fingers_dof = np.arange(7, 9)

# Control - perfected
franka.set_dofs_kp(
    np.array([4500, 4500, 3500, 3500, 2000, 2000, 2000, 100, 100]),
)
franka.set_dofs_kv(
    np.array([450, 450, 350, 350, 200, 200, 200, 10, 10]),
)
franka.set_dofs_force_range(
    np.array([-87, -87, -87, -87, -12, -12, -12, -100, -100]),
    np.array([ 87,  87,  87,  87,  12,  12,  12,  100,  100]),
)

end_effector = franka.get_link('hand')

# pre-grasp position above dough
qpos_pre = franka.inverse_kinematics(
    link = end_effector,
    pos  = np.array([0.65, 0.0, 0.25]),
    quat = np.array([0, 1, 0, 0]),
)
qpos_pre[-2:] = 0.04

# OMPL path planning not working hence linear interpolation
current_qpos = franka.get_dofs_position()
num_steps = 200
for i in range(num_steps):
    t = (i + 1) / num_steps
    interp_qpos = (1 - t) * current_qpos + t * qpos_pre
    franka.control_dofs_position(interp_qpos)
    scene.step()
    if i % 2 == 0:
        cam.render()

for i in range(100):
    scene.step()
    if i % 2 == 0:
        cam.render()

# Move down to grasp dough
qpos = franka.inverse_kinematics(
    link = end_effector,
    pos  = np.array([0.65, 0.0, 0.130]),
    quat = np.array([0, 1, 0, 0]),
)
franka.control_dofs_position(qpos[:-2], motors_dof)
for i in range(100):
    scene.step()
    if i % 2 == 0:
        cam.render()

# Close gripper to grasp dough
franka.control_dofs_position(qpos[:-2], motors_dof)
franka.control_dofs_force(np.array([-0.5, -0.5]), fingers_dof)

for i in range(100):
    scene.step()
    if i % 2 == 0:
        cam.render()

# Lift dough up
qpos = franka.inverse_kinematics(
    link=end_effector,
    pos=np.array([0.65, 0.0, 0.28]),
    quat=np.array([0, 1, 0, 0]),
)
franka.control_dofs_position(qpos[:-2], motors_dof)
for i in range(200):
    scene.step()
    if i % 2 == 0:
        cam.render()