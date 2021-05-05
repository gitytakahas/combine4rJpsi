#g++ -c -fPIC foo.cpp -o foo.o
#g++ -shared -Wl,-soname,libfoo.so -o libfoo.so  foo.o


#root -l <<EOF

#.L foo.cpp+g

#EOF


#
root -l <<EOF

.L fakefactor.C+g

EOF

root -l <<EOF

.L fakeRate.C+g

EOF

root -l <<EOF

.L zptweight.C+g

EOF


root -l <<EOF

.L functionmacro.C+g

EOF
