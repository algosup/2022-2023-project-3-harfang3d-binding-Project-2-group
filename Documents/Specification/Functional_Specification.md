<!--#### -> Click [here](https://github.com/algosup/2022-2023-project-3-harfang3d-binding-Project-2-group/blob/main/readme.md) to go to the README.md-->

# Functionnal Specification

<details>

<summary>Table of content</summary>

- [Functionnal Specification](#functionnal-specification)
    - [1. Stakeolders](#1-stakeolders)
      - [Roles:](#roles)
      - [Documents:](#documents)
    - [2. Company Overview](#2-company-overview)
    - [3. Goals](#3-goals)
    - [4. Requirements](#4-requirements)
    - [5. Personas and Scenarios](#5-personas-and-scenarios)
        - [5.1 Aurélia](#51-aurélia)
        - [5.2 Jean-Marc](#52-jean-marc)
        - [5.3 Baptiste](#53-baptiste)
        - [5.4 Nathalie](#54-nathalie)
    - [6. Use case](#6-use-case)
    - [7. What will happen in the future](#7-what-will-happen-in-the-future)
        - [7.1. Today](#71-today)
        - [7.2. In the future](#72-in-the-future)
    - [8. Development and Environement](#8-development-and-environement)
    - [9. Glossary](#9-glossary)

</details>

###  1. Stakeolders

####  Roles:

| Person/Organisation |   ROLE  |
| :----: | :-----: |
| HARFANG3D         | Project Owner         |
| Robert PICKERING  | Tech Consultant       |
| Pierre GORIN      | Project Manager       |
| Audrey TELLIEZ    | Program Manager       |
| Florent HUREAUX   | Tech Lead             |
| Alexandre BOBIS   | Software Engineer     |
| Salaheddine NAMIR | Quality Assurance (QA)|

#### Documents:

| Person  | DOCUMENT |
| :----: | :-----: |
| Pierre GORIN (Project Manager)| |
| Audrey TELLIEZ (Program Manager)| [Functionnal Specification](#functionnal-specification) |
| Florent HUREAUX (Tech Lead)| [Technical Specification](/Documents/Specification/Technical_Specification.md) |
| Salaheddine NAMIR (QA)| [Test case](/Documents/Tests/Test_Case.md) |
| Salaheddine NAMIR (QA)| [Test plan](/Documents/Tests/Test_Plan.md) |

### 2. Company Overview

[HARFANG®3D](https://www.harfang3d.com/en_US/)  builds real-time 3D tools for industry professionals. They enable the implementation and deployment of 3D solutions (HMI [^8], VR/AR, simulation, interactive 3D), regardless of development language or platform constraints.

They meet two different types of demands :

- HARFANG® Studio is the ideal 3D editor for creating real-time scenes and animations that match your design vision. It can handle the entire 3D graphics workflow in a simple and optimised way, without compromising integration with other development environments.Everything that works in HARFANG® Studio is compatible with their HARFANG®Framework and its supported coding languages.

<br>

- HARFANG® Framework is an easy-to-adapt, cross-platform, multi-language, powerful and optimized 3D visualization engine written in C++ and accessible via an open API [^9] in C++[^2], or high-level programming languages such as Python, Golang, and Lua.

### 3. Goals

The goal of this project is to implement the langage F# in FABGen[^6] Following this, it will allow us to create a binding between our 3D engine, written in C++[^2], and the F#[^1] programming language. This binding will allow us to use our 3D engine in a F# environment and access its functionality from within a F# program.

to create a binding between our 3D engine, written in C++[^2], and the F#[^1] programming language. This binding will allow us to use our 3D engine in a F# environment and access its functionality from within a F# program.

To achieve this goal, we will need to research different approaches for creating bindings(Fabgen[^6] in is case), select appropriate tools and libraries, and implement the binding according to our chosen approach. We will also need to test the binding to ensure that it is functioning correctly and meets the requirements of our project.

### 4. Requirements

F0 = Mandatory;      F1 = Important;     F2 = Secondary;

|Function| Criteria|Flexibility|
|:----:|:----:|:----:|:----:|
|run FABgen to generate biding in CPython, Lua and Go| use FABgen | F0 |
|examine how th GO,Lua and python binding work | use FABgen|  F0  |
| create F# functions     | inspire by the unit test |  F1  |
| create test function |base on ("basic_type_exchange.py", "function_call.py") | F1|
|convert to F# in C or C++ | use C API for convert  | F1|
|build Harfang as a F# library  |create code |F2|

### 5. Personas and Scenarios

##### 5.1 Aurélia

  Aurélia is an F# developer. She writes her code in F#. But HARFANG®3D doesn't support F#. So she must find a way to convert her code.

##### 5.2 Jean-Marc

  Jean-Marc is a Python dev and he works has an IT developer in a services company. He would like to make a wallpaper for a project. So he made a code in python in the HARFANG® Framework application. And then he put the code given by HARFANG® Framework into HARFANG® Studio.

##### 5.3 Baptiste

  Baptiste is an IT student and learns F# at school. and he would make an app game by his hands. So he use F# to code his game and he use FABGen to bind the F# into C++ and put it in HARFANG® Studio.

##### 5.4 Nathalie
  Nathalie is dev python. And she wanted to create a game application in python. So she put in HARFANG® Framework  a code in python. And she has take the code give by HARFANG® Framework. And also put it in HARFANG® Studio.

<!--
idées :
*dev F# 
dev python
IT student and learn F# 
dev python 

adim it harfang pour creer aussi leur propre visuel 
-->

### 6. Use case
<img src="/Documents/Specification/Use_Case_FABGen.png" width="500"> 

### 7. What will happen in the future

##### 7.1. Today

Add F# language in HARFANG®3D.

##### 7.2. In the future
  - add F# to FABgen
  - build the F# binding for HARFANG
  - build a F# (or DOT.NET) version of the HARFANG library
<!--ajouter de nouveaux languages  -->

### 8. Development and Environement

- F#[^1]
- C++ [^2]
- Python [^3]
- (Lua [^4] and Go [^5])
- (Windows / MAC OS)  

******************************

### 9. Glossary

[^1]: F# is a functional, imperative, object-oriented programming language for the . NET PLATFORM. F# is developed by Microsoft Research.

[^2]: C++ is a programming language: it is used to write computer programs, for example to create mobile applications or video games. C++ was created from the C language, whose functionalities it extends: C++ makes it possible to do object-oriented programming.

[^3]: Python is the most widely used open source programming language for computer scientists. It has become the leading language for infrastructure management, data analysis and software development.

[^4]: Lua is a free, reflexive, imperative scripting language. It is designed to be embedded in other applications to extend them.

[^5]: Go is an open-source, statically typed programming language. This programming language includes tools for safe memory usage, object management, rubbish collection and static typing along with concurrency.

[^6]: FABGen is a set of Python scripts to generate C++ binding code to different languages.  
It was written as a SWIG[^7] replacement for the Harfang Multimedia [Framework](http://www.harfang3d.com). Its role is to prepare an interface between the HARFANG object code and the DOT.NET VM.

[^7]: SWIG (Simplified Wrapper and Interface Generator) is an open source software tool for connecting software or software libraries written in C/C++ with scripting languages such as: Tcl, Perl, Python, Ruby, PHP, Lua or other programming languages such as Java, C#, Scheme and OCaml.

[^8]: A Human Machine Interface (HMI) is the point of contact between users and machines. These interfaces allow users to control machines, monitor processes and, in some cases, intervene.

[^9]: API (Application Programming Interface) is a software interface which makes it possible to "connect" a software or a service to another software or service in order to exchange data and functionalities.



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
