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
        - [5.1 Aurélia](#51-aurélia)
        - [5.2 Jean-Marc](#52-jean-marc)
        - [5.3 Baptiste](#53-baptiste)
        - [5.4 Nathalie:](#54-nathalie)
    - [6. Use case](#6-use-case)
    - [7. What will happen in the futur](#7-what-will-happen-in-the-futur)
        - [Today:](#today)
        - [In the futur:](#in-the-futur)
    - [8. Development and Environement](#8-development-and-environement)
  - [Glossary](#glossary)
          - [1 - F#:](#1---f)
          - [2 - C++:](#2---c)
          - [3 - Python:](#3---python)
          - [4 - Lua:](#4---lua)
          - [5 - Go:](#5---go)
          - [6 - FABGen:](#6---fabgen)
          - [7 - SWIG:](#7---swig)
          - [8 - HMI:](#8---hmi)
          - [9 - API:](#9---api)
>>>>>>> 723e4d3d6ff445095a9e76f3d7642ac29a45d57d
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

[HARFANG®3D](https://www.harfang3d.com/en_US/)  builds real-time 3D tools for industry professionals. They enable the implementation and deployment of 3D solutions (HMI [[8]](#8---hmi), VR/AR, simulation, interactive 3D), regardless of development language or platform constraints.

They meet two different types of demands :

- HARFANG® Studio is the ideal 3D editor for creating real-time scenes and animations that match your design vision. It can handle the entire 3D graphics workflow in a simple and optimised way, without compromising integration with other development environments.Everything that works in HARFANG® Studio is compatible with their HARFANG®Framework and its supported coding languages.

<br>

- HARFANG® Framework is an easy-to-adapt, cross-platform, multi-language, powerful and optimized 3D visualization engine written in C++ and accessible via an open API [[9]](#9---api) in C++[[2]](#2---c), or high-level programming languages such as Python, Golang, and Lua.

### 3. Goals

The goal of this project is to create a binding between our 3D engine, written in C++[[2]](#2---c), and the F#[[1]](#1---f) programming language. This binding will allow us to use our 3D engine in a F# environment and access its functionality from within a F# program.

To achieve this goal, we will need to research different approaches for creating bindings, select appropriate tools and libraries, and implement the binding according to our chosen approach. We will also need to test the binding to ensure that it is functioning correctly and meets the requirements of our project.

### 4. Requirements

F0 = Mandatory;
F1 = Important;
F2 = Secondary;

|Function| Criteria|Level|Flexibility|
|:----:|:----:|:----:|:----:|:----:|:----:|
| F# functions     | entry of code     |  put code     |  F0  |
|convert to F# in C or C++ | use C API for convert  | code F# / code C/C++ | F1|

### 5. Personas and Scenarios

##### 5.1 Aurélia

  Aurélia, HARFANG®3D developer since 2018, living near Orléans. She write her code and have the idea of what she could would a thing but she code this in F#. But HARFANG®3D 3D can't take F#. She write an email to put F#  in the code list. And permit to her and customers to do in F#. If they can't she will have to find a language that is in HARFANG®3D and that can do the same thing

##### 5.2 Jean-Marc

  Jean-Marc, developer in an IT services company and Python dev. He would like to make a wallpaper for a project. So he made a code in python in the HARFANG® Framework application. And then he put the code given by HARFANG® Framework into HARFANG® Studio.

##### 5.3 Baptiste

  Baptiste is a student in IT. and he would make an app game by his hands. So he learn C++ to just put in HARFANG® Studio.

##### 5.4 Nathalie:
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
<img src="/Documents/Specification/image.png" width="500">

### 7. What will happen in the futur

##### Today:
Add F# language in HARFANG®3D.

##### In the futur: 
Add new languages.
<!--ajouter d enouveaux languages  -->

### 8. Development and Environement

  - F#[ [1]](#1---f-)
  - C++ [[2]](#2---c)
  - Python [[3]](#3---python)
  - (Lua [[4]](#4---lua) and Go [[5]](#5---go)) 
  - (Windows / MAC OS)  

******************************

## Glossary

###### 1 - F#:
F# is a functional, imperative, object-oriented programming language for the . NET PLATFORM. F# is developed by Microsoft Research.
###### 2 - C++:
C++ is a programming language: it is used to write computer programs, for example to create mobile applications or video games. C++ was created from the C language, whose functionalities it extends: C++ makes it possible to do object-oriented programming.
###### 3 - Python:
Python is the most widely used open source programming language for computer scientists. It has become the leading language for infrastructure management, data analysis and software development.
###### 4 - Lua:
Lua is a free, reflexive, imperative scripting language. It is designed to be embedded in other applications to extend them.
###### 5 - Go:
It is an open-source, statically typed programming language. This programming language includes tools for safe memory usage, object management, rubbish collection and static typing along with concurrency.

###### 6 - FABGen:
Fabgen is a set of Python scripts to generate C++ binding code to different languages.  
It was written as a SWIG [[8](#8---swig)] replacement for the Harfang Multimedia [Framework](http://www.harfang3d.com).

###### 7 - SWIG:
SWIG (Simplified Wrapper and Interface Generator) is an open source software tool for connecting software or software libraries written in C/C++ with scripting languages such as: Tcl, Perl, Python, Ruby, PHP, Lua or other programming languages such as Java, C#, Scheme and OCaml.

###### 8 - HMI:
A Human Machine Interface (HMI) is the point of contact between users and machines. These interfaces allow users to control machines, monitor processes and, in some cases, intervene.

###### 9 - API:
API (Application Programming Interface) is a software interface which makes it possible to "connect" a software or a service to another software or service in order to exchange data and functionalities.



<!---
### Author
<img src="https://avatars.githubusercontent.com/u/114394252?v=4" width="150">
### [**`Audrey Telliez`**](https://github.com/audreytllz)
##### *Program Manager*
-->



<!---
faire de temps en temps :
Product Requirement Document

High level overview of a problem to solve and the plan to address it 
Usually owned by the Product team

Articulate a problem and a proposition to address it (new capabilities or entirely new product)
Key decisions are listed but the implementation remain to be defined
Ideally a one-pager
Public, different audience
Meant to serve as a compass for the product and engineering teams





- Function specification
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