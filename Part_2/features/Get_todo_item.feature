Feature: As a user I want to check on one of my todo items

  Background: RestAPI is running and available
    Given I am currently navigated to the rest API todo list manager
    And I know the ID of the pre-existing todo items inside the API

  Scenario Outline: As a user I want to get a specific single todo item through their integer todo ID (Normal Flow)
    When I send a GET request "/todo/id" with the ID <id> of the todo item I want
    Then I get the todo item title as <title> for that todo item
    And I get the todo item description as <description> for that todo item
    And I get back the todo item status as <doneStatus> for that todo item
    And I shutdown the rest API todo list manager
    Examples:
     | id | title | description | doneStatus |
     | 3 |ECSE 429| Project Part B | False |
     | 4 |ECSE 427| Assignment 2 | True |


  Scenario Outline: As a user I want to find my todo item from a list of all todo items (Alternate Flow)
    When I send a GET request "/todo" for all the items in the todo list
    Then I get back all the todo items
    And  I check for the todo item ID <id> I wanted
    And I get the todo item title as <title> for that todo item from the todo list
    And I get the todo item description as <description> for that todo item from the todo list
    And I get back the todo item status as <doneStatus> for that todo item from the todo list
    And I shutdown the rest API todo list manager
    Examples:
      | id | title | description | doneStatus |
      | 3 |ECSE 429| Project Part B | False |
      | 4 |ECSE 427| Assignment 2 | True |

    Scenario Outline: As a user I want to get a specific single todo item through their string todo ID (Error Flow)
      When I send a GET request "/todo/id" with the ID <id> of the todo item I want
      Then I get back an error message <message>
      And I shutdown the rest API todo list manager
      Examples:
        | id | message |
        | three | Could not find an instance with todos/three|
        | four | Could not find an instance with todos/four|


