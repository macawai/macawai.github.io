---
title: "Hybrid computing using a neural network with dynamic external memory"
source: "http://www.nature.com/articles/nature20101.epdf?author_access_token=ImTXBI8aWbYxYQ51Plys8NRgN0jAjWel9jnR3ZoTv0MggmpDmwljGswxVdeocYSurJ3hxupzWuRNeGvvXnoO8o4jTJcnAyhGuZzXJ1GEaD-Z7E6X_a9R-xqJ9TfJWBqz"
authors:
  - "Alex Graves"
  - "Greg Wayne"
  - "Malcolm Reynolds"
  - "Tim Harley"
  - "Ivo Danihelka"
  - "Agnieszka Grabska-Barwińska"
  - "Sergio Gómez Colmenarejo"
  - "Edward Grefenstette"
  - "Tiago Ramalho"
  - "John Agapiou"
  - "Adrià Puigdomènech Badia"
  - "Karl Moritz Hermann"
  - "Yori Zwols"
  - "Georg Ostrovski"
  - "Adam Cain"
  - "Helen King"
  - "Christopher Summerfield"
  - "Phil Blunsom"
  - "Koray Kavukcuoglu"
  - "Demis Hassabis"
tags:
  - nature
  - google
  - memory
  - DNC
published_in:
  - terriblegoat-research-feature
abstract: |
  Artificial neural networks are remarkably adept at sensory processing, sequence
  learning and reinforcement learning, but are limited in their ability to represent
  variables and data structures and to store data over long timescales, owing to the
  lack of an external memory. Here we introduce a machine learning model called a
  differentiable neural computer (DNC), which consists of a neural network that can
  read from and write to an external memory matrix, analogous to the random-access
  memory in a conventional computer. Like a conventional computer, it can use its
  memory to represent and manipulate complex data structures, but, like a neural
  network, it can learn to do so from data. When trained with supervised learning,
  we demonstrate that a DNC can successfully answer synthetic questions designed to
  emulate reasoning and inference problems in natural language. We show that it can
  learn tasks such as finding the shortest path between specified points and
  inferring the missing links in randomly generated graphs, and then generalize
  these tasks to specific graphs such as transport networks and family trees.
  When trained with reinforcement learning, a DNC can complete a moving blocks
  puzzle in which changing goals are specified by sequences of symbols. Taken
  together, our results demonstrate that DNCs have the capacity to solve complex,
  structured tasks that are inaccessible to neural networks without external
  read–write memory.
snippet: |
  This paper is filled with fascinating ideas from the folks at google,
  but is a little light on the
  technical details required to reproduce the systems and results described.

  DNCS as defined as an extension to previous differentiable explicit memory NN
  models, using existing techniques for direct, and pattern matching memory accesses.
  The key addition seems to be the ability for the NN to request blocks of memory
  to be allocated
  or deallocated, the ability to read from these blocks, and the ability to navigate
  back and forward through the allocation blocks. This allows the training to be
  more independent of the amount of memory available to the NN.

  While interesting results are provided that show this network out preforms existing
  LTSTM networks, the improvement due the new block-access does not seem to be
  evaluated on its own. Nor are many details about how the allocation and forward-backward
  lists are kept differentiable.

  Further details are promised in the form of a forthcoming code release - which should
  clear up all of these issues.
---
