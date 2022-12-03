project(day01)

add_executable(${PROJECT_NAME} main.cpp)

configure_file(
    sample_input.txt
    ${CMAKE_CURRENT_BINARY_DIR}/${CMAKE_BUILD_TYPE}/sample_input.txt
    COPYONLY
)

configure_file(
    input.txt
    ${CMAKE_CURRENT_BINARY_DIR}/${CMAKE_BUILD_TYPE}/input.txt
    COPYONLY
)