package com.nasa;

import java.io.IOException;
import java.util.HashMap;

import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import com.fasterxml.jackson.databind.ObjectMapper;

/**
 * Servlet implementation class KGServlet
 */
@WebServlet("/kgServlet/*")
public class KGServlet extends HttpServlet {
	private static final long serialVersionUID = 1L;
       
    /**
     * @see HttpServlet#HttpServlet()
     */
    public KGServlet() {
        super();
        // TODO Auto-generated constructor stub
    }

	/**
	 * @return 
	 * @see HttpServlet#doGet(HttpServletRequest request, HttpServletResponse response)
	 */
	protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
		String name = request.getParameter("name");
		String group = request.getParameter("group");
		String affiliation = request.getParameter("affiliation");
		String object = request.getParameter("object");
		String project = request.getParameter("project");
		String mission = request.getParameter("mission");
		String topic = request.getParameter("topic");
		HashMap<String, Object> graphMap = RemoteRepository.getAllPeople(name, group, affiliation, object, project, mission, topic);
		ObjectMapper objectMapper = new ObjectMapper();
		String json = objectMapper.writeValueAsString(graphMap);
		response.setContentType("text/html; charset=UTF-8");
		response.setCharacterEncoding("UTF-8");
		response.getOutputStream().write(json.toString().getBytes("UTF-8"));
	}

	/**
	 * @see HttpServlet#doPost(HttpServletRequest request, HttpServletResponse response)
	 */
	protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
		// TODO Auto-generated method stub
		doGet(request, response);
	}

}
