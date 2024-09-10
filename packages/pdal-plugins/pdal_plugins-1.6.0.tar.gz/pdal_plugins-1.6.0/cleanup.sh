rm -rf _skbuild
find . |grep '__pycache*'|xargs rm
rm -rf *.egg-info
rm *.whl
rm pdal/*.dylib

