package com.nasa;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;

import org.eclipse.rdf4j.query.BindingSet;
import org.eclipse.rdf4j.query.QueryLanguage;
import org.eclipse.rdf4j.query.TupleQuery;
import org.eclipse.rdf4j.query.TupleQueryResult;
import org.eclipse.rdf4j.query.Update;
import org.eclipse.rdf4j.repository.Repository;
import org.eclipse.rdf4j.repository.RepositoryConnection;
import org.eclipse.rdf4j.repository.manager.RemoteRepositoryManager;
import org.eclipse.rdf4j.repository.manager.RepositoryManager;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.slf4j.Marker;
import org.slf4j.MarkerFactory;

public class RemoteRepository {

	private static Logger logger = LoggerFactory.getLogger(RemoteRepository.class);
	private static final Marker WTF_MARKER = MarkerFactory.getMarker("WTF");

	public static void main(String[] args) {
		//writePerson("SwapnaliYadav", "Swapnali", "Yadav");
		System.out.println("********************************" + getPersonProfile(""));
	}

	public static List<HashMap<String, Object>> getPersonProfile(String name) {
		try {
			// Replace http://Swap:7200 with appropriate GraphDB remote repository URL
			RepositoryManager repositoryManager = new RemoteRepositoryManager("http://Swap:7200");
			repositoryManager.init();
			// Replace cfha-repository with created graphDB repository name
			Repository repository = repositoryManager.getRepository("cfha-repository");
			RepositoryConnection repositoryConnection = repository.getConnection();

			List<HashMap<String, Object>> personProfileList = new ArrayList<>();

			String queryStringForPerson = "PREFIX CfHA: <http://www.semanticweb.org/ontologies/2022/1/CfHA#> \n";
			queryStringForPerson += "PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> \n";
			queryStringForPerson += "select ?person ?givenName ?familyName ?location ?project ?mission ?skill ?affiliatedPerson ?affiliatedGroup ?affiliatedPartner \n";
			queryStringForPerson += "WHERE { \n";
			queryStringForPerson += "    ?person rdf:type CfHA:Person ; \n";
			queryStringForPerson += "    CfHA:givenName ?givenName; \n";
			queryStringForPerson += "    CfHA:familyName ?familyName. \n";
			queryStringForPerson += "    OPTIONAL {?person CfHA:hasLocation ?location} \n";
			queryStringForPerson += "    OPTIONAL {?person CfHA:associatedWithProject ?project} \n";
			queryStringForPerson += "    OPTIONAL {?person CfHA:associatedWithProcess ?mission} \n";
			queryStringForPerson += "    OPTIONAL {?person CfHA:hasSkill ?skill} \n";
			queryStringForPerson += "    OPTIONAL {?person CfHA:isConnected ?affiliatedPerson} \n";
			queryStringForPerson += "    OPTIONAL {?person CfHA:collaboratesWithGroup ?affiliatedGroup} \n";
			queryStringForPerson += "    OPTIONAL {?person CfHA:collaborateWithPartner ?affiliatedPartner} \n";
			if (name != null && !name.isEmpty())
				queryStringForPerson += "FILTER regex(STR(?person), \"" + name + "\")";
			queryStringForPerson += "} \n";

			TupleQuery queryForPerson = repositoryConnection.prepareTupleQuery(queryStringForPerson);
			try (TupleQueryResult result = queryForPerson.evaluate()) {
				for (BindingSet solution : result) {
					HashMap<String, Object> personMap = new HashMap<>();
					personProfileList.add(personMap);
					personMap.put("name", solution.getValue("person").stringValue());
					personMap.put("givenName", solution.getValue("givenName").stringValue());
					personMap.put("familyName", solution.getValue("familyName").stringValue());
					personMap.put("location", solution.getValue("location")!= null?solution.getValue("location").stringValue():null);
					personMap.put("project", solution.getValue("project")!= null?solution.getValue("project").stringValue():null);
					personMap.put("mission", solution.getValue("mission")!= null?solution.getValue("mission").stringValue():null);
					personMap.put("skill", solution.getValue("skill")!= null?solution.getValue("skill").stringValue():null);
					personMap.put("affiliatedPerson", solution.getValue("affiliatedPerson")!= null?solution.getValue("affiliatedPerson").stringValue():null);
					personMap.put("affiliatedGroup", solution.getValue("affiliatedGroup")!= null?solution.getValue("affiliatedGroup").stringValue():null);
					personMap.put("affiliatedPartner", solution.getValue("affiliatedPartner")!= null?solution.getValue("affiliatedPartner").stringValue():null);
				}
			}

			repositoryConnection.close();
			repository.shutDown();
			repositoryManager.shutDown();
			return personProfileList;
		} catch (Throwable t) {
			logger.error(WTF_MARKER, t.getMessage(), t);
		}
		return null;
	}

	public static HashMap<String, Object> getAllPeople(String name, String group, String affiliation, String object, String project, String mission, String topic) {
		try {
			// Replace http://Swap:7200 with appropriate GraphDB remote repository URL
			RepositoryManager repositoryManager = new RemoteRepositoryManager("http://Swap:7200");
			repositoryManager.init();
			// Replace cfha-repository with created graphDB repository name
			Repository repository = repositoryManager.getRepository("cfha-repository");
			RepositoryConnection repositoryConnection = repository.getConnection();

			HashMap<String, Object> graphMap = new HashMap<>();
			List<HashMap<String, Object>> nodeList = new ArrayList<>();
			List<HashMap<String, Object>> edgeList = new ArrayList<>();

			String rdfNameSpace = "http://www.w3.org/1999/02/22-rdf-syntax-ns#";
			String rdfsNameSpace = "http://www.w3.org/2000/01/rdf-schema#";
			String owlNameSpace = "http://www.w3.org/2002/07/owl#";
			String queryStringForPerson = "PREFIX CfHA: <http://www.semanticweb.org/ontologies/2022/1/CfHA#> \n";
			queryStringForPerson += "PREFIX rdf: <"+rdfNameSpace+"> \n";
			queryStringForPerson += "PREFIX rdfs: <"+rdfsNameSpace+"> \n";
			queryStringForPerson += "PREFIX owl: <"+owlNameSpace+"> \n";
			queryStringForPerson += "SELECT ?s ?slab ?p ?plab ?o ?olab \n";
			queryStringForPerson += "WHERE { \n";
			queryStringForPerson += "    ?s ?p ?o ; \n";
			queryStringForPerson += "    rdf:type CfHA:Person . \n";
			queryStringForPerson += "    OPTIONAL{?s rdfs:label ?slab} \n";
			queryStringForPerson += "    OPTIONAL{?p rdfs:label ?plab} \n";
			queryStringForPerson += "    OPTIONAL{?o rdfs:label ?olab} \n";
			if (name != null && !name.isEmpty())
				queryStringForPerson += "    FILTER regex(lcase(STR(?slab)), \"" + name.toLowerCase() + "\") \n";
			if (group != null && !group.isEmpty())
				queryStringForPerson += "    FILTER regex(lcase(STR(?o)), \"" + group.toLowerCase() + "\") \n";
			if (affiliation != null && !affiliation.isEmpty())
				queryStringForPerson += "    FILTER regex(lcase(STR(?p)), \"" + affiliation.toLowerCase() + "\") \n";
			if (object != null && !object.isEmpty())
				queryStringForPerson += "    FILTER regex(lcase(STR(?olab)), \"" + object.toLowerCase() + "\") \n";
			if (project != null && !project.isEmpty())
				queryStringForPerson += "    FILTER regex(lcase(STR(?olab)), \"" + project.toLowerCase() + "\") \n";
			if (mission != null && !mission.isEmpty())
				queryStringForPerson += "    FILTER regex(lcase(STR(?olab)), \"" + mission.toLowerCase() + "\") \n";
			if (topic != null && !topic.isEmpty())
				queryStringForPerson += "    FILTER regex(lcase(STR(?olab)), \"" + topic.toLowerCase() + "\") \n";
			queryStringForPerson += "    FILTER (?p != owl:topObjectProperty && ?p != owl:topDataProperty && ?o != owl:NamedIndividual && ?p != rdfs:label) \n";
			queryStringForPerson += "} LIMIT 30 \n";

			TupleQuery queryForPerson = repositoryConnection.prepareTupleQuery(queryStringForPerson);
			try (TupleQueryResult result = queryForPerson.evaluate()) {
				for (BindingSet solution : result) {
					HashMap<String, Object> nodesMap = new HashMap<>();
					nodesMap.put("id", solution.getValue("s").stringValue());
					nodesMap.put("label", solution.getValue("slab")== null?solution.getValue("s")
							:solution.getValue("slab").stringValue());
					nodeList.add(nodesMap);
					nodesMap = new HashMap<>();
					nodesMap.put("id", solution.getValue("o").stringValue());
					nodesMap.put("label", solution.getValue("olab")== null?solution.getValue("o").stringValue().replace(owlNameSpace,"")
							:solution.getValue("olab").stringValue());
					nodeList.add(nodesMap);

					HashMap<String, Object> edgesMap = new HashMap<>();
					edgesMap.put("source", solution.getValue("s").stringValue());
					edgesMap.put("target", solution.getValue("o").stringValue());
					edgesMap.put("label", solution.getValue("plab")== null?solution.getValue("p").stringValue().replace(rdfNameSpace, "").replace(rdfsNameSpace,"")
							:solution.getValue("plab").stringValue());
					edgeList.add(edgesMap);
				}
			}
			
			graphMap.put("nodes", nodeList);
			graphMap.put("edges", edgeList);

			repositoryConnection.close();
			repository.shutDown();
			repositoryManager.shutDown();
			return graphMap;
		} catch (Throwable t) {
			logger.error(WTF_MARKER, t.getMessage(), t);
		}
		return null;
	}

