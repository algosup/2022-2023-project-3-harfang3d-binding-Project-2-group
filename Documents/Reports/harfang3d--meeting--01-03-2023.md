Title: Harfang3D Progress Report
Date: 01/03/2023
==========================================

Introduction:
-------------

*   Briefly introduce the project and its goals
*   Mention the use of Fabgen and Harfang 3D

Background:
-----------

*   Provide some context and background information on Fabgen and Harfang 3D (e.g., what are they, what are they used for)

Presentation highlights:
------------------------

*   Summarize the key points and information presented during the presentation given by the creators of Harfang 3D
*   Mention any new or noteworthy information that was shared about Harfang 3D
*   Include any quotes or notable examples given during the presentation

Current progress:
-----------------

*   Describe the work that has been done so far on the project
*   Mention any challenges or obstacles that have been encountered and how they were addressed

Upcoming tasks:
---------------

*   Outline the next steps for the project
*   Identify any potential issues that may arise and how they will be addressed

Reflections:
------------

*   Share any personal thoughts or insights you had during the presentation
*   Mention how the information presented ties into your project and its goals

Conclusion:
-----------

*   Summarize the main takeaways from the presentation and the progress that has been made on the project so far
*   Mention any next steps or follow-up actions that may be necessary based on the information presented



# Notes by Pierre
<!-- Write here -->

# Notes by Salaheddine
<!-- Write here -->

# Notes by Florent
<!-- Write here -->

# Notes by Alexandre

Mainly use for industries

- Automotive Cluster
- Automotive HUD
- Human factor study
- Simulation
- Data visualization
- Teleoperation


Industry = Strong Technical Requirements (Satefy certifications, embeddability and custom hardware and power consumption)
Industry = Sovereignty & Confidentiality (Game engines with private and insecure license in the long term, Must run on premise, 100% offline, the VG industry needs metrics, very hungry for user data)
Industry = Long term (A video game has a commercial life of 1 to 3 years, an industrial project must be maintained between 5 to 30 years, maintainability, upgradability, interoperability)

GOALS:

- 1. Produce latest generation HMIs
- 2. Provide sovereignty and strategic autonomy
- 3. Ensure greater responsivness, portability and interoperability

extern = packages imported

bgfx = graphic abstraction layer

contact: francois.gutherz@harfang3d.com --- emmanuel.julien@harfang3d.com


FABgen written as a replacement for SWIG, an other binding generator.
It tries to solve this issue by:

- Using python to implement FABgen and the binding definitions themsleves
- Implementing as much as possible of the features in a common part of the program (gen.py)

As a newer project FABgen also tries to leverage newer APIs whenever possible.

Python and Lua: Dynamically typed.
Go: Statically typed.
C API to extend the language with native extension module.
Minimum of 3 functions:

- check
- to_c
- from_c

# Notes by Audrey
<!-- - presentation by customer
    - to visualized and manipulate different data
    - 

safety certification (misra) ,  embeddability and custom hardware , power consumption 

—> iso, misra, autosar

maloc instruction (c or c++)

tout doit etre déclarer avant dappeler la fonction 

JPU on monitor (jsp 😢)

- confidential :
    
    control every thinks  , private licence 
    

- long term :
    
    a video game has a commercial life of 1  to 3 years 
    
    an industrial project must be maintained between 5 to 30 years 
    
     maintainability, upgradability , interoperability 
    

goals : produce lastest generation HMIs 

provide sovereignty and strategic autonomy, ensure greater responsiveness portability …

tools for designers 

prototyping and 3D simulations,  creation of 3D sciences & 3d HMIs

tools for 

secure
—> leurs docs git sont open sources 

API and python 

like lua go and f# 

whats append in human brain 

vr headset, wristband, external loudspeaker, video monitoring 

numpy

fast —> c , c++ , javas 2 times —> “slow”

python 35 times to slow

- biding definition in  python
- common part of the program
- au dessus (python ≤ 3.2) de la version 3.2 python
- Cpython limited  ABI so that extension modules it generates can be used by any version  of Cpython > 3.2.
- dinamically typed
- interpreted bytecode
- C API to extend the language with native extension modules
- ABI Py_LIMITED_API macro
- C API to create values and call functions

Fabgen create a minimum of Three functions :

- `check`: Test if an object in the target language holds a copy or reference to a C/C++ object of a specific type.
- `to_c`: Returns a reference to the C/C++ object held by an object in the target language.
- `from_c`: Return an object in the target language holding a copy or reference to a C/C++ object.

import and call functions from a C-style ABI. most of the time this will be the only way to call into a different language 

**1. Create a mapping of elementary types**

**2. Implement a C API wrapping the C/C++ objects**

**3. Better integration with the target language**

 -->