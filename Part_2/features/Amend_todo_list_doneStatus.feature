Feature: As a user I want to update one of my todo list with a new done Status

  Background: RestAPI is running and available
    Given I am currently navigated to the rest API todo list manager
    And I know the ID of the pre-existing todo items inside the API

  Scenario Outline: As a user I want to update a todo item with a new done status True (Normal Flow)
    When I send a POST request "/todo/id" with the ID of the todo item and the new done status- True
    Then I get the todo item title <title> as it was for that todo item
    And I get the todo item description <description>, as it was for that todo item
    And I get back the todo item status as the updated version - True
    And I shutdown the rest API todo list manager
    Examples:
      | title | description |
      | ECSE 429| Project Part B |
      | ECSE 427|  Assignment 2  |

  Scenario Outline: As a user I want to update a todo item with a new done status False and description Final Exam (Alternate Flow)
    When I send a POST request "/todo/id" with the ID of the todo item, the new done status- False and the new description- <description>
    Then I get the todo item title <title> as it was for that todo item initially
    And I get the todo item descriptions as <description> for that todo item.
    And I get back the todo item status as the updated version - False
    And I shutdown the rest API todo list manager
    Examples:
      | description | title |
      | Project Part B | ECSE 429 |
      | Assignment 2  | ECSE 427|

  Scenario Outline: As a user I want to update a todo item with a new done Status as a non boolean Status (Error Flow)
    When I send a POST request "/todo/id" with the ID of the todo item and the new done status - <doneStatus>
    Then I get back an error message - Failed Validation: doneStatus should be BOOLEAN
    And I shutdown the rest API todo list manager
    Examples:
      | doneStatus |
      | InProgress |
      | Almost     |
