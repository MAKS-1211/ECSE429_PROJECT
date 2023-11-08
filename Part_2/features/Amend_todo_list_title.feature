Feature: As a user I want to change the title of one of my todo list items

  Background: RestAPI is running and available
    Given I am currently navigated to the rest API todo list manager
    And I know the ID of the pre-existing todo items inside the API

  Scenario: As a user I want to update a todo item with a new title ECSE 206 (Normal Flow)
    When I send a POST request "/todo/id" with the ID of the todo item and the new title- ECSE 206
    Then I get the todo item title as ECSE 206 for that todo item
    And I get the todo item description as it was for that todo item
    And I get back the todo item status as it was for that todo item
    And I shutdown the rest API todo list manager


  Scenario: As a user I want to update a todo item with a new title ECSE 331 and description Mid Term 2 (Alternate Flow)
    When I send a POST request "/todo/id" with the ID of the todo item, the new title- ECSE 331 and the new description- Mid Term 2
    Then I get the todo item title as ECSE 331 for that todo item
    And I get the todo item description as Mid Term 2 for that todo item
    And I get back the todo item status as it was for that todo item initially
    And I shutdown the rest API todo list manager

  Scenario: As a user I want to update a todo item with a blank title (Error Flow)
    When I send a POST request "/todo/id" with the ID of the todo item and the new title as blank
    Then I get back an error message - Failed Validation: title : can not be empty
    And I shutdown the rest API todo list manager

