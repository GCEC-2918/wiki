Driver-control multitasking in PROS
===================================

This is a guide to using the RTOS multi-tasking system in PROS for driver-control.

--

.. highlight:: c++

Let's start with a basic ``main.cpp`` skeleton::

    void initialize() {}

    void disabled() {}

    void autonomous() {}

    void opcontrol() {}

We won't be using ``competition_initialize() {}``, as this is just a basic template.

Let's create some tasks to run during ``opcontrol``::

    void chassis_drive (void* param){
        /* set your one-time variables here */

        while (true) {
            /* code that is repeated, like tank-drive, etc, goes here */

            pros::delay(20); // Don't forget to add a delay so that other tasks can be run!
        }
    }

    void initialize() {}

    void disabled() {}

    void autonomous() {}

    void opcontrol() {
        pros::Task chassis_control(chassis_drive);
    }

Great! Anything that you put inside the while loop will be run asynchronously to everything else. However, this means that the tasks you start in ``opcontrol`` do not stop when ``opcontrol`` does.

This has a roll-on effect that any code that runs in the loop continues to run, so if you are setting a motor's velocity to a joystick value, and then you want to change that motor's velocity in the ``autonomous`` function, you have to make sure that ``opcontrol`` is not called (by plugging it in to the competition switch before starting the program).

To fix this, we can use the ``pros::Task`` notification system. See `the PROS documentation <https://pros.cs.purdue.edu/v5/tutorials/topical/notifications.html>`_ for a run-down, especially that last code-snippet. By using a combination of atomic variables (see `here <https://cplusplus.com/reference/atomic/atomic/>`_) and task notifications, we can get a system that allows for both driver-control async tasks and procedural autonomous code::

    // an atomic variable allows other tasks (this includes opcontrol) to see the state of the task
    std::atomic<bool> chassis_drive_running = true;
    void chassis_drive (void* param){
        /* set your one-time variables here */

        // this variable and chassis_drive_running could be combined, but I like seperating them for readability
        bool should_run = true;

        while (true) {
            // this checks for 20ms if a notification is sent
            if (pros::Task::notify_take(true, 20)) {
                // if a notification was received, toggle the state of the task
                should_run = !should_run;
            }

            // set the atomic variable to the state of the task
            chassis_drive_running = should_run;

            if (should_run){  // if the task should run the code, run the code
                /* code that is repeated, like tank-drive, etc, goes here */
            }

            pros::delay(20); // Don't forget to add a delay so that other tasks can be run!
            // this means that there is 40ms of wait before the task is run again
        }
    }

    pros::Task chassis_control(chassis_drive);

    void initialize() {}

    void disabled() {
        // if the task is running, stop it
        // atomic variables cannot be directly read, the need to be loaded
        if (chassis_drive_running.load()) chassis_drive.notify();
    }

    void autonomous() {
        // if the task is running, stop it
        if (chassis_drive_running.load()) chassis_drive.notify();
    }

    void opcontrol() {
        // if the task isn't running, start it
        if (!chassis_drive_running.load()) chassis_drive.notify();
    }

This can be re-used for any number of tasks you want to use in ``opcontrol``.

**Written by Thomas Dickson [2918H]**
