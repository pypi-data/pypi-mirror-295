include(CMakeFindDependencyMacro)

string(REGEX MATCHALL "[^;]+" SEPARATE_DEPENDENCIES "Eigen3 3.4;autodiff 1.1;cspice;Matplot++ 1.2;OpenMP;HighFive 2.10;Boost")

foreach(dependency ${SEPARATE_DEPENDENCIES})
  string(REPLACE " " ";" args "${dependency}")
  find_dependency(${args})
endforeach()

include("${CMAKE_CURRENT_LIST_DIR}/LuPNTTargets.cmake")
