cmake_minimum_required(VERSION 3.16)
project(mm_filters)

include(GNUInstallDirs)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

find_package(Python COMPONENTS Interpreter Development.Module REQUIRED)

# module target
add_library(mmces_filters SHARED 
            bindings.cpp
            filter0.cpp
            filter1.cpp
            filter2.cpp
            Hungarian.cpp)

set_target_properties(mmces_filters PROPERTIES 
    PREFIX ""
    BUILD_RPATH "$ORIGIN/rdkit.libs"
    INSTALL_RPATH "$ORIGIN/rdkit.libs"
)

if(WIN32)
    set_target_properties(mmces_filters PROPERTIES SUFFIX ".pyd")
elseif(APPLE)
    set_target_properties(mmces_filters PROPERTIES SUFFIX ".so")
endif()

#cmake_policy(SET CMP0167 NEW)

set(RDKIT_LIB_DIR "$ENV{RDKIT_LIB_DIR}")
set(RDKIT_INCLUDE_DIR "$ENV{RDKIT_INCLUDE_DIR}")
set(RDKIT_BUILD_INCLUDE_DIR "$ENV{RDKIT_BUILD_INCLUDE_DIR}")

message(STATUS "RDKit lib directory: ${RDKIT_LIB_DIR}")
message(STATUS "RDKit include directory: ${RDKIT_INCLUDE_DIR}")
message(STATUS "RDKit build include directory: ${RDKIT_BUILD_INCLUDE_DIR}")

if(WIN32)
    file(GLOB RDKIT_GRAPHMOL_LIBRARY "${RDKIT_LIB_DIR}/RDKitGraphMol*.lib")
    file(GLOB RDKIT_DATASTRUCTS_LIBRARY "${RDKIT_LIB_DIR}/RDKitDataStructs*.lib")
    file(GLOB RDKIT_SMILESPARSE_LIBRARY "${RDKIT_LIB_DIR}/RDKitSmilesParse*.lib")
    file(GLOB BOOST_RDKIT_LIBRARY "${RDKIT_LIB_DIR}/libboost_python*.lib")
else()
    file(GLOB BOOST_RDKIT_LIBRARY "${RDKIT_LIB_DIR}/libboost_python*.so*")
    file(GLOB RDKIT_GRAPHMOL_LIBRARY "${RDKIT_LIB_DIR}/libRDKitGraphMol*")
    file(GLOB RDKIT_DATASTRUCTS_LIBRARY "${RDKIT_LIB_DIR}/libRDKitDataStructs*")
    file(GLOB RDKIT_SMILESPARSE_LIBRARY "${RDKIT_LIB_DIR}/libRDKitSmilesParse*")     
endif()

if(BOOST_RDKIT_LIBRARY)
    list(GET BOOST_RDKIT_LIBRARY 0 BOOST_RDKIT_LIBRARY)
endif()

message(STATUS "Conda Dir: $ENV{CONDA_PREFIX}")
message(STATUS "Boost.Python: ${BOOST_RDKIT_LIBRARY}")
message(STATUS "RDKit graphmol: ${RDKIT_GRAPHMOL_LIBRARY}")
message(STATUS "RDKit datastructs: ${RDKIT_DATASTRUCTS_LIBRARY}")
message(STATUS "RDKit smilesparse: ${RDKIT_SMILESPARSE_LIBRARY}")

if (NOT MSVC)
    target_compile_options(mmces_filters PRIVATE
        -U_GLIBCXX_USE_CXX11_ABI 
        -D_GLIBCXX_USE_CXX11_ABI=0
    )
endif()

target_include_directories(mmces_filters PRIVATE
    "${RDKIT_INCLUDE_DIR}"
    "${RDKIT_BUILD_INCLUDE_DIR}"
    "${RDKIT_LIB_DIR}"
    "$ENV{CONDA_PREFIX}/include"
    "$ENV{BOOST_INCLUDE_DIR}"
)

target_link_directories(mmces_filters PRIVATE
    "${RDKIT_LIB_DIR}"
)

target_link_libraries(mmces_filters PRIVATE
    "${BOOST_RDKIT_LIBRARY}"
    Python::Module
    "${RDKIT_DATASTRUCTS_LIBRARY}"
    "${RDKIT_GRAPHMOL_LIBRARY}"
    "${RDKIT_SMILESPARSE_LIBRARY}"
)

# makes sure compiled .so file is in correct place for python wheel
install(TARGETS mmces_filters DESTINATION .)
