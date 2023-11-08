Feature: As a user I want to update one of my todo list with a new done Status

  Background: RestAPI is running and available
    Given I am currently navigated to the rest API todo list manager
    And I know the ID of the pre-existing todo items inside the API

  Scenario: As a user I want to update a todo item with a new done status True (Normal Flow)
    When I send a POST request "/todo/id" with the ID of the todo item and the new done status- True
    Then I get the todo item title as it was for that todo item
    And I get the todo item description as it was for that todo item
    And I get back the todo item status as the updated version - True
    And I shutdown the rest API todo list manager

  Scenario: As a user I want to update a todo item with a new done status False and description Final Exam (Alternate Flow)
    When I send a POST request "/todo/id" with the ID of the todo item, the new done status- False and the new description- Final Exam
    Then I get the todo item title as it was for that todo item initially
    And I get the todo item description as Final Exam for that todo item
    And I get back the todo item status as the updated version - False
    And I shutdown the rest API todo list manager

  Scenario: As a user I want to update a todo item with a new done Status as a string In Progress (Error Flow)
    When I send a POST request "/todo/id" with the ID of the todo item and the new done status - InProgress
    Then I get back an error message - Failed Validation: doneStatus should be BOOLEAN
    And I shutdown the rest API todo list manager
