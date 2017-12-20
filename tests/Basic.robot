*** Settings ***
Library  SeleniumLibrary
Resource  Resources/Common.robot
Resource  Resources/Pages/Login.robot
Suite Setup  Open Website  ${URL}
Suite Teardown  Close Browser

*** Variables ***
${URL}  http://nthienan.com.s3-website-us-east-1.amazonaws.com
${LOGIN_URL}  http://nthienan.com.s3-website-us-east-1.amazonaws.com/#/login
${USERNAME}  an@it.com
${PASSWORD}  123456

*** Test Cases ***
Have login form
    Page Should Contain Element  id=loginForm  limit=1

Valid login
    Go To   ${LOGIN_URL}
    Submit Userame  ${USERNAME}
    Submit Password  ${PASSWORD}
    Submit Credentials
    Verify Home Page Should Be Opened


