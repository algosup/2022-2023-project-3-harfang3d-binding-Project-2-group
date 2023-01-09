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
        - [Aurélia:](#aurélia)
        - [Jean-Marc:](#jean-marc)
        - [Baptiste:](#baptiste)
      - [Nathalie:](#nathalie)
    - [6. Use case](#6-use-case)
    - [7. What will happen in the futur](#7-what-will-happen-in-the-futur)
      - [Today :](#today-)
      - [In the futur :](#in-the-futur-)
    - [8. Development and Environement](#8-development-and-environement)
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

|Function	| Criteria	|Level	| Flexibility|
|:----:|:----:|:----:|:----:|:----:|:----:|
| F# functions     | entry of code     |  put code     |  F0  |
|convert to F# in C or C++ | use C API for convert  | code F# / code C/C++ | F1|
| part with C/C++ code | 


### 5. Personas and Scenarios
##### Aurélia:
  Aurélia, HARFANG®3D developer since 2018, living near Orléans. She write her code and have the idea of what she could would a thing but she code this in F#. But HARFANG®3D 3D can't take F#. She write an email to put F#  in the code list. And permit to her and customers to do in F#. If they can't she will have to find a language that is in HARFANG®3D and that can do the same thing

##### Jean-Marc:
  Jean-Marc, developer in an IT services company and Python dev. He would like to make a wallpaper for a project. So he made a code in python in the HARFANG® Framework application. And then he put the code given by HARFANG® Framework into HARFANG® Studio.

##### Baptiste:
  Baptiste is a computer science student. He wanted to create a game application with his own hands. So he learned C++ to make a code and put it in HARFANG® Studio.

#### Nathalie:
  Nathalie is dev python. And she wanted to create a game application in python. So she put in HARFANG® Framework  a code in python. And she has take the code give by HARFANG® Framework. And also put it in HARFANG® Studio.
  
<!--
idées :
*dev F# company 
dev nul 
dev python 
adim it harfang pour creer aussi leur propre visuel 
-->

### 6. Use case
<!--voir plus tard ----- > discord -->

### 7. What will happen in the futur
#### Today :

#### In the futur : 

### 8. Development and Environement

  - F#
  - C++
  - Python
  - (Windows / MAC OS)  

******************************
## Glossary 

FABGen : Fabgen is a set of Python scripts to generate C++ binding code to different languages.  
It was written as a SWIG replacement for the Harfang Multimedia Framework (http://www.harfang3d.com).


<!---
### Author
<img src="https://avatars.githubusercontent.com/u/114394252?v=4" width="150">
### [**`Audrey Telliez`**](https://github.com/audreytllz)
##### *Program Manager*
-->




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