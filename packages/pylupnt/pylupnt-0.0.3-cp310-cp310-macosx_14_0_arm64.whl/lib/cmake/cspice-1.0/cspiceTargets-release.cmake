#----------------------------------------------------------------
# Generated CMake target import file for configuration "Release".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "cspice::cspice" for configuration "Release"
set_property(TARGET cspice::cspice APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(cspice::cspice PROPERTIES
  IMPORTED_LINK_INTERFACE_LANGUAGES_RELEASE "C"
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/cspice-1.0/libcspice.a"
  )

list(APPEND _cmake_import_check_targets cspice::cspice )
list(APPEND _cmake_import_check_files_for_cspice::cspice "${_IMPORT_PREFIX}/lib/cspice-1.0/libcspice.a" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
