# SonarCTL Software

This software allows you to control your SteelSeries Sonar slider with a custom MIDI controller.

Config View                       |  Console View                     |  Slider Preview View
:--------------------------------:|:---------------------------------:|:--------------------------------:
![](docs/images/ConfigView.png)   |  ![](docs/images/ConsoleView.png) | ![](docs/images/SliderView.png)

## Hardware requirement

To use this software, you must build your own SonarCTL MIDI controller. The materials needed and the steps can be found in this repository: [SonarCTL Firmware](https://github.com/CyR1en/SonarCTL-Firmware).

## Run from source

You can run this software directly from the source. You can do this by following steps:

1. **Install Python**:
    - Ensure you have Python version between 3.6 and 3.12 installed on your computer.

2. **Clone this repository**:
    ```
    git clone https://github.com/CyR1en/SonarCTL.git
    cd SonarCTL
    ```

3. **Initialize the virtual environment**:
    ```
    python -m venv venv
    ```

4. **Activate the virtual environment**:
    - **Windows**:
        ```
        .\venv\Scripts\Activate
        ```
    - **Linux**:
        ```
        source venv/bin/activate
        ```

5. **Install the dependencies**:
    ```
    pip install -r requirements.txt
    ```

6. **Run the app**:
    ```
    pythonw -m src.SonarCTL
    ```

## Build and Install

If you do not want to run the program from the source, you can download the installer from the [release section](https://github.com/CyR1en/SonarCTL/releases). 
If you want to build it yourself, the steps are:

1. **Make a virtual environment**:
    ```
    python -m venv venv
    ```

2. **Install dependencies from `requirements.txt`**:
    ```shell
    pip install -r requirements.txt
    ```

3. **Build the application using PyInstaller**:
    ```shell
    pyinstaller --noconfirm sonarctl.spec
    ```

4. **Install InstallForge, open the `.ifp` file, and click build**.

## Attribution

This software uses [Mark788k's steelseries-sonar-py](https://github.com/Mark7888/steelseries-sonar-py) library to communicate with the SteelSeries Sonar.
This software allows you to control your SteelSeries Sonar slider with a custom MIDI controller.
