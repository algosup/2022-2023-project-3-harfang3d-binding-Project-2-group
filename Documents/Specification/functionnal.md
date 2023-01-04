<!--#### -> Click [here](https://github.com/algosup/2022-2023-project-3-harfang3d-binding-Project-2-group/blob/main/readme.md) to go to the Read Me.-->

# Functionnal Specification
## Table of content 
- functionnal Specification
  - [Project roles](#1-project-roles)
  - [overview of the company](#overview-of-the-company)
  - [Goal of the project](#goals)

###  1. Project roles :
| PERSON |   ROLE  | DOCUMENT |
| :----: | :-----: | :------: |
| Alexandre BOBIS | Software Engineer |  |
| Audrey TELLIEZ | Program Manager | [functionnal specification]()|
|Florent HUREAUX | Tech Lead | [Technical specification ]()  |
|Salaheddine NAMIR | Quality Assurance (QA)| [test plan]()|
| Pierre GORIN | Project Manager | |

### 2. Overview of the company 

[HARFANG®3D](https://www.harfang3d.com/en_US/) builds real-time 3D tools for industry professionals. They enable the implementation and deployment of 3D solutions (HMI, VR/AR, simulation, interactive 3D), regardless of development language or platform constraints.

They meet two different types of demands :

- HARFANG® Studio is the ideal 3D editor for creating real-time scenes and animations that match your design vision.
  <!-- 2 espaces à la fin de la ligne -->
  It can handle the entire 3D graphics workflow in a simple and optimised way, without compromising integration with other development environments.
    <!-- 2 espaces à la fin de la ligne -->  
  Everything that works in HARFANG® Studio is compatible with their HARFANG®Framework and its supported coding languages.
<br>
- HARFANG® Framework is an easy-to-adapt, cross-platform, multi-language, powerful and optimized 3D visualization engine written in C++ and accessible via an open API in C++, or high-level programming languages such as Python, Golang, and Lua.

### 3. Goals

The goal of this project is to create a binding between our 3D engine, written in C++, and the F# programming language. This binding will allow us to use our 3D engine in a F# environment and access its functionality from within a F# program.

To achieve this goal, we will need to research different approaches for creating bindings, select appropriate tools and libraries, and implement the binding according to our chosen approach. We will also need to test the binding to ensure that it is functioning correctly and meets the requirements of our project.



#personage
*dev F#
dev nul 
dev python 
adim it harfang pour creer aussi leur propre visuel 

<!---
### Author
<img src="https://avatars.githubusercontent.com/u/114394252?v=4" width="150">
### [**`Audrey Telliez`**](https://github.com/audreytllz)
##### *Program Manager*
-->

****************************************************************
FABGen : Fabgen is a set of Python scripts to generate C++ binding code to different languages.  
It was written as a SWIG replacement for the Harfang Multimedia Framework (http://www.harfang3d.com).