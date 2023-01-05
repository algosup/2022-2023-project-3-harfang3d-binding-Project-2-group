- [Harfang3D Progress Report](#harfang3d-progress-report)
  - [Date: 01/03/2023](#date-01032023)
- [1 - Introduction](#1---introduction)
  - [1.1 - Purpose of the meeting](#11---purpose-of-the-meeting)
  - [1.2 - Participants](#12---participants)
- [2 - Overview of 3D engines in industry](#2---overview-of-3d-engines-in-industry)
  - [**2.1 - Need for 3D engines in civil, defense, and industry sectors**](#21---need-for-3d-engines-in-civil-defense-and-industry-sectors)
  - [**2.2 - Suitability of HARFANG® 3D for the industry**](#22---suitability-of-harfang-3d-for-the-industry)
- [3 - Topics related to the automotive industry](#3---topics-related-to-the-automotive-industry)
- [4 - Standards related to software development in various industries](#4---standards-related-to-software-development-in-various-industries)
  - [**4.1 - ISO**](#41---iso)
  - [**4.2 - MISRA**](#42---misra)
  - [**4.3 - AUTOSAR**](#43---autosar)
- [5 - Long-term nature of the industry](#5---long-term-nature-of-the-industry)
- [6 - Role of standards in ensuring software quality and reliability](#6---role-of-standards-in-ensuring-software-quality-and-reliability)
- [7 - Introduction to HARFANG® SDK](#7---introduction-to-harfang-sdk)
  - [**7.1 - Compatibility with Python, Lua, and Go**](#71---compatibility-with-python-lua-and-go)
  - [**7.2 - C++ vs Python**](#72---c-vs-python)
- [8 - Presentation of projects by attendees](#8---presentation-of-projects-by-attendees)
- [9 - Overview of features in the HARFANG® 3D engine browser](#9---overview-of-features-in-the-harfang-3d-engine-browser)
  - [**9.1 - Extern directories**](#91---extern-directories)
  - [**9.2 - bgfx graphic abstraction layer**](#92---bgfx-graphic-abstraction-layer)
- [10 - Overview of Fabgen](#10---overview-of-fabgen)
  - [**10.1 - Description of Fabgen**](#101---description-of-fabgen)
  - [**10.2 - Key features of Fabgen**](#102---key-features-of-fabgen)
  - [**10.3 - How to use Fabgen**](#103---how-to-use-fabgen)
  - [**10.4 - Compatibility with Python**](#104---compatibility-with-python)
- [11 - Overview of HARFANG® 3D](#11---overview-of-harfang-3d)
  - [**11.1 - Goal of providing 3D HMI**](#111---goal-of-providing-3d-hmi)
  - [**11.2 - Description of HARFANG® 3D engine**](#112---description-of-harfang-3d-engine)
  - [**11.3 - Description of HARFANG® Studio**](#113---description-of-harfang-studio)
- [12 - Conclusion](#12---conclusion)
- [13 - Contacts](#13---contacts)

# Harfang3D Progress Report<br>
## Date: 01/03/2023
<br><br><hr><br><br>

# 1 - Introduction

## 1.1 - Purpose of the meeting

The purpose of the meeting was to discuss the use of HARFANG® 3D in the industry, as well as the use of the HARFANG® SDK.

## 1.2 - Participants

The participants of the meeting were group 1 to 4, as well as François Gutherz and Emmanuel Julien.


<br><br><hr><br><br>

# 2 - Overview of 3D engines in industry

At the meeting, we explored the need for 3D engines in the civil, defense, and industry sectors and the decision to build a 3D engine from scratch.

## **2.1 - Need for 3D engines in civil, defense, and industry sectors**

HARFANG® 3D, specifically, was highlighted as suitable for the industry because it can be used to visualize and manipulate complex data, control and monitor a robot remotely, and meet strong technical requirements.
It was noted that these engines must be able to run on-premise and be 100% offline, as the video game industry is very interested in collecting user data and metrics and needs to be able to run on its own servers to ensure security and privacy.

## **2.2 - Suitability of HARFANG® 3D for the industry**

We also discussed whether game engines are suitable for use in the industry and concluded that 3D engines like HARFANG® are more appropriate due to their strong technical capabilities.


<br><br><hr><br><br>

# 3 - Topics related to the automotive industry

During the meeting, we discussed several important topics related to the automotive industry, including safety certification, embeddability, custom hardware, and power consumption, as well as the importance of MISRA, a set of rules for embedded software development in the automotive industry.
We emphasized the need for sovereignty and confidentiality in the industry and the importance of game engines with private and secure licenses that can run on-premise and offline.
Additionally, we noted that the video game industry is interested in collecting user data and metrics.


<br><br><hr><br><br>

# 4 - Standards related to software development in various industries

We also learned about three different standards that are relevant to software development in various industries: ISO, MISRA, and AUTOSAR.

## **4.1 - ISO**

ISO (International Organization for Standardization), which has many standards related to software development including ISO 26262 for the functional safety of road vehicles.

## **4.2 - MISRA**

MISRA (Motor Industry Software Reliability Association), a consortium of companies in the automotive industry that develops guidelines and standards for the development of safety-critical software.

## **4.3 - AUTOSAR**

AUTOSAR (AUTomotive Open System ARchitecture), a standard for the development of automotive software that provides a set of guidelines and tools for the development of software that is portable across different hardware platforms.


<br><br><hr><br><br>

# 5 - Long-term nature of the industry

We discussed the long-term nature of the industry and how industrial projects must be maintained for a period of 5-30 years, compared to the shorter commercial lifespan of video games (1-3 years). We emphasized the importance of maintainability, upgradability, and interoperability in this context.


<br><br><hr><br><br>

# 6 - Role of standards in ensuring software quality and reliability

According to the HARFANG® representatives, one common point between these standards is that they all relate to the development and use of software in specific industries and are intended to ensure the safety, reliability, and quality of the software.
These standards play an important role in ensuring that software is developed to high standards and can be trusted to perform critical functions safely and effectively.


<br><br><hr><br><br>

# 7 - Introduction to HARFANG® SDK

## **7.1 - Compatibility with Python, Lua, and Go**

HARFANG® SDK is compatible with Python, Lua, and Go.
It is compatible with Python, Lua, and Go because it is written in C++ and uses the C API to expose its functionality to other programming languages.

## **7.2 - C++ vs Python**

It's written in C++ mainly for performance reasons, to ensure that it can be used in real-time applications. Python is popular for rapid development and strong data science capabilities, but is approximately 75 times slower than C++.


<br><br><hr><br><br>

# 8 - Presentation of projects by attendees

The attendees presented several projects they have been working on, including a head-up display for Valeo, the consideration of the human factor for workers in train stations, the analysis of complex data, and a 3D flight simulator.
These projects demonstrate the diverse range of applications and capabilities of the tools and technologies being developed, including teleoperation or the remote control of a device or machine.
These projects showcase the potential of the tools and technologies being developed by the attendees to be used in a variety of different industries and applications.


<br><br><hr><br><br>

# 9 - Overview of features in the HARFANG® 3D engine browser

## **9.1 - Extern directories**

The HARFANG® 3D engine browser includes the "extern" directories, which contain packages that can be imported into the engine.

## **9.2 - bgfx graphic abstraction layer**

Additionally, the engine includes "bgfx", a graphic abstraction layer.
This layer provides a consistent interface for accessing graphics and rendering functionality, which allows developers to use the engine more easily and efficiently.


<br><br><hr><br><br>

# 10 - Overview of Fabgen

During our research, we learned about Fabgen, a binding generator written in Python that is designed to improve upon SWIG, a similar tool.

## **10.1 - Description of Fabgen**

Fabgen is able to generate bindings for a variety of programming languages including dynamically typed languages like Python and Lua, and statically typed languages like Go.

## **10.2 - Key features of Fabgen**

One of the key features of Fabgen is its use of a common part called "gen.py" to implement as much functionality as possible.
Fabgen also aims to take advantage of newer APIs whenever possible and uses a C API to extend the target language with native extension modules.

## **10.3 - How to use Fabgen**

To use Fabgen, it is necessary to import and call functions from a C-style ABI.
Fabgen requires a minimum of three functions, "check", "to_c", and "from_c", which are used to test if an object in the target language holds a copy or reference to a C/C++ object, return a reference to the C/C++ object held by an object in the target language, and return an object in the target language holding a copy or reference to a C/C++ object, respectively.

## **10.4 - Compatibility with Python**

Overall, Fabgen appears to be a useful tool for generating bindings between different programming languages and is compatible with Python versions above 3.2. It uses the Py_LIMITED_API macro to ensure that extension modules it generates can be used by any version of Cpython above 3.2.


<br><br><hr><br><br>

## 11 - Overview of HARFANG® 3D

One of the main goals of HARFANG® is to provide the latest generation of HMI (Human-Machine Interface) in 3D.

HARFANG® offers two different products for creating 3D graphics and animations: the HARFANG® 3D engine, also known as the HARFANG® Framework, and HARFANG® Studio.

## **11.1 - Goal of providing 3D HMI**

Currently, HMI is mainly 2D, but the goal of HARFANG® is to build HMI in 3D for applications such as extended reality.
By providing a 3D HMI, HARFANG® aims to make it easier for users to interact with systems and machines and to enable more efficient and effective communication between humans and machines.
This can help to improve the overall performance and usability of the systems and machines that use Harfang's HMI technology.

## **11.2 - Description of HARFANG® 3D engine**

The HARFANG® 3D engine is a cross-platform, multi-language tool that is written in C++ and accessible via an open API in C++, as well as other high-level programming languages such as Python, Golang, and Lua.
It is easy to adapt, powerful, and optimized, making it well-suited for creating real-time 3D graphics and animations.

## **11.3 - Description of HARFANG® Studio**

HARFANG® Studio is a 3D editor that is specifically designed for creating real-time scenes and animations that match a user's design vision.
It is capable of managing the entire 3D graphics production workflow in a simple and optimized manner, and is compatible with the HARFANG® 3D engine and its supported coding languages.
It does not compromise the integration of other development environments.


<br><br><hr><br><br>

# 12 - Conclusion

Overall, both HARFANG® products are designed to enable users to easily create high-quality 3D graphics and animations.


<br><br><hr><br><br>

# 13 - Contacts

For any further questions or inquiries, please contact François Gutherz at francois.gutherz@harfang3d.com or Emmanuel Julien at emmanuel.julien@harfang3d.com.

[1]: https://www.youtube.com/watch?v=IJS9GMP9h9Y
