project (client)

# Tools
include (platform/nk)

# Project header
project_header_default ("STRICT_WARNINGS:NO")

nk_build_edl_files (client_edl_files NK_MODULE "client" EDL "${CMAKE_SOURCE_DIR}/resources/edl/Client.edl")


message(STATUS "foo include dir: ${CMAKE_CURRENT_SOURCE_DIR}")

#${CMAKE_CURRENT_SOURCE_DIR}
include_directories(${CMAKE_CURRENT_SOURCE_DIR}/src/rapidjson/include)

add_executable (Client "src/robot.cpp")
add_dependencies (Client client_edl_files)
target_link_libraries (Client ${gpio_CLIENT_LIB})

if ("${CMAKE_SYSTEM_PROCESSOR}" MATCHES "arm")
    target_link_libraries (Client ${bsp_CLIENT_LIB})
endif ()
