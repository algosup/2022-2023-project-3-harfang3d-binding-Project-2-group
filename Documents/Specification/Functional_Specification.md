<!--#### -> Click [here](https://github.com/algosup/2022-2023-project-3-harfang3d-binding-Project-2-group/blob/main/readme.md) to go to the README.md-->

# Functionnal Specification

<details>

<summary>Table of content</summary>

- [Functionnal Specification](#functionnal-specification)
    - [1. Stakeolders](#1-stakeolders)
    - [2. Company Overview](#2-company-overview)
    - [3. Goals](#3-goals)
    - [4. Requirements](#4-requirements)
    - [5. Personas and Scenarios](#5-personas-and-scenarios)
    - [6. Use case](#6-use-case)
    - [7. What will happen in the futur](#7-what-will-happen-in-the-futur)
    - [8. Risks and Assumptions](#8-risks-and-assumptions)
    - [9. Development and Environement](#9-development-and-environement)
  - [Glossary](#glossary)

</details>

###  1. Stakeolders

| Person/Organisation |   ROLE  | DOCUMENT |
| :----: | :-----: | :------: |
| HARFANG3D         | Project Owner         | |
| Robert PICKERING  | Tech Consultant       | |
| Pierre GORIN      | Project Manager       | |
| Audrey TELLIEZ    | Program Manager       | [Functionnal Specification]() |
| Florent HUREAUX   | Tech Lead             | [Technical Specification]() |
| Alexandre BOBIS   | Software Engineer     |  |
| Salaheddine NAMIR | Quality Assurance (QA)| [Test plan]() |

### 2. Company Overview

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

### 4. Requirements

F0 = mandatory; F1 = important; F2 = secondary

|Function	| Criteria	|Level	|Tolerance	|Flexibility|
|:----:|:----:|:----:|:----:|:----:|:----:|

### 5. Personas and Scenarios
<!--
idées :
*dev F#
dev nul 
dev python 
adim it harfang pour creer aussi leur propre visuel 
-->

### 6. Use case
<!--voir plus tard -->

### 7. What will happen in the futur

### 8. Risks and Assumptions

### 9. Development and Environement

  - F#
  - C++
  - Python
  - (Windows / MAC OS)  

******************************
## Glossary 

<!---
### Author
<img src="https://avatars.githubusercontent.com/u/114394252?v=4" width="150">
### [**`Audrey Telliez`**](https://github.com/audreytllz)
##### *Program Manager*
-->

****************************************************************
FABGen : Fabgen is a set of Python scripts to generate C++ binding code to different languages.  
It was written as a SWIG replacement for the Harfang Multimedia Framework (http://www.harfang3d.com).


<!---
 Function specification
    - details how work the product
    - clear and detail description
    - define the requirement and constraints
    - doesn’t describe the implementation
    - basis for testing
    - serves as a contract between the  team and the users

- Functional specification
    - context
    - goal/ scope
    - functional requirements
    - acceptance criteria
    - design
    - non-functional requirement
    - out of scope
    - security
    - glossary
-->