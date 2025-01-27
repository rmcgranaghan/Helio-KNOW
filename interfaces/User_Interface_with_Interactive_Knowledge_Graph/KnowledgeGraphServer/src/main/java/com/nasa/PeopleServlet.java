package com.nasa;

import java.io.IOException;
import java.util.HashMap;
import java.util.List;

import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import com.fasterxml.jackson.databind.ObjectMapper;

/**
 * Servlet implementation class PeopleServlet
 */
@WebServlet("/peopleServlet/*")
public class PeopleServlet extends HttpServlet {
	private static final long serialVersionUID = 1L;
       
    /**
     * @see HttpServlet#HttpServlet()
     */
    public PeopleServlet() {
        super();
        // TODO Auto-generated constructor stub
    }

	/**
	 * @see HttpServlet#doGet(HttpServletRequest request, HttpServletResponse response)
	 */
	protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
		String name = request.getParameter("name");
		List<HashMap<String, Object>> personProfileMap = RemoteRepository.getPersonProfile(name);
		ObjectMapper objectMapper = new ObjectMapper();
		String json = objectMapper.writeValueAsString(personProfileMap);
		response.setContentType("text/html; charset=UTF-8");
		response.setCharacterEncoding("UTF-8");
		response.getOutputStream().write(json.toString().getBytes("UTF-8"));
	}

	/**
	 * @see HttpServlet#doPost(HttpServletRequest request, HttpServletResponse response)
	 */
	protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
		/* 
		String name = request.getParameter("name");
		String givenName = request.getParameter("givenName");
		String FamilyName = request.getParameter("FamilyName");
		
		RemoteRepository.writePerson(name, givenName, FamilyName);
		*/
	         
		String subject = request.getParameter("subject");
		String predicate = request.getParameter("predicate");
		String object = request.getParameter("object");
		
		RemoteRepository.writeTriples(subject, predicate, object);
	}

}
