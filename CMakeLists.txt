# Ensure FindPython3 supports NumPy and CMP0094
cmake_minimum_required(VERSION 3.15)

# Create main project.
project(pygotm VERSION 0.1.0 LANGUAGES Fortran C)

# Specify position-independent code since we will build a shared library.
set(CMAKE_POSITION_INDEPENDENT_CODE ON)

# Use solution folders in IDEs
set_property(GLOBAL PROPERTY USE_FOLDERS ON)

if (MSVC)
  add_compile_options(/libs:static)
endif()

# Find target Python interpreter.
find_package(Python3 COMPONENTS Interpreter Development NumPy)

add_subdirectory(extern/gotm gotm EXCLUDE_FROM_ALL)

add_library(cgotm
  src/pygotm_wrapper.F90)
target_link_libraries(cgotm turbulence util yaml)

add_custom_command(OUTPUT _pygotm.c
  COMMENT "Creating ${CMAKE_CURRENT_BINARY_DIR}/_pygotm.c from ${CMAKE_CURRENT_SOURCE_DIR}/_pygotm.pyx"
  COMMAND Python3::Interpreter -m cython "${CMAKE_CURRENT_SOURCE_DIR}/_pygotm.pyx" -o "${CMAKE_CURRENT_BINARY_DIR}/_pygotm.c"
  DEPENDS _pygotm.pyx
  VERBATIM
)

Python3_add_library(_pygotm MODULE
  "${CMAKE_CURRENT_BINARY_DIR}/_pygotm.c")
target_link_libraries(_pygotm PRIVATE cgotm Python3::NumPy)

install(TARGETS _pygotm DESTINATION .)
