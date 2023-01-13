#### -> Click [here](https://github.com/algosup/2022-2023-project-3-harfang3d-binding-Project-2-group/blob/main/readme.md) to go to the Read Me.

# Test Plan

### Author

<img src="https://avatars.githubusercontent.com/u/71770514?v=4" width="150">

### [**`Salaheddine NAMIR`**](https://github.com/T3rryc)
##### *Quality Assurance (QA)*

### Table of content 
- [Test Plan](#test-plan)
    - [Author](#author)
    - [**`Salaheddine NAMIR`**](#salaheddine-namir)
        - [*Quality Assurance (QA)*](#quality-assurance-qa)
    - [Table of content](#table-of-content)
        - [Introduction](#introduction)
        - [Objectif and Tasks](#objectif-and-tasks)
             - [Objectif](#objectif)
             - [Tasks](#tasks)
      - [Test F#](#test-f)
      - [Test CPython](#test-cpython)
      - [Test C++](#test-c)

### Introduction
This test plan is for HARFANG® 3D company, asked for an binding F#  for it 3D engine with Fabgen, an binder developpe by the group. This binder is used instead of SWING. FabGen has already implemented CPython 3.2+, Lua 5.3+ and Go 1.11+.

### Objectif and Tasks
#### Objectif
The main tasks is create a binding generator for F# source code, assure the  is alway works with the target language F#, and used binding library on Harfang studio.

#### Tasks
- Link a F# API on FabGen.
- Build a binding F# interface. 
- Binding method, type of F#.
  

#### Test F# 
|   REFERENCE TEST        | TEST          |      RESULT EXPETED         |  RESULT |
|:----------|:---------:|:--------------:|---------: |
|   a1        |    TDD n°1(name of function)       |             | |


#### Test CPython
At this case, we test the FABgen function works to bind with F#.
|     REFERENCE TEST      |   TEST        |     RESULT EXPETED          | RESULT |
|:----------|:---------:|:--------------:|----: |
|   b1        |   check: if the object in target language hold a copy or reference to a C/C++ object of specific type       |         C/C++ object     | |
| b2| to_c: return to an object with the target language C/C++ held by an object in the target language   | C/C++ object | | |
|b3| from_c: return an object in target language or reference to  C/C++ object|C/C++ object||
|b4|idendify: identify elementary type common of both language and create mapping between them |type||
|b5| map: mapping a single or more elementary type  of target language|type||
|b6|obj_memb: access object members of elementary type|object||
|b7|warp:||||
|b8|destruct:|||

#### Test C++
|     REFERENCE TEST      |    TEST       |    RESULT EXPETED            | RESULT  |
|:----------|:---------:|:--------------:|----:|
|     c1      |           |               |   |