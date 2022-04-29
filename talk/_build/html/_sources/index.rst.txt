
Creating Software Tools
=======================
One software development practice that I would like to encourage, particularly in researchers, is the
creation of software *tools*, not just *scripts*. In my experience, this is something that researchers
need special encouragement to do because their work may not be as team focused as, for example, work in
industry, and researchers may not have programming as their primary expertise. Nonetheless, I think
researchers have a lot to gain from just a few tweaks to their software development practices.

Before we get in too deep, let me explain what I mean by developing tools as apposed to scripts. I want to focus
particularly on *application* software, i.e. software that is executed by a user in order to accomplish a certain task.
I would call an application a *tool* if it is designed to be reusable. That is, it can be used to solve any iteration
of the particular task it is designed for. A *script* on the other hand may be a single file program that is hard-coded
to solve the developer's specific use case. It may have hard-coded parameters, operate on implicit assumptions about
the input data, and have a specific rigid operation flow. There is obviously considerable work required in elevating
an application from a script to a tool, but I hope to explain how significant steps can be made down this path with just
a little effort.

Let's first look at a few reasons why it might be worthwhile doing the work to convert your script into a fully fledged
software tool. The most obvious reason to me is to increase the impact of the work you've already done. When you write
a script, you devote time and effort into solving a problem. Making that code reusable means more overall benefit can
be derived from that precious time and effort. It also means that those who use it can spend their time on accomplishing
more, rather than continuously reinventing the wheel. Among many other benefits you will find that spending time working
to improve your code in this way will help demonstrate the significance of the problem it solves, and will greatly
assist in maintaining *data provenance* when doing complex research.

Without further ado, let's dive into how to actually go about converting a software script into a reusable tool. In
this article we'll be covering four main areas where with minimal effort you can go a long way to improving the
reusability of your code. These areas are:

- Sharing
- Configuration
- Testing
- Documentation

Note that while in this article we will provide examples using the Python programming language and some specific tools
for sharing and documentation, the overall concepts are not language specific and apply broadly to any language or
environment.

Sharing
-------
Perhaps the most obvious requirement for making your code useful to others is sharing it! After all, no one can use
your code if they don't know about it. It may be less obvious why this is the first topic to be discussed, since it
may seem intuitive that you should share your application after you are finished developing it. However, I have put this
topic first for a reason.

First of all, I would like to encourage everyone to share their projects early. With a lot of
people, there is an understandable tendency to want to get things just right before letting them out into the world.
But it might take a long time for your project to get to that stage, if it ever does! If you share your work in
progress, on the other hand, some parts of it may be useful to others, or they may even contribute.

