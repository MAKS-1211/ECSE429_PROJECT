Feature: As a user I want to change the title of one of my todo list items

  Background: RestAPI is running and available
    Given I am currently navigated to the rest API todo list manager
    And I know the ID of the pre-existing todo items inside the API

  Scenario Outline: As a user I want to update a todo item with a new title (Normal Flow)
    When I send a POST request "/todo/id" with the ID of the todo item and the new title- <title>
    Then I get the todo item title as <title> for that todo item itself.
    And I get the todo item description <description>, as it was for that todo item
    And I get back the todo item status <doneStatus> as it was for that todo item
    And I shutdown the rest API todo list manager
    Examples:
      | title | description | doneStatus |
      | ECSE 429| Project Part B | True |
      | ECSE 427|  Assignment 2  | False |


  Scenario Outline: As a user I want to update a todo item with a new title and description (Alternate Flow)
    When I send a POST request "/todo/id" with the ID of the todo item, the new title- <title> and the new description- <description>
    Then I get the todo item title as <title> for that todo item.
    And I get the todo item description as <description> for that todo item.
    And I get back the todo item status <doneStatus> as it was for that todo item initially
    And I shutdown the rest API todo list manager
    Examples:
      | title | description | doneStatus |
      | ECSE 429| Project Part B | True |
      | ECSE 427|  Assignment 2  | False |

  Scenario: As a user I want to update a todo item with a blank title (Error Flow)
    When I send a POST request "/todo/id" with the ID of the todo item and the new title as blank
    Then I get back an error message - Failed Validation: title : can not be empty
    And I shutdown the rest API todo list manager

