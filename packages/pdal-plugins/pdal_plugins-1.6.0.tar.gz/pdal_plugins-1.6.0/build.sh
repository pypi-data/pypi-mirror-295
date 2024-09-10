#!/bin/bash
#
#rm -rf _skbuild
#find . |grep '__pycache*'|xargs rm -rf
#rm -rf python_pdal.egg-info
#rm -rf pdal/*.dylib


#SKBUILD_CONFIGURE_OPTIONS="-DWITH_TESTS=ON -DCMAKE_BUILD_TYPE=Debug " python setup.py develop
#codesign --force -s - ./pdal/libpdal_plugin_filter_python.dylib
#codesign --force -s - ./pdal/libpdal_plugin_reader_numpy.dylib
#
rm -rf build && python -m pip install -Cbuild-dir=build -v  -Ccmake.define.WITH_TESTS=ON . --config-settings=cmake.build-type="Debug"   -vv --no-deps --no-build-isolation

