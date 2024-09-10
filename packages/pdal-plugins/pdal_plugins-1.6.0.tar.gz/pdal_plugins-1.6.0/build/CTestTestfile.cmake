# CMake generated Testfile for 
# Source directory: /Users/hobu/dev/git/pdal-python-plugins
# Build directory: /Users/hobu/dev/git/pdal-python-plugins/build
# 
# This file includes the relevant testing commands required for 
# testing this directory and lists subdirectories to be tested as well.
add_test(pdal_io_numpy_test "/Users/hobu/dev/git/pdal-python-plugins/build/bin/pdal_io_numpy_test")
set_tests_properties(pdal_io_numpy_test PROPERTIES  WORKING_DIRECTORY "/.." _BACKTRACE_TRIPLES "/Users/hobu/dev/git/pdal-python-plugins/CMakeLists.txt;149;add_test;/Users/hobu/dev/git/pdal-python-plugins/CMakeLists.txt;214;PDAL_PYTHON_ADD_TEST;/Users/hobu/dev/git/pdal-python-plugins/CMakeLists.txt;0;")
add_test(pdal_filters_python_test "/Users/hobu/dev/git/pdal-python-plugins/build/bin/pdal_filters_python_test")
set_tests_properties(pdal_filters_python_test PROPERTIES  WORKING_DIRECTORY "/.." _BACKTRACE_TRIPLES "/Users/hobu/dev/git/pdal-python-plugins/CMakeLists.txt;149;add_test;/Users/hobu/dev/git/pdal-python-plugins/CMakeLists.txt;232;PDAL_PYTHON_ADD_TEST;/Users/hobu/dev/git/pdal-python-plugins/CMakeLists.txt;0;")
subdirs("src/pdal/test/gtest")
