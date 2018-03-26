## Homework 3: Gazebo and ROS Control
#### ME 495: Embedded Systems in Robotics
#### Kashish Goyal


## Introduction
The package demonstrates the usage of Gazebo simulation tool and its interfacing with ROS.

## Part 1: `rrbot` and ROS interfacing
1. ### The Gazebo world - [rrbot.world](https://github.com/ME495-EmbeddedSystems/homework-3-f2017-Kashugoyal/blob/starter/worlds/rrbot.world "rrbot.world")
   The world contains 4 models namely `House1`, `Pickup`, `Mailbox` and `Jersey Barrier`. 
2. ###  The launch file - [rrbot_world.launch](https://github.com/ME495-EmbeddedSystems/homework-3-f2017-Kashugoyal/blob/starter/launch/rrbot_world.launch "rrbot_world.launch")
   The launch file will launch the *Gazebo* simulator with the world file mentiond in the previous text and also spwan *rrbot* model. This can be seen in the following image. 

   <img src="https://github.com/ME495-EmbeddedSystems/homework-3-f2017-Kashugoyal/blob/starter/screenshots/Screenshot%20from%202017-11-11%2020-02-46.png?raw=true" width=700>
3. ### Viewing the camera image - rqt_image_view
   * To start the *rqt_image viewer*, we use the following command:
   ```
    $ rosrun rqt_image_view rqt_image_view
   ```
   > Make sure the correct topic is selected in the rqt window. It should be `/rrbot/camera1/image_raw`.
   * The view from the camera is:
   
     <img src="https://github.com/ME495-EmbeddedSystems/homework-3-f2017-Kashugoyal/blob/starter/screenshots/camera%20feed.png?raw=true" width=300>

   * The plugin responsible for simulating the camera is **camera_controller** and this can be seen in the file [rrbot.gazebo](https://github.com/ME495-EmbeddedSystems/homework-3-f2017-Kashugoyal/blob/starter/urdf/rrbot.gazebo) file [here](https://github.com/ME495-EmbeddedSystems/homework-3-f2017-Kashugoyal/blob/3db140e81411683e53f91cd17e0b44cf6a721afe/urdf/rrbot.gazebo#L99 "Camera Plugin").
   * The simulated image is published on `/rrbot/camera1/image_raw` topic and this is defined in the rrbot.gazebo file inside the plugin tag. This can be seen [here](https://github.com/ME495-EmbeddedSystems/homework-3-f2017-Kashugoyal/blob/3db140e81411683e53f91cd17e0b44cf6a721afe/urdf/rrbot.gazebo#L102-L103).
4. ### Launching *Rviz* along with *Gazebo*
   * The file, [**rrbot_rviz.launch**](https://github.com/ME495-EmbeddedSystems/homework-3-f2017-Kashugoyal/blob/starter/launch/rrbot_rviz.launch "rrbot_rviz.launch") launches *Rviz* with the specific configuration which is descibed in the file [rrbot.rviz](https://github.com/ME495-EmbeddedSystems/homework-3-f2017-Kashugoyal/blob/starter/launch/rrbot.rviz "rrbot.rviz"). Rviz is started with `LaserScan` and `Camera` modules.
   * To make the `laserscan` show up in *Rviz*, following steps need to be followed:
      * In the file [rrbot.gazebo](https://github.com/ME495-EmbeddedSystems/homework-3-f2017-Kashugoyal/blob/starter/urdf/rrbot.gazebo), make the following changes. 
      Replace: 
      `
      <sensor type="gpu_ray" name="head_hokuyo_sensor">` to ` <sensor type="ray" name="head_hokuyo_sensor">
      `
       as shown [here](https://github.com/ME495-EmbeddedSystems/homework-3-f2017-Kashugoyal/blob/3db140e81411683e53f91cd17e0b44cf6a721afe/urdf/rrbot.gazebo#L40), and replace
`<plugin name="gazebo_ros_head_hokuyo_controller" filename="libgazebo_ros_gpu_laser.so">` to `<plugin name="gazebo_ros_head_hokuyo_controller" filename="libgazebo_ros_laser.so">`. This can be seen [here](https://github.com/ME495-EmbeddedSystems/homework-3-f2017-Kashugoyal/blob/3db140e81411683e53f91cd17e0b44cf6a721afe/urdf/rrbot.gazebo#L68).
      * Also, set the `<visualise>` tag to `true` as [here](https://github.com/ME495-EmbeddedSystems/homework-3-f2017-Kashugoyal/blob/3db140e81411683e53f91cd17e0b44cf6a721afe/urdf/rrbot.gazebo#L42).

    * With a noise setting such that mean is 0.0 and standard deviation is 0.01, following is observed in the *Rviz*
      
         <img src="https://github.com/ME495-EmbeddedSystems/homework-3-f2017-Kashugoyal/blob/starter/screenshots/laser_scan1.png?raw=true" width=500 border=2>
    * With a noise setting such that mean is 0.0 but standard deviation is 5, following is observedin *Rviz*
      
         <img src="https://github.com/ME495-EmbeddedSystems/homework-3-f2017-Kashugoyal/blob/starter/screenshots/laser_scan2.png?raw=true" width=500 border=2>
        
         > It can be seen that with high value of standard deviation, it is tough to extract any significant results out of the data which is nothing but a collection of randome dots. 



## Part 2: ROS control, ROS communication, and custom plugins

1. ### *Gazebo_ROS_Control*
   * By default, the `gazebo_ros_control` plugin does not provide *joint state* information to ROS. The *YAML* file that configures the `joint_state_controller/JointStateController` to convert model *poses* to *joint_states* information is [here](https://github.com/ME495-EmbeddedSystems/homework-3-f2017-Kashugoyal/blob/starter/config/rrbot_control.yaml "rrbot_control.yaml").
   * To run this configuration, 
      a. Launch the [rrbot_world.launch](https://github.com/ME495-EmbeddedSystems/homework-3-f2017-Kashugoyal/blob/starter/launch/rrbot_world.launch "rrbot_world.launch") file.
      b. Launch the [rrbot_control.launch](https://github.com/ME495-EmbeddedSystems/homework-3-f2017-Kashugoyal/blob/starter/launch/rrbot_control.launch "rrbot_control.launch") file. This file starts the controller and also starts the *Rviz* node which listens to the `robot_state_publisher` to move the data in sync with *Gazebo*.
      > The launch file also takes an argument `jspub` which is by default set to false. To run the `Joint_State_publisher`, set this to true. *Rviz* will then listen to `Joint_State_Publisher* and not *Gazebo* for joint state information.

2. ### Swinging the Arm
    To swing the arm we use ` /gazebo/apply_joint_effort` service and call it using a custom python script. The procedure to run this is:
    
    * Launch the *Gazebo* world using [rrbot_world.launch](https://github.com/ME495-EmbeddedSystems/homework-3-f2017-Kashugoyal/blob/starter/launch/rrbot_world.launch "rrbot_world.launch") file if it is not already running.
    * Launch the [rrbot_control.launch](https://github.com/ME495-EmbeddedSystems/homework-3-f2017-Kashugoyal/blob/starter/launch/rrbot_control.launch "rrbot_control.launch") file.
    * Run the node [swing_arm.py](https://github.com/ME495-EmbeddedSystems/homework-3-f2017-Kashugoyal/blob/starter/src/swing_arm.py "Swing_arm.py"). This node uses the ` /gazebo/apply_joint_effort` service and applies torque to *joint1* for certian time and then withdraws it. This allows the arm to swing. The motion is not controlled however. The arm can be seen swinging in the *Gazebo* simulator and *Rviz*. 
3. ### RRBot custom plugin
    * To get the plugin running followng are the things to be done:
        * The plugin is to be compiled using `catkin_make`. The name of the plugin can be reconned from the *CMaklists.txt* file from [this line](https://github.com/ME495-EmbeddedSystems/homework-3-f2017-Kashugoyal/blob/baa8911fed1fe207f2365743494ca6b1ae604b38/CMakeLists.txt#L53).
        * Now the *rrbot.gazebo* file from the *rrbot_description* package has to be updated to add this plugin. The new file is [rrbot_plugin.gazebo](https://github.com/ME495-EmbeddedSystems/homework-3-f2017-Kashugoyal/blob/starter/urdf/rrbot_plugin.gazebo) and the changes made are [here](https://github.com/ME495-EmbeddedSystems/homework-3-f2017-Kashugoyal/blob/baa8911fed1fe207f2365743494ca6b1ae604b38/urdf/rrbot_plugin.gazebo#L11-L13).
    * The new launch file [rrbot_world_plugin.launch](https://github.com/ME495-EmbeddedSystems/homework-3-f2017-Kashugoyal/blob/starter/launch/rrbot_world_plugin.launch) is the upldated launch file that contains reference to the new [rrbot_plugin.gazebo](https://github.com/ME495-EmbeddedSystems/homework-3-f2017-Kashugoyal/blob/starter/urdf/rrbot_plugin.gazebo). The file also includes a call to run the [rrbot_control.launch](https://github.com/ME495-EmbeddedSystems/homework-3-f2017-Kashugoyal/blob/starter/launch/rrbot_control.launch "rrbot_control.launch") file. This elin=minates an additional step.
    * After launching file we inspect the list of topics using :
       ```
       $ rostopic list
       ```
        we see the following additional topic.
        ```
        /rrbot_joint_position_control/rrbot_ref_joint_config
        ```
        Inspecting the topic using the follwing commands, we get the message definition.
        
        ```
        $ rostopic type /rrbot_joint_position_control/rrbot_ref_joint_config |rosmsg show
        float32 j1
        float32 j2
        ```
4. ### Cyclic Trajectory
    To make the end effector follow a cyclic trajectory, we use a node very similar to the previous homework but with few changes. The node will now publish on the `/rrbot_joint_position_control/rrbot_ref_joint_config` topic with the new message definition. The node can be seen [here](https://github.com/ME495-EmbeddedSystems/homework-3-f2017-Kashugoyal/blob/starter/src/circle_swing.py "circle_swing.py"). To see this running, follow the steps:
    * Launch the [circle_swing.launch](https://github.com/ME495-EmbeddedSystems/homework-3-f2017-Kashugoyal/blob/starter/launch/circle_swing.launch "Circle_swing.launch") file. This file already includes the links different nodes needed. It does take the arguments such as `time` which controls the period of the loop, `rviz` which controls whether or not to start *Rviz* , etc. Both the *Rviz* and the *Gazebo* are launched from the same file. The arguments for the launch file are [here](https://github.com/ME495-EmbeddedSystems/homework-3-f2017-Kashugoyal/blob/baa8911fed1fe207f2365743494ca6b1ae604b38/launch/circle_swing.launch#L4-L12).

---
## Commit Description
Hashtag| Description
---|---
baa8911| Updated Readme.md
3db140e| Added the circle_swing node and launch file
9ce03c6 |Adde the plugin
13d90a3 |Added the node to swing the arm
436849e |Added laser scan screenshots
5afc09c |Added the models to world file
0ea8b15 |First run of the URDF in RVIZ
9deb319 |Added dep to CMakeLists and cleaned up plugin formatting
208e06d |Updated the API for Gazebo 7 on Kinetic
cd76198 |Just cleaning up whitespace
ee19f63 |Merge remote-tracking branch 'origin/starter' into starter
b98eea5 |Added README files
c52aad4 |Added README files
2b55a61 |Just adding some of the template code
6fe8662 |“root”






