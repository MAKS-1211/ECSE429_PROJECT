@Story
  Feature: The user wants to amend an exising project using a PUT call

    Background: The API is already running on the user's system and has no entries
      Given the API is running
      And the API has no project entries

    # Normal Flow
    Scenario Outline: User wants to amend all fields of an existing project in the database using a PUT call
      Given An already existing project with a title <tit>, a description <desc>, an active status <act> and a completed status <comp>
      When The user tries to amend the project with a new title <newtit>, a new description <newdesc>, a new active status <newact> and a new completed status <newcomp> using PUT
      Then The user receives an OK HTTP status code (200)
      And The user receives the project back in the response
      And The project will have its fields updated in the database

      Examples:
        | tit       | desc            | act   | comp  | newtit       | newdesc       | newact | newcomp |
        | Project 1 | Python testing  | False | True  | Project 1.1  | Java testing  | True   | False   |
        | Project 2 | Gherkin testing | True  | False | Project 2.1  | C++ testing   | False  | True    |


    # Alternate Flow
    Scenario Outline: User wants to amend no fields of an existing project in the database using a PUT call
      Given An already existing project with a title <tit>, a description <desc>, an active status <act> and a completed status <comp>
      When The user tries to amend the project with no fields declared using PUT
      Then The user receives an OK HTTP status code (200)
      And The user receives the existing project back in the response unchanged
      And The project will have its fields unchanged in the database

      Examples:
        | tit       | desc            | act   | comp  |
        | Project 1 | Python testing  | False | True  |
        | Project 2 | Gherkin testing | True  | False |


    # Error Flow
    Scenario Outline: User wants to amend the id of an existing project in the database using a PUT call
      Given An already existing project with a title <tit>, a description <desc>, an active status <act> and a completed status <comp>
      When The user tries to amend the project's id to <id> using PUT
      Then The user will get a Bad Request HTTP status code (400)
      And The project will have its fields unchanged in the database

      Examples:
        | tit       | desc            | act   | comp  | id |
        | Project 1 | Python testing  | False | True  | 2  |
        | Project 2 | Gherkin testing | True  | False | 47 |

