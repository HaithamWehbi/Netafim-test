Feature: User Registration

  @sanity
  Scenario: Successful User Registration and Delete Account
    Given launch the browser
    When I navigate to website homepage "http://automationexercise.com"
    Then verify that homepage is displayed
    When clicking on sign up button
    Then verify New User sign is displayed
    When entering a name and email "test1" "em@t5.au"
    And click signup button
    Then verify that Enter Account Info is displayed
    When filling details: "mr", "name", "password", "5/5/1998"
    And select sign up checkbox
    And select receive offers
    And filling more details: "last_name", "first_name", "company", "address", "address2", "Canada", "state", "city", "zipcode", "number"
    And clicking on create account button
    Then verify that Account Created is visible
    When click on continue button
    Then verify that Logged In As Username is visible
    When click delete account button
    Then verify Account Deleted is visible and click Continue button
