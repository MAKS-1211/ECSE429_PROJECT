@Story
  Feature: The user has finished a project and wants the database to show that

    Background: The API is already running on the user's system and has no entries
      Given the API is running
      And the API has no project entries

    # Normal Flow
    Scenario Outline: The user wants to mark the project as done in the database
      Given An already existing project with a title <tit>, a description <desc>, an active status <act> and a completed status <comp>
      When The user marks the project as done by updating the active and completed status using a POST call
      Then The user receives an OK HTTP status code (200)
      And The user receives the updated project back in the response
      And The project will have its completed and active status updated in the database

      Examples:
        | tit       | desc            | act   | comp  |
        | Project 1 | Python testing  | True  | False |
        | Project 2 | Gherkin testing | True  | False |


    # Alternate Flow
    Scenario Outline: The user wants to delete the project from the database entirely
      Given An already existing project with a title <tit>, a description <desc>, an active status <act> and a completed status <comp>
      When The user marks the project as done by deleting it from the database
      Then The user receives an OK HTTP status code (200)
      And The project will no longer be in the database

      Examples:
        | tit       | desc            | act   | comp  |
        | Project 1 | Python testing  | True  | False |
        | Project 2 | Gherkin testing | True  | False |


    # Error Flow
    Scenario: The user wants to mark a project that has already been deleted as done
      Given An already existing project with a title <tit>, a description <desc>, an active status <act> and a completed status <comp>
      When The user marks the project as done by deleting it from the database
      And The user marks the project as done by updating the active and completed status using a POST call
      Then The user will get a Not Found HTTP status code (404)