#----------------------------------------------------------------
# Generated CMake target import file for configuration "Release".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "LuPNT::LuPNT" for configuration "Release"
set_property(TARGET LuPNT::LuPNT APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(LuPNT::LuPNT PROPERTIES
  IMPORTED_LINK_INTERFACE_LANGUAGES_RELEASE "CXX"
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib64/LuPNT/libLuPNT.a"
  )

list(APPEND _cmake_import_check_targets LuPNT::LuPNT )
list(APPEND _cmake_import_check_files_for_LuPNT::LuPNT "${_IMPORT_PREFIX}/lib64/LuPNT/libLuPNT.a" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
