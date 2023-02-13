<details>

<summary>Table of content</summary>

- [1- KPI](#1--kpi)
- [2- Measure the current status of ours KPIs](#2--measure-the-current-status-of-ours-kpis)
- [3- List the causes for the non-conform KPIs](#3--list-the-causes-for-the-non-conform-kpis)
  - [Pareto law](#pareto-law)
    - [Deadlines](#deadlines)
    - [Safety](#safety)
    - [Environment](#environment)
  - [Impact-effort matrix](#impact-effort-matrix)
  - [Problem solving](#problem-solving)
    - [DMAIC problem 1](#dmaic-problem-1)
    - [DMAIC problem](#dmaic-problem)
  - [Reporting during problem solving](#reporting-during-problem-solving)

</details>

## 1- KPI

- 100% of functional specs written
- 100% of technical specs written
- 80% of test plan written
- 35% of code functions written
- 30% test procedure
- 5% integration test completed
- 5% functional test completed
- 50% action decided during the last meeting milestone completed
- 70% of code commented
- 20% of code documented
- 100% of code reviewed
- 80% of critical path done
- 100% of Communication plan written
- 80% of the project calendar done
- 80% of the project weekly report done
- 80% of customers meetings written
- 90% of the research document written

## 2- Measure the current status of ours KPIs

- Run FABgen to generate biding in CPython, Lua and Go
- Examine how th GO,Lua and python binding work
- Create F# functions
- Create test function
- Convert to F# in C or C++
- Build Harfang as a F# library
- Functionnal code

## 3- List the causes for the non-conform KPIs

### Pareto law


#### Deadlines

80% in time (from trello)

#### Safety

100% check that we don’t put some malware (from Github)

#### Environment

90% every members do his part of works (from Trello)

### Impact-effort matrix

<img src="image.png" width="500">

### Problem solving

Problem 1: can’t have an idea of how the wrapper will work
→ Impact: High
→ Effort: Low-Medium

#### DMAIC problem 1

Define:
→ Our problem is that we don’t have any idea about how we can do the wrapper, we don’t know how the program works so therefore we don’t know how we will adapt it to our needs.
→ The limits: our problem is the intern of the program but it’s primordial to know the things we are working on.

Measure:
→ It is a primordial problem so we quantify the problem at 100%.
→ Identify what factors are causing the lack of understanding of how the wrapper works.

Analyze:
→ The data that we have is only the FABGen code. The code isn’t commented on and is like “spaghetti code”.

→ We can’t do the wrapper right now. The wrapper is supposed to take a part of code written in F# and to “translate” each variable, each method, each function, etc… in a language understandable by Harfang®3D (in this case it’s C++).

→ We can’t do the wrapper because we’ve not so much information about the functions in FABGen, because of a lack of time, because we prioritize the documents (because we wanted to send the documents to the customers this week).

Improve:
→ One of the solutions is to redo the whole code, but it’s a bit too long, we need to implement each binding.

→ Another solution is to understand the code. We will be able to implement what we want to.

→ Maybe Comment the code but it’s not a good idea (it takes too much time).

→ Plan to do it as the primary priority and follow it.

Control:
→ This would allow us to begin the project on a solid foundation.

→ Monitor the process and the wrapper to ensure that the solutions are effective and that the problem does not reoccur. Implement a system to regularly review and improve the wrapper's performance.

#### DMAIC problem

### Reporting during problem solving
