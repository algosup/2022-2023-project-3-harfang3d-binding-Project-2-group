#### -> Click [here](https://github.com/algosup/2022-2023-project-3-harfang3d-binding-Project-2-group/blob/main/readme.md) to go to the Read Me.

# Technical Specification

<details> 
<summary style="text-decoration: underline; font-size:150%">Table of contents:</summary>


- [Technical Specification](#technical-specification)
  - [1. Glossary :](#1-glossary-)
    - [2. Project Overview :](#2-project-overview-)
    - [3. Solution :](#3-solution-)
      - [3.1. Goal of the project :](#31-goal-of-the-project-)
      - [3.2. Current Solution :](#32-current-solution-)
        - [3.3. Supported languages](#33-supported-languages)
          - [Python 3.2+ (CPython)](#python-32-cpython)
          - [Lua 5.3+](#lua-53)
          - [Go 1.11+](#go-111)
      - [Proposed Solution :](#proposed-solution-)
          - [F#](#f)
    - [4. Development of the Solution :](#4-development-of-the-solution-)
    - [5. Risks:](#5-risks)
    - [6. Success Evaluation :](#6-success-evaluation-)
      - [6.1. Unit Test :](#61-unit-test-)
      - [6.2. Test Plan :](#62-test-plan-)
    - [Author](#author)
    - [**`Florent HUREAUX`**](#florent-hureaux)
        - [*Tech Lead*](#tech-lead)
  

</details>

## 1. Glossary :

Fabgen : It's a set of Python scripts to generate C++ binding code to different languages.

SWIG : It's a software development tool that connects programs written in C and C++ with a variety of high-level programming languages.

API : They are mechanisms that enable two software components to communicate with each other using a set of definitions and protocols.

ABI : An application binary interface (ABI) is an interface between two binary program modules. Often, one of these modules is a library or operating system facility, and the other is a program that is being run by a user.

Unit Test : It's a type of software testing where individual units or components of a software are tested.

Statically-typed language  : It's a language (such as Java, C, or C++) where variable types are known at compile time.

Dynamically typed languages : Type checking takes place at runtime or execution time. This means that variables are checked against types only when the program is executing.




### 2. Project Overview :

Fabgen was written for the Harfang 3D project to bring the C++ engine to languages such as Python, Lua and Go. It was written as a replacement for SWIG, a very well-known binding generator supporting a lot of target languages.

SWIG has different issues we wished to address:

Very old and complex codebase. Language support is written partially in C and SWIG interface files which are almost a language by themselves. The C codebase does everything through a single Object struct hiding the real type of variables making it extremely difficult to debug and extend the SWIG core.
Uneven feature support between languages with missing features although the target language could support them.
Fabgen tries to solve this issues by:

Using Python to implement Fabgen and the binding definitions themselves.
Implementing as much as possible of the features in a common part of the program (gen.py).
As a newer project Fabgen also tries to leverage newer APIs whenever possible for example by supporting CPython limited ABI so that extension modules it generates can be used by any version of CPython >3.2 without recompilation (at least in theory, the Py_LIMITED_API support in CPython is finicky at best).

### 3. Solution :

#### 3.1. Goal of the project :

The goal of the project is to create a binding for F# language in order to bring the C++ engine for the Harfang 3D project.

#### 3.2. Current Solution :

Right now, Fabgen support languages such as Python, Lua and GO.
##### 3.3. Supported languages
###### Python 3.2+ (CPython)
Interpreted bytecode
Dynamically typed
C API to extend the language with native extension modules (stable ABI since 3.2 through the Py_LIMITED_API macro)
C API to create values and call functions
###### Lua 5.3+
Interpreted bytecode
Dynamically typed
C API to extend the language with native extensions
C API to push values to the VM stack and call functions
###### Go 1.11+
Compiled
Statically typed
Link to C library, C++ has to be wrapped with C first (https://stackoverflow.com/questions/1713214/how-to-use-c-in-go)

#### Proposed Solution :

We want to add a new F# binding to the existing solution.
###### F#
JIT from IL
Statically typed
Link to C library (C++ has to be wrapped with C first)


### 4. Development of the Solution :

F# is a staticaly typed language.
In order to develop the solution, We will follow the same structure that are already done for static language like GO or C#.

First, We will create a mapping of elementary types. We will identify the elementary types common to both languages and create a mapping between them. C types might map to a single or more types in the target language.
It will look like this :
[Insert example here]

Afterward, we will implement a C API wrapping the C/C++ objects. We will create functions to access object's members of elementary type and implement a mechanism to access nested objects.
Note that passing C/C++ objects will be done through the use of naked pointers, the target language will however not be able to differentiate object A from object B (as both essentially are void *) so wrapped objects need to include a type tag to catch programming errors such as passing an object of type A to a function expecting an object of type B.

This can be done by using a structure like the following:

```C
struct wrapped_native_obj {
  uint32_t type_tag;
  void *obj;
};
```
The ownership of a wrapped object needs to be stored as well in order to properly handle object destruction.
```C
struct Vec3 {
  float x, y, z;
};

const Vec3 *get_global_vec3();
Vec3 new_vec3(float x, float y, float z);
```
The get_global_vec3 function returns a pointer to a Vec3 that is owned by the native layer, ownership is not passed to the target language. For small objects it might be justified to force a copy of the returned object to address potential issues with the object lifetime, the target language gets ownership of the returned object. But some native types might be too expensive to copy or might simply be non-copyable.

In addition, we will implement a better integration with the target language
While the wrapped API can technically everything we need to use the native library its usage will feel completely foreign to the target language.

### 5. Risks:

We need to avoid taking shortcut and think about every possibility in order to avoid core dump or memory leak on the user side at a later point. 
We have no idea how intertwined the code will be in the user's program so they must be correct from every possible angle.

### 6. Success Evaluation :
#### 6.1. Unit Test :

In order to evaluate the success of our product, we will follow a Test plan and do Unit Test to our program.
We will be using Python to run our Unit Test.
#### 6.2. Test Plan :

[More information](https://github.com/algosup/2022-2023-project-3-harfang3d-binding-Project-2-group/blob/documents/Documents/Tests/test-plan.md) 

### Author

<img src="https://avatars.githubusercontent.com/u/71769655?v=4" width="150">

### [**`Florent HUREAUX`**](https://github.com/florenthureaux)
##### *Tech Lead*
