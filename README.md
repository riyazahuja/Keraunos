# Keraunos

Keraunos is a cutting-edge drone swarm controller leveraging computer vision and artificial intelligence. This project utilizes Arduino for connectivity and YOLOv5 for advanced object detection and tracking, enabling sophisticated and parallelizable command decisions for swarms of 1-5 drones. Keraunos is designed for application in fields such as search and rescue and defense, featuring roles for leader and follower drones to maintain precise formation flying.

## Features

- **Real-time Object Detection**: Uses YOLOv5 for accurate and fast object detection, and employs the swarms' cameras for triangulation-based depth perception.
- **Drone Swarm Management**: Controls a swarm with distinct leader and follower roles and can fly in triangular, circular or linear formations.
- **Arduino Integration**: Ensures seamless communication with any WIFI-based drone hardware.
- **Versatile Applications**: Suitable for scenarios ranging from rescue operations to tactical deployments.

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/keraunos.git
   cd keraunos
   ```

2. Set Up the Python Environment:
    ```bash
    # Create a virtual environment
    python -m venv env
    # Activate the environment
    source env/bin/activate
    # Install dependencies
    pip install -r requirements.txt
    ```

## Arduino Setup:
Ensure that all related Arduino libraries are installed.
Please contact me at riyaza@andrew.cmu.edu for Arduino hardware schematics and details.

## Usage
To start the system, ensure that the drones are connected to the arduino hardware, and run the following commands from the root of the project directory:
- For follower drones:
    ```bash
    python deployment/follower.py
    ```
- For leader drones:
    ```bash
    python deployment/merge.py
    ```
- For direct PS4 control:
    ```bash
    python deployment/merge_ps4.py
    ```

## License
This project is licensed under the MIT License - see the LICENSE.md file for details.

## Acknowledgments
Thanks to the YOLOv5 team for providing the object detection model, and to the Arduino community for the extensive resources and libraries.

Additionally, thank you to the CMU Build18 team for organizing and hosting the event that sparked this idea, and special thanks to Arturo Paras, Jose Cestero, Kaloyan Stefanov, and Alexa Lowe for helping turn it into a reality!