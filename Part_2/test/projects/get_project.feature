@Story
  Feature: The user wants to retrieve an exising project using Get

    Background: The API is already running on the user's system and has no entries
      Given the API is running
      And the API has no project entries

    # Normal Flow
    Scenario Outline: User wants to retrieve an existing project by using its id
      Given An already existing project with a title <tit>, a description <desc>, an active status <act> and a completed status <comp>
      When The user tries to get the project using its id
      Then The user receives an OK HTTP status code (200)
      And The user receives the existing project back in response

      Examples:
        | tit       | desc            | act   | comp  |
        | Project 1 | Python testing  | False | True  |
        | Project 2 | Gherkin testing | True  | False |


    # Alternate Flow
    Scenario Outline: User wants to retrieve an existing project by getting all projects and looking through them
      Given An already existing project with a title <tit>, a description <desc>, an active status <act> and a completed status <comp>
      When The user tries to get all existing projects in the database
      Then The user receives an OK HTTP status code (200)
      And The project will be in the collection of all projects that were returned

      Examples:
        | tit       | desc            | act   | comp  |
        | Project 1 | Python testing  | False | True  |
        | Project 2 | Gherkin testing | True  | False |


    # Error Flow
    Scenario Outline: User wants to get a project by id from an empty database
      When The user tries to get the project using an id <id>
      Then The user will get a Not Found HTTP status code (404)
      And The user gets an error message <err>

    Examples:
      | id | err |
      | 2  | Could not find an instance with projects/2  |
      | 47 | Could not find an instance with projects/47 |

