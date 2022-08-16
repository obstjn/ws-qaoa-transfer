# Transferability Map
### Setup (exemplary for ubuntu 18.04): 
* ``git clone https://github.com/obstjn/ws-qaoa-transfer.git``
* ``cd ws-qaoa-transfer``
* ``sudo -H pip install virtualenv`` (if you don't have virtualenv installed)
* ``virtualenv venv`` (create virtualenv named 'venv')
* ``source venv/bin/activate`` (enter virtualenv; in Windows systems activate might be in ``venv/Scripts``)
* ``pip install -r requirements.txt`` (install application requirements)

### Execution:
* Run with: ``py interactive-map.py``
* or      : ``py interactive-diffmap.py``

### Usage:
Click into the map to investigate the transferability of two subgraphs.
Displayed next to them are their landscapes.
The blue circles are the points that are evaluated for the transferability coefficient.
For the donor landscape these are the maxima.

You can use the tools of matplotlib (zoom/pan) to explore the map.
If a tool is active the data won't be updated when clicking into the map.

The order in which the graphs appear is shown in ``graphs/graph-ordering.pdf``
