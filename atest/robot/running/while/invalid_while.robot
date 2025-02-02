*** Settings ***
Resource          while.resource
Suite Setup       Run Tests    --log test_result_model_as_well    running/while/invalid_while.robot

*** Test Cases ***
Multiple conditions
    ${tc} =   Check Invalid WHILE Test Case
    Should Be Equal    ${tc[0].condition}    Too, many, conditions, !

Invalid condition
    Check Invalid WHILE Test Case

Non-existing ${variable} in condition
    Check Invalid WHILE Test Case

Non-existing $variable in condition
    Check Invalid WHILE Test Case

Recommend $var syntax if invalid condition contains ${var}
    Check Test Case    ${TEST NAME}

Invalid condition on second round
    Check Test Case    ${TEST NAME}

No body
    Check Invalid WHILE Test Case    body=False

No END
    Check Invalid WHILE Test Case

Invalid data causes syntax error
    Check Test Case    ${TEST NAME}

Invalid condition causes normal error
    Check Test Case    ${TEST NAME}

Non-existing variable in condition causes normal error
    Check Test Case    ${TEST NAME}

Templatest are not supported
    ${tc} =    Check Test Case    ${TEST NAME}
    Should Be Equal       ${tc[0].type}         WHILE
    Should Be Equal       ${tc[0].status}       FAIL
    Should Be Equal       ${tc[0, 0].type}      ITERATION
    Should Be Equal       ${tc[0, 0].status}    NOT RUN
    Check Keyword Data    ${tc[0, 0, 0]}        ${EMPTY}    args=1    status=NOT RUN
    Check Keyword Data    ${tc[0, 0, 1]}        ${EMPTY}    args=2    status=NOT RUN

*** Keywords ***
Check Invalid WHILE Test Case
    [Arguments]    ${body}=True
    ${tc} =    Check Test Case    ${TESTNAME}
    Should Be Equal    ${tc[0].type}         WHILE
    Should Be Equal    ${tc[0].status}       FAIL
    Should Be Equal    ${tc[0, 0].type}      ITERATION
    Should Be Equal    ${tc[0, 0].status}    NOT RUN
    IF    ${body}
        Should Be Equal    ${tc[0, 0, 0].full_name}      BuiltIn.Fail
        Should Be Equal    ${tc[0, 0, 0].status}         NOT RUN
    END
    RETURN    ${tc}