The second reason why sharing code should be the first step in the development process is to do with the tools that we
use to do so. The Git revision control software is one of the most useful and widely used tools available for managing
code in development. This, coupled with the Github hosting service (don't conflate Git with Github), makes the perfect
system for managing your project as you continue to develop it, and releasing updates in a controlled manner. We don't
have room in this article for a complete introduction to Git and Github, but my recommendation is to place all or your
software projects under Git revision control, and host them on Github (or similar services) for both sharing and
backup purposes.

.. figure:: _static/git_workflow.svg

    `Image: Git Centralized Workflow <https://www.atlassian.com/git/tutorials/comparing-workflows>`_


Configuration
-------------
Keep your configuration separate from your code. This is the key lesson to take away when it comes to writing the code
for a reusable application. To explain what this means, let us consider the following example:

.. code-block:: python

    import numpy as np
    import matplotlib.pyplot as plt
    from scipy import integrate, signal

    # Read data
    flow = np.genfromtxt("data.csv")

    # Calculate volume
    flow_filtered = signal.savgol_filter(flow, 20, 2)
    volume = integrate.cumulative_trapezoid(flow_filtered, dx=0.01, initial=0)

    # Plot results
    plt.plot(flow, label="Flow")
    plt.plot(volume, label="Volume")
    plt.legend()
    plt.show()

The above code snippet shows a very simple python script that takes in data from a file, processes it, and plots it
to screen. But the actual function of the code is not important. What I'd like to draw your attention to is that the
code uses several parameters as input to the functions, and relies on the presence of a specific external file. Taken
together, these elements can be thought of as the program's *configuration*. If this code were to be used for anything
other than the specific case it is set up for, some or all of these variables would need to change. You can imagine that
as the script grew bigger and more complicated, it would become increasingly difficult to quickly locate the parameter
in need of changing for any given task. So how can we alleviate this difficulty?

The simplest way would be to create intermediate variables for each of the configuration parameters, and place them
at the top of the file. That way, whenever anyone needs to change the program's configuration, they know exactly where
to make changes to the code. See the amended snippet below:

.. code-block:: python

    import numpy as np
    import matplotlib.pyplot as plt
    from scipy import integrate, signal

    # Define settings
    data_filename = "data.csv"
    filter_window_length = 20
    filter_order = 2
    dx = 0.01
    initial = 0

    # Read data
    flow = np.genfromtxt(data_filename)

    # Calculate volume
    flow_filtered = signal.savgol_filter(flow, filter_window_length, filter_order)
    volume = integrate.cumulative_trapezoid(flow_filtered, dx=dx, initial=initial)

    # Plot results
    plt.plot(flow, label="Flow")
    plt.plot(volume, label="Volume")
    plt.legend()
    plt.show()

This code is significantly improved already, and much easier to configure. This way of coding is considered best
practice and I recommend using this technique as a bare minimum for any project. But, as a project grows, especially
if more than one person is using the application, there are more advanced techniques you can apply.

As a software project grows, it can become useful to fully separate the configuration from the code. Consider the
updated script below:

main.py:

.. code-block:: python

    import numpy as np
    import matplotlib.pyplot as plt
    from scipy import integrate, signal
    import json
    from tkinter import Tk
    from tkinter.filedialog import askopenfilename

    # Define settings
    config_filename = "conf.json"
    with open(config_filename, "r") as file:
        conf = json.load(file)

    # # Select data file
    Tk().withdraw()
    data_filename = askopenfilename(title="Select data file", initialdir=".")
    Tk().destroy()

    # Read data
    flow = np.genfromtxt(data_filename)

    # Calculate volume
    flow_filtered = signal.savgol_filter(flow, conf["filter_window_length"], conf["filter_order"])
    volume = integrate.cumtrapz(flow_filtered, dx=conf["dx"], initial=conf["initial"])

    # Plot results
    plt.plot(flow, label="Flow")
    plt.plot(volume, label="Volume")
    plt.legend()
    plt.show()

conf.json:

.. code-block:: json

    {
      "filter_window_length": 20,
      "filter_order":   2,
      "dx" : 0.01,
      "initial" : 0
    }

The above code has a few interesting improvements. First, the configuration parameters have been placed in an entirely
separate file from the code. This is particularly useful in situations where multiple people are using a piece of code,
all with different parameter requirements. They may still, however desire to continuously receive updates to the code
as the project progresses and new features are added. If their parameter changes are made in a separate file, it is much
easier for them to pull in updates to the code without manually resetting their configurations each time.

A second very useful improvement that has been made to the above code is how it is given a data file. The hard coded
filename has been replaced with a function that brings up a file select dialog for the user, making it much easier for
them to quickly specify which file to operate on. This type of simple yet powerful updates can greatly improve the
usability of an application.

Testing
-------
Unit tests are a crucial, yet often overlooked, part of software development. This is especially true for software that
will be developed by multiple people. The overall purpose of software tests is to define how a program can be expected
to behave. Tests can be set up to run automatically before any change is accepted, and if any change causes a section
of code to behave differently than previously defined, the tests will fail. This gives the developers a chance to
fix the code before any errors are encountered by the users.

Unit tests are very easy to write in Python. As an example, consider the code below.

In main.py:

.. code-block:: python

     def calculate_volume(flow, dx, initial):
        volume = integrate.cumulative_trapezoid(flow_filtered, dx=dx, initial=initial)
        return volume

In test_main.py:

.. code-block:: python

    def test_calculate_volume():
        sample_frequency = 100
        duration = np.pi
        time = np.linspace(0, np.pi, int(duration*sample_frequency))
        flow = np.sin(time)

        # Integral from zero to pi of sin(x) dx is 2.
        correct_max_volume = 2

        volume = calculate_volume(flow, 1/sample_frequency, initial=0)
        max_volume = volume[np.argmax(volume)]

        # Check to two decimal places
        np.testing.assert_almost_equal(correct_max_volume, max_volume, decimal=2)

The example from the previous section has been broken into functions, and we are interested in ensuring that the
calculate_volume function has the desired behaviour. In Python, the way to create a test for this is to simply create
a new function called test_calculate_volume() (as we will see later, it is important that the function name starts with
the word "test"). From basic trigonometry, we know that the area under a sine function between zero and pi is equal to
2. Therefore, we create input data representing this condition and feed it into our function under test. We then compare
the output to our known correct output using the assert statement.

In order to make use of our new test function, we need to use a Python module called *pytest*. When pytest is installed
it can be run as a command line utility, and it automatically searches a project for functions with names begining with
"test". pytest runs these functions and if the assert passes, the tests are considered to have passed, while if the
assert fails, the tests are considered to have failed. In our example, we can see that if the calculate_volume function
were to be accidentally modified to return results incompatible with our known mathematically correct result, the test
would fail, alerting us to the situation.

Documentation
-------------
Documentation may be the most important of the four topics we've discussed so far. Without documentation of some form,
it's highly unlikely that a piece of software will be useful to anyone except the developer. This means that, in terms
of increasing the impact of your work, writing a little documentation is often far more efficient than time spent
developing new features. In terms of content, there are a few main topics I suggest you include in the documentation
for a software application:

**1. What it is:**

The start of any good documentation should be a high level introduction detailing things like the project's purpose,
it's structure, motivations for creating it, and any broader context needed to understand the ecosystem in which the
project is intended to be used. This often requires the developer to mentally take a step back from the project and
imagine the mindset of a new user with no prior knowledge.

**2. Features:**

It's a good idea to list features up front, to give a prospective user a better idea of the specific capabilities of
a piece of software.

**3. User Guide:**

Any features that you wish others to be able to use should be documented with instructions in the user guide. Ideally
these will contain screenshots of the program in use.

As an example, see below a snippet of some documentation for the code we looked at previously.

.. image:: _static/volume_calculator_no_sidebar.png
    :class: with-border

The usage section goes on to describe the required format for the input data file, and the
function of each of the configuration parameters. `See the full document here.
<https://github.com/acreegan/creating_software_tools_talk/tree/main/step_4/docs>`_

One final subject to discuss is how to publish documentation so it is accessible to users of your application. For
Python, there is a commonly used tool called Sphinx which allows you to easily build web ready documentation from
simple text files, and this documentation can then be hosted on free services such as readthedocs or github pages.
The documentation above is an example of a Sphinx project, and you can see more detailed documentation build with Sphinx
below in the :ref:`Further Reading` section


To Sum Up
---------
Before we finish I want to acknowledge a couple of important topics that there wasn't room for in this article
to discuss:

**Packaging**

Packaging in Python is the process of setting up a system which makes it easy for others to install your code
and use it as a distinct unit. Python packages can range from simple to complex, but is very useful. I
encourage you to learn more about it.

**Code level documentation**

While we discussed project level documentation in this article, code level documentation (i.e. documentation
of each function and code element, written inside the python file) is a key element to documentation, though
it is more important to developers than to users.

In any case, I hope that his article has showed that you can make your code much more useful with some
relatively simple steps. I wish you all good luck in writing more useful, more impactful software.

Further Reading
---------------

- Source code for this article and examples: `<https://github.com/acreegan/creating_software_tools_talk>`_

- Real project demonstrating these concepts in use: `<https://abi-eit.github.io/tetrahedralizer>`_

- More resources for research software development: `<https://github.com/Research-software-development-resources>`_

- Git tutorials from Atlassian: `<https://www.atlassian.com/git/tutorials>`_

- Sphinx homepage: `<https://www.sphinx-doc.org/>`_

.. toctree::
   :hidden:

   self



