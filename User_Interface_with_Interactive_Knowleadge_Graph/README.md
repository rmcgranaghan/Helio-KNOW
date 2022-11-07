
The code in this directory was contributed by Swapnali Yadav (@SwapnaliY16). It was developed as a frontend user interface for a community knowledge graph created for the [NASA Center for HelioAnalytics](https://helioanalytics.io/). 

To understand the details of this user interface, please see [Swapnali's Masters Degree final presentation](https://docs.google.com/presentation/d/14iZqQidtRYyYHRrO6jseUP5zfoCe4GYV/edit?usp=share_link&ouid=102947217778623290502&rtpof=true&sd=true). The frontend was designed for the CfHA community knowledge graph (a graph instantiated with data provided by that community and using the Community Action and Understanding via Semantic Enrichment (CAUSE) ontology (paper forthcoming). However, this code is sufficiently general to provide a foundation for frontend interactivity for any community-based knowledge graph. 

Project Overview
- User Interface to enable community members to analyse and extract information from ontologies and researchers seeking associations among semantic terms such as astrophysics, machine learning, publications, papers, and conferences in the organisational realm.
- User interface is developed to provide an instinctive experience for users to discover data to answer the core competency questions, which are:
    - Who are we engaging with the most? Who do I have the most associations with?
    - What projects do we (a member or members of the CfHA) work on with this person or group? What missions do we work on with this person or group?
    - What skills and expertise does this person or group have?
- It is built on the knowledge base called CAUSE, which is made up of topics, objects, individuals and groups and affiliations.
- In addition, it is built on a technology stack such as (1) Eclipse RDF4J for processing, and handling RDF data (2) Ontotext GraphDB, a graph database for storing RDF with SPARQL support (3) React for building component-based user interface.






