
# Contribution Guidelines
These guidelines have been adadpted from those followed by the open science [Pangeo](https://pangeo.io/) community. 

Please note that this project follows a [Contributor Code of Conduct]() developed by [Contributor Covenant](https://www.contributor-covenant.org/). By participating in this project you agree to abide by its terms.



## How to contribute?

---

### Understanding *where* to contribute
This repository (and the Helio-KNOW project) has many facets. We attempt to categorize the directions for development into several categories:

#### Refine the HelioKNOW Suite of Ontologies
This is the first official draft of HelioKNOW, which means that it could easily be improved in terms of both breadth and depth of coverage. There are relevant concepts that are either stubbed or not represented entirely. Several options are listed below. 

Most obviously, the notion of temporality is absent from the model. Thus, this version of the HelioKNOW can be used to model fundamental relationships between concepts, but is not yet suitable for describing dynamic relationships between phenomena as they unfold through time. 

Another consideration that led to the creation of this ontology is defining the terminology that could be used to find relevant scientific research. To support that goal, one might want to incorporate a scientific publications taxonomy into the model. Concepts like Publishing Media  (web/print), Format (text/audio/video),  Forum (conference/symposium), Type (article/monograph/thesis), etc. could help dimension the space to aid with content discoverability. 
Similarly, the concept of Discipline was considered as a useful dimension of categorizing research, so it was defined and stubbed with a few initial values, but could definitely benefit from a thoughtful expansion. 

Finally, HelioKNOW defines a few basic relationships like hk:characterizedBy and hk:influences, which we started refining, mostly in the Phenomenon ontology. We anticipate the need to describe new relationships between concepts, especially as new classes are being added. Particularly, we would consider defining relationships between publications, disciplines, and phenomena one of main priorities. 

#### Relate to Other Knowledge Organization Systems
The value of this ontology can best be realized in linking it to other KOS.

On one end of the compatibility spectrum, we are aiming to improve knowledge representation interoperability within the Astrophysics community. To that end we have taken initial steps to align terminology between HelioKNOW and the Unified Astronomy Thesaurus (UAT). We led the effort to extend the UAT to comprehensively represent Heliophysics and identified a future arrangement in which the UAT maintains regions and HelioKNOW maintains phenomena, with both semantic resources importing those elements from the other in order to include the most up to date terminology. In Fall 2025 we contributed 173 concepts in a full taxonomy that were co-identified with the Heliophysics community and harmonized in cooperation with the UAT steering committee to establish a new version of the astronomy thesaurus. Those terms were deliberately limited to be region-based and we altered the phenomena ontology to use the same terminology where regions are included to be consistent. Finally, we organized an agreement with UAT to import HelioKNOW to represent Heliophysics phenomena.  
A meaningful next step would be to identify and close the gaps between the two. Integration options range from the lightweight rdfs:seeAlso between related concepts, to a more nuanced skos-based mapping, to full ontological alignment using owl:sameAs|owl:equivalentClass|owl:equivalentProperty to establish formal equivalences. 
More generally, initial efforts were made to align HelioKNOW with the SWEET Ontology. Any effort towards expanding the alignment will surely benefit the larger scientific community across multiple disciplines. 
Finally, for truly global recognition and compatibility, one could further develop Schema.org compatibility, either through direct extension, or, perhaps, by creating a schema.org profile of the ontologies. 

#### HelioKNOW Knowledge Graph
We are looking forward to the community taking up the task of adding more datasets to the HelioKNOW knowledge graph. We started by uplifting existing Madrigal and SPASE Instrument data into RDF, but the more datasets could be added the more valuable a resource HKKG could become. 

#### Graph Analytics
The hope is that with addition of new data the HelioKNOW Knowledge Graph would provide the necessary substrate for advanced data analytics. 
Even now one could use geoSPARQL to establish equivalence (or at least physical proximity) between the Madrigal and the SPASE Instruments.  
Another option is to build a solution supporting path traversal tasks (e.g. shortest path) that would enable exploration of long cause-and-effect chains. 

#### Additional ideas
- NLP: *natural language processing*; This category includes tools and analysis that scrape text-based resources (e.g., academic publications) and produce insight from them
- ML: *machine learning*; Tools for performing machine learning analyses on Heliophysics data
- ontology: Tools that build and visualize the knowledge representation system/data model for Helio-KNOW data
- platform: Tools that create the interaction layer to Helio-KNOW data, tools, and resources.
- storymaps: Inspiring, immersive stories by combining text, interactive maps, and other multimedia content.
- utils: General utilities for data accumulation, wrangling, and analysis
- Knowledge_Modeling_Curriculum: Curricular/pedogogical/learning resources for knowledge modeling, which generally includes concept mapping, vocabulary harmonization, ontology development. 

These categories will remain fluid and you are welcome to suggest a change to the existing categories (create [an issue](https://github.com/rmcgranaghan/Helio-KNOW/issues)) or suggest creating an entirely new one (create [a discussion topic](https://github.com/rmcgranaghan/Helio-KNOW/discussions) for the community to converse about the addition). 


---

### Software/technology contributions
You'll need a [GitHub account](https://github.com/)!

1. Explore the resources, especially the Jupyter Notebooks. 
2. Fork this repository, create changes and new resources on your own
3. Make a [pull request](https://docs.github.com/en/github/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/about-pull-requests) to pass your improvements to this repository! 
4. Create [issues](https://github.com/rmcgranaghan/Helio-KNOW/issues) for discussion topics and for development that you recommend

---

### Suggesting changes and identifying issues
Please create [issues](https://github.com/rmcgranaghan/Helio-KNOW/issues) for development that you recommend to Helio-KNOW and for issues you find with existing tools in this repository. 

---

### Asking questions/creating discussions
If you wish to ask a question or create a discussion, please leave your comment in the [Discussions page](https://github.com/rmcgranaghan/Helio-KNOW/discussions).






[Further guidance on how to contribute to Github projects.](https://www.dataschool.io/how-to-contribute-on-github/)

