# Fourier Robot Descriptions

## Usage

```python
from fourier_robot_descriptions.loaders.pinocchio import load_robot_description
robot = load_robot_description("GR1T2")
```

To directly get the URDF file path:

```python
from fourier_robot_descriptions.fourier_right_hand import URDF_PATH, PACKAGE_PATH
```

## Available Robots

| Name | Description |
|------|-------------|
| GR1T1 | GR1T1 with Fourier hand  |
| GR1T1_inspire_hand | GR1T1 with Inspire hand |
| GR1T1_jaw | GR1T1 with Gripper |
| GR1T2 | GR1T2 with Fourier hand  |
| GR1T2_inspire_hand | GR1T2 with Inspire hand |
| GR1T2_jaw | GR1T2 with Gripper |
| fourier_right_hand | Fourier right hand |
| fourier_left_hand | Fourier left hand | 