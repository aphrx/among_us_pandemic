# Among Us Pandemic Simulator
Have you ever wanted to simulate a pandemic? Whether it was to learn more of how a slightly different virus could alter things or how a different response could affect the outcome. Well now you can... and within the beloved Skeld Map

### Execution

To run the simulation, simply run ```python simulator.py``` or ```python3 simulator.py``` depending on the version. You could also attach parameters to change the simulation.

### Arguments

```--origin```: This changes how many agents start off with the virus. Appending ```--origin 5``` for instances changes the simulation so that 5 people start off with the virus.

```--infection-rate```: This changes how easily the virus spreads from one agent to the other. The default value is 0.03 which gives it a 3% chance to infect per frame.

```--radius```: This changes how close a susceptible agent has to be near an infected agent to possibly get the virus. The default value is 20.

```--amount```: This changes the total population of the simulation. This number should be greater or equal to the origin parameter. The default value is 20.

```--lifespan```: This changes how long the virus keeps an agent infected. The default value is 1000.

```--sporadic```: This changes how random the movements of the agents are. The default value is 0.1 so that there is a 10% chance per frame that it'll move in a random direction.

```--quarantine```: This parameter signifies how many frames it should take an agent to be quarantined. The default value is -1 which represents that the quarantine is disabled.

```--quarantine-probability```: This parameter reduces how likely agents are to go into quarantine once the quarantine frames have been met. The default value is 1.

```--mortality```: This signifies the probability per frame while the agent is infected that it will die. The default value is 0.0005 which represents 0.05% per frame.

```--visualize```: Adding this without any value will enable the simulation to record a log file. This is disabled by default.