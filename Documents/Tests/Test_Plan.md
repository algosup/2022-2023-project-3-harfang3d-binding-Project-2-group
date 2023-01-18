#### -> Click [here](https://github.com/algosup/2022-2023-project-3-harfang3d-binding-Project-2-group/blob/main/readme.md) to go to the Read Me.

# Test Plan

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
      <!-- - [Test F#](#test-f)-->
      - [Scope](#scope)
        - [Test F# on FABgen](#test-f-on-fabgen)
      <!-- - [Test C++](#test-c)-->

### Introduction
This test plan is for HARFANG® 3D company, asked for an binding F#  for it 3D engine with Fabgen, an binder developpe by the group. This binder generator is used instead of SWING. FabGen has already implemented the following language, CPython 3.2+, Lua 5.3+ and Go 1.11+.

### Objectif and Tasks
#### Objectif
The main tasks is to implement F# on FABgen.
F# is a hight level, static and compiled language and  it's expected for FABgen to bind with it.
The other tasks is more a nice to have, build F# binding and F# version of HARFANG library.

#### Tasks
- Add F# to FabGen.
- Build the F# binding for HARFANG.(nice to have) 
- build a F# (or DOT.NET) version of the HARFANG  library (nice to have)
  
### Scope
For binding, we need to compare the target language (F#) identifier with the C++ one, check if entities match with both language and else, make a function to match entities of target language with C++.  
<!--#### Test F# 
|   REFERENCE TEST        | TEST          |      RESULT EXPETED         |  RESULT |
|:----------|:---------:|:--------------:|---------: |
|   a1        |    TDD n°1(name of function)       |             | | -->


#### Test F# on FABgen
At this case, we test the FABgen function works to bind with F#.
|     REFERENCE TEST      |   TEST        |     RESULT EXPETED          | RESULT |
|:----------|:---------:|:--------------:|----: |
|   b1        |   check: if the object in target language hold a copy or reference to a C/C++ object of specific type       |         true    | |
| b2| to_c: return a reference to  the C/C++ object  held by an object in the target language   | C/C++ object | | |
|b3| from_c: return an object in target language or reference to  C/C++ object|F# object||
|b4|idendify: identify elementary type common of both language |type||
|b5| map: mapping a single or more elementary type  of target language|type||
|b6|obj_memb: access object members of elementary type|object||
|b7|warp: warp an object from the target language| object|||
|b8|destruct: destruct a warping object| deleted object ||

<!--#### Test C++
|     REFERENCE TEST      |    TEST       |    RESULT EXPETED            | RESULT  |
|:----------|:---------:|:--------------:|----:|
|     c1      |           |               |   |-->



### Author

<img src="https://avatars.githubusercontent.com/u/71770514?v=4" width="150">

### [**`Salaheddine NAMIR`**](https://github.com/T3rryc)
##### *Quality Assurance (QA)*