	public static void writePerson(String name, String givenName, String familyName) {
		try {
			// Replace http://Swap:7200 with appropriate GraphDB remote repository URL
			RepositoryManager repositoryManager = new RemoteRepositoryManager("http://Swap:7200");
			repositoryManager.init();
			// Replace cfha-repository with created graphDB repository name
			Repository repository = repositoryManager.getRepository("cfha-repository");
			RepositoryConnection repositoryConnection = repository.getConnection();

			String queryStringForPerson = "PREFIX CfHA: <http://www.semanticweb.org/ontologies/2022/1/CfHA#> \n";
			queryStringForPerson += "PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> \n";
			queryStringForPerson += "PREFIX owl: <http://www.w3.org/2002/07/owl#> \n";
			queryStringForPerson += "PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> \n";
			queryStringForPerson += "INSERT DATA { \n";
			queryStringForPerson += "    CfHA:" + name + " rdf:type CfHA:Person ; \n";
			queryStringForPerson += "    rdf:type owl:NamedIndividual ; \n";
			queryStringForPerson += "    rdfs:label \"" + givenName + " " + familyName + "\" ; \n";
			queryStringForPerson += "    CfHA:givenName \"" + givenName + "\" ; \n";
			queryStringForPerson += "    CfHA:familyName \"" + familyName + "\" . \n";
			queryStringForPerson += "} \n";

			Update updateOperation = repositoryConnection.prepareUpdate(QueryLanguage.SPARQL, queryStringForPerson);
			updateOperation.execute();

			repositoryConnection.close();
			repository.shutDown();
			repositoryManager.shutDown();
		} catch (Throwable t) {
			logger.error(WTF_MARKER, t.getMessage(), t);
		}
	}

	public static void writeTriples(String subject, String predicate, String object) {
		try {
			// Replace http://Swap:7200 with appropriate GraphDB remote repository URL
			RepositoryManager repositoryManager = new RemoteRepositoryManager("http://Swap:7200");
			repositoryManager.init();
			// Replace cfha-repository with created graphDB repository name
			Repository repository = repositoryManager.getRepository("cfha-repository");
			RepositoryConnection repositoryConnection = repository.getConnection();

			writePerson(subject.replace(" ",""), subject.split(" ")[0], subject.split(" ")[1]);
			String queryStringForPerson = "PREFIX CfHA: <http://www.semanticweb.org/ontologies/2022/1/CfHA#> \n";
			queryStringForPerson += "INSERT DATA { \n";
			queryStringForPerson += "    CfHA:" + subject.replace(" ","") + " CfHA:" + predicate + " CfHA:"  + object + ". \n";
			queryStringForPerson += "} \n";

			Update updateOperation = repositoryConnection.prepareUpdate(QueryLanguage.SPARQL, queryStringForPerson);
			updateOperation.execute();

			repositoryConnection.close();
			repository.shutDown();
			repositoryManager.shutDown();
		} catch (Throwable t) {
			logger.error(WTF_MARKER, t.getMessage(), t);
		}
	}
}
