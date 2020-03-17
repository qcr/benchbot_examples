**NOTE: this software is part of the BenchBot Software Stack, and not intended to be run in isolation. For a working BenchBot system, please install the BenchBot Software Stack by following the instructions [here](https://github.com/RoboticVisionOrg/benchbot). In particular, all native commands shown below should be run through `benchbot_submit`.**


# BenchBot Examples

This package contains some simple examples to use with the [BenchBot Software Stack](https://github.com/RoboticVisionOrg/benchbot). The examples use the [BenchBot API](https://github.com/RoboticVisionOrg/benchbot_api) to control a simulated robot in a realistic 3D simulated environment.

All examples are contained in their own directory, & can be either run natively:

```bash
python hello_benchbot/hello_benchbot
```

```bash
./hello_benchbot/hello_benchbot
```

or inside a container using the provided Dockerfiles (useful if you don't want to have to change your system configuration):

```bash
cd hello_benchbot; docker build; docker run
```

## Examples list

### hello_benchbot

![benchbot_examples_hello](./docs/benchbot_examples_hello_web.gif)

Drives the robot forward 1m, rotates 180 degrees, drives back 1m, rotates 180 degrees, & repeats indefinitely. Includes visualisation of the robot's observations after each step.

### hello_passive

![benchbot_examples_passive](./docs/benchbot_examples_passive_web.gif)

Drives the robot through the entire pose trajectory provided by passive mode. Requires the software stack to be running a task where `control_mode = 'passive'`. Includes visualisation of the robot's observations after each step.

### hello_active

![benchbot_examples_active](./docs/benchbot_examples_active_web.gif)

Provides interactive control of the robot through a command line interface (e.g. `a 30` rotates 30 degrees, `d 0.5` drives forward 50cm). Requires the software stack to be running a task where `control_mode = 'active'`. Includes visualisation of the robot's observations after each step.

### hello_scd

Extension of the `hello_passive` example, but explicitly for running a task where `type = 'scd'` (Scene Change Detection). `hello_passive` will also work for Scene Change Detection tasks, although this example also shows how to the API can be used to determine which scene is currently running.

### hello_evaluate

Creates a basic agent which exits immediately & saves some dummy results based on the ground truth for `miniroom:1` (the example can be run against other environments but will obviously return poor evaluation results).

### aigym_semantic_slam

Demonstrates how to explicitly create an "OpenAI Gym" style control loop for tasks where `type = 'semantic_slam'` as opposed to simply calling the API's `run()` method. Shows how custom run loops could be created from core API functions.

### aigym_scd

Demonstrates how to explicitly create an "OpenAI Gym" style control loop for tasks where `type = 'scd'` as opposed to simply calling the API's `run()` method. Shows how custom run loops could be created from core API functions.

### semantic_slam_attempt

Wraps Facebook Research's [VoteNet](https://github.com/facebookresearch/votenet) 3D object detector, with an attempted solution created for tasks where `type = 'semantic_slam'` & `control_mode = 'passive'`. The included Dockerfile allows running without manually installing VoteNet (note: the compilation of CUDA layers has to be done **everytime** due to limitations in Docker's GPU support - running natively is recommended if possible). The top of the [BenchBot Software Stack's README](https://github.com/RoboticVisionOrg/benchbot) shows this example in action.
 
