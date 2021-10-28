# Crypto-Project

<h2>Implementation of Anonymous Lightweight Chaotic Map-Based Authenticated Key Agreement Protocol for Industrial Internet of Things</h2>

The protocol is a seven step process having the below phases: <br/>
<br/>
1.Pre - Deployment Phase <br/>
2.Registration Phase <br/>
3.Login Phase <br/>
4.Authentication Phase <br/>
5.Password and Biometric Update <br/>
6.Smart Card Revocation Phase <br/>
7.Dynamic IoT Sensing Device Addition Phase <br/>
<br/>
This is a simulation of the above steps using python modules.
<br/>
<p>
  In the first phase of this paper, i.e., in the pre-deployment step, each of the sensor (ISDj) is
registered with the gateway node and is given its specific set of credentials . In the registration
phase a user Ui will be registered to the Gateway node to get his specific smartcard SCi and the
required parameters are stored in the smart card, SCi issued to the user. In the second and third
phases i.e., in login step and in the authentication step, the Ui and the selected ISDj by the Ui
mutually authenticate with the help of Gateway node and they establish a session key for
secure communicatation. If an already registered user wants to update password or his
biometric fingerprints, there is a phase called password and biometric phase to facilitate it. The
smartcard revocation phase is used when a user Ui’s SCi is lost or stolen.To deploy a new IoT
device later into this setup, after the main deployment, the dynamic IoT sensing device phase is
used.
 </p> 
<h3> Steps to run </h3>
python main.py
<br/>
Enter number of GWNs <br/> 
Enter number of ISD devices <br/>
Select a GWN number from the available ones 0 to n-1 of the number of GWNs <br/>
Enter an username and password <br/>
Select an ISD number from the available ones 0 to n-1 of the number of ISDs to establish a session with the user Ui entered above <br/>
Skey, Keyj, and various other hashes are computed in the intermediate steps. Finally session key Skeyj is established for further communication.
