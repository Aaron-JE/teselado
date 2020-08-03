# A hello world for simulation. A short tutorial.

This short tutorial should get you up and running on this repo. Hopefully it
will make you feel more comfortable following the code and it will encourage
you to make changes to it in order to improve it. Any issues, please contact
[Diego](mailto:diego.peteiro@just-eat.com) directly or just drop a message on
the Slack channel [#proj-just-simulate]().

### Page 1: A gentle intro to event driven systems

[Page 1](page_1.ipynb) provides a very gentle introduction to event driven
systems. This is important because the simulator is built using events and
messages being passed between the different agents of the system. In this
short tutorial, you will see a cat interacting with a dog, meowing and
woofing at each other.

### Page 2: Modeling restaurants, customers and couriers

[Page 2](page_2.ipynb) shows a very simple intro to modeling restaurants,
customers and couriers. These agents communicate with each other using events
as explained in the previous tutorial. A bit more complicated than meowing
and woofing but hopefully easy to follow when reading the code.

A very summarised version of the message flow would be something like this
1. A customer places an order to a restaurant
2. The order manager creates an order into the system
3. The assigner will assign a courier to deliver the order
4. The courier receives a message but they could reject the order
5. If the order gets rejected, the assigner will need to find another courier
6. When the order gets accepted, the courier will start the job or add the
job to their backlog if already busy with other orders.
7. When the courier gets to the restaurant, it will notify the restaurant
8. When the food is ready, the restaurant will tell the courier to collect
the order
9. The courier will drive to the delivery address
10. The customer will collect the food and the order will get tagged as
delivered by the order manager.

This flow is very flexible and extensible and can be adapted to many other
circumstances and situation someone might want to model. For example, if you
want some homework to prove yourself you have understood the code, try to add
the possibility for restaurants to reject orders from customers, and the
little changes downstream when that happens, e.g. a customer will try to
place another order to a different restaurant.  

### Page 3: A gentle intro to time distributions

[Page 3](page_3.ipynb) provides a very gentle introduction to time 
distributions. Time distribution aren't any different from probability
distributions. They will just have units, e.g. hours, minutes, seconds. It
is important to note that all times in the simulation are implemented as
`timedelta` with the simulation starting at `timedelta(0)`. It is just
an implementation detail, but brings many little, handy benefits. That
doesn't mean that you cannot account for specific dates, but from the
simulation point of view, everything starts at `timedelta(0)` and that
could be `1970-01-01 00:00:00` or `1999-12-31 23:59:59` for you. It doesn't
matter to much, you know what that time zero is anyway. The simulation
doesn't need to know. 

### Page 4: Running simulations with randomly generated data

[Page 4](page_4.ipynb) provides the very beginning of something that could be
useful for simulating delivery orders. Still very simplistic, but hopefully
enough to get the gist of it. Here, restaurants, customers and couriers are
randomly allocated around a given radius in a circle. Orders could follow a
specific distribution of arrival (see previous page for more details on
time distributions) or you could hard coded them. It's ok, whatever is useful
to get you head around a basic simulation.

### Page 5: Running simulations from real data

[Page 5](page_5.ipynb) is under construction but will provide some more info
about how to start modeling your agents using real data. Whilst this page is
not finished, you can find an example of pretty much the same on this test
[here](/tests/just/simulate/test_simulation.py) just in case you are 
interested. Still many other things to be modeled, e.g. wait times at
restaurants, wait times at customers, accurate average speeds for couriers,
etc. Those little bits that will bring the simulation closer to reality.

### More to come

We will be adding more content to this tutorial as we develop the simulator.
Stay tuned and drop as a line on [#proj-just-simulate]() for more info or
feature requests. We will be happy to help.
