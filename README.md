# BlokX

This is a web application built using: Python, Flask, and HTML/CSS.

The main purpose of this application is as an exercise in learning how a blockchain, in its most fundamental form, functions.

The blockchain uses a Proof-of-Work method to validate new blocks. It is currently a locally hosted application that requres a dedicated server to run. The goal for future versions of this application is to create a decentralized node structure for the blockchain, itself, allowing for a React front-end to communicate with the blockchain through the implementation of a RESTful API. The front-end will compile information to then display to the end user.

The current version of this application, although technically functioning, has some deficiencies. Other than the lack of a decentralized protocol, the application has such a drw on computing power that it requires a system with multiple processing cores with multiple threads in order to function smoothly. The mining function that runs on its own thread in the background does not allow any other processes to run on machines with a minimum of computing capacity. This deficiency will hopefully be solved when the back-end blockchain is set up to run in a decentralized manner with the front-end application making asynchronous calls to the back-end API for the information required by the UI.

Currently, there is no difficulty adjustment for the mining method. This works okay while the blockchain is run on a centrl server, as this can be monitored and adjusted as necessary. However, in order to function as a true blockchain, in a decentralized manner, this difficulty adjustment algorithm will need to be implemented.

For anyone interested in collaborating on this project, I am happy to discuss ideas and improvements that can be made!
