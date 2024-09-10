#----------------------------------------------------------------
# Generated CMake target import file for configuration "Release".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "incstats" for configuration "Release"
set_property(TARGET incstats APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(incstats PROPERTIES
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/libincstats.dylib"
  IMPORTED_SONAME_RELEASE "@rpath/libincstats.dylib"
  )

list(APPEND _cmake_import_check_targets incstats )
list(APPEND _cmake_import_check_files_for_incstats "${_IMPORT_PREFIX}/lib/libincstats.dylib" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
