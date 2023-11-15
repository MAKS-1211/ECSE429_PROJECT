Feature: As a user I want to create a new todo list item with a specific description in mind

  Background: RestAPI is running and available
    Given I am currently navigated to the rest API todo list manager
    And I am currently working with a rest API that has no todo entries

  Scenario Outline: As a user I want to create a new todo item with a description, title and done Status  (Normal Flow)
    When I send a POST request "/todos" of the todo item with a description <description>, doneStatus <doneStatus> and Title as <title>
    Then I get back my todo item with a new todo item ID
    And I get back my todo item with the same description as <description>
    And I get back my todo item with the same Title as <title>
    And I get back my todo item with the doneStatus as <doneStatus>.
    And I shutdown the rest API todo list manager
    Examples:
      | description | doneStatus | title |
      | Project Part B| True     | ECSE 429|
      | Assignment 2  | False    | ECSE 427|

  Scenario Outline: As a user I want to create a new todo item with a description and title (Alternate Flow)
    When I send a POST request "/todos" of the todo item with a description <description> and Title as <title>
    Then I get back my todo item with a new todo item ID as above
    And I get back my todo item with the same description <description>
    And I get back my todo item with the same Title <title>
    And I shutdown the rest API todo list manager
    Examples:
      | description | title |
      | Project Part B| ECSE 429|
      | Assignment 2  | ECSE 427|

  Scenario Outline: As a user I want to create a new todo item with just a description (Error Flow)
    When I send a POST request "/todos" of the todo item with a description <description>
    Then I get back an error message: 'title : field is mandatory'
    And I shutdown the rest API todo list manager
    Examples:
      | description |
      | Project Part B|
      | Assignment 2  |
