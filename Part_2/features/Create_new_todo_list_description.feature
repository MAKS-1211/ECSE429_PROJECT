Feature: As a user I want to create a new todo list item with a specific description in mind

  Background: RestAPI is running and available
    Given I am currently navigated to the rest API todo list manager
    And I am currently working with a rest API that has no todo entries

  Scenario: As a user I want to create a new todo item with a description, title and done Status  (Normal Flow)
    When I send a POST request "/todos" of the todo item with a description 'Project Part B', doneStatus True and Title as 'ECSE 429'
    Then I get back my todo item with a new todo item ID
    And I get back my todo item with the same description
    And I get back my todo item with the same Title
    And I get back my todo item with the doneStatus as True
    And I shutdown the rest API todo list manager

  Scenario: As a user I want to create a new todo item with a description and title (Alternate Flow)
    When I send a POST request "/todos" of the todo item with a description 'Assignment 2' and Title as 'ECSE 427'
    Then I get back my todo item with a new todo item ID as above
    And I get back my todo item with the same description as above
    And I get back my todo item with the same Title as above
    And I shutdown the rest API todo list manager

  Scenario: As a user I want to create a new todo item with just a description (Error Flow)
    When I send a POST request "/todos" of the todo item with a description 'McGill ECSE'
    Then I get back an error message: 'title : field is mandatory'
    And I shutdown the rest API todo list manager