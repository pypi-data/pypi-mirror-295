cmake_minimum_required(VERSION 3.0)

project(wdotoold VERSION 0.1 LANGUAGES CXX)

set(BIN_NAME wdotoold)

set(CMAKE_CXX_STANDARD 11)
set(CMAKE_INCLUDE_CURRENT_DIR ON)
set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTORCC ON)
set(CMAKE_CXX_FLAGS "-g -Wall")


find_package(Qt5 COMPONENTS Core Gui Widgets DBus Concurrent Network REQUIRED)
find_package(KF5Wayland REQUIRED)

set(Qt_LIBS
    Qt5::Core
    Qt5::Gui
    Qt5::Widgets
    Qt5::DBus
    Qt5::Concurrent
    Qt5::Network
)
set(SOURCE_FILES
        cli/main.cpp
        cli/datastruct.h
        cli/input.h
        cli/input.cpp
        cli/tcpserver.h
        cli/tcpserver.cpp
        cli/config.h
        cli/config.cpp
        )
add_executable(${BIN_NAME}
    ${SOURCE_FILES}
)

set_target_properties(${BIN_NAME}
        PROPERTIES
        CXX_STANDARD 11
        CXX_STANDARD_REQUIRED ON
        CXX_EXTENSIONS ON
)

target_link_libraries(${BIN_NAME}
        ${Qt_LIBS}
)

target_link_libraries(${BIN_NAME} KF5::WaylandClient)

INSTALL(TARGETS ${BIN_NAME} DESTINATION bin)
