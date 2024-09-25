# SonarCTL Software

This is a software that communicates with a custom midi controller. The main purpose of this app is to allow you to
control your SteelSeries sonar slider with a midi controller.

### How to use

1. Make sure that you have a SonarCTL MIDI controller.
    - If you don't have one, you can build one by following the instructions in the [SonarCTL MIDI repository]()
2. Connect your SonarCTL MIDI controller to your computer.
3. Make sure you have 3.6 < Python < 3.12 installed on your computer.
4. Clone this repository.
5. Initialize the virtual environment by running:
    ```shell
    python -m venv venv
    ```
6. Activate the virtual environment:
    - Windows:
        ```shell
        .\venv\Scripts\Activate
        ```
    - Linux:
        ```shell
        source venv/bin/activate
        ```
7. Install the dependencies:
    ```shell
    pip install -r requirements.txt
    ```
8. Run the app:
    ```shell
   pythonw -m src.SonarlCTL
    ```
   
### Attribution
This uses [Mark788k's steelseries-sonar-py](https://github.com/Mark7888/steelseries-sonar-py) library to communicate with the SteelSeries Sonar.