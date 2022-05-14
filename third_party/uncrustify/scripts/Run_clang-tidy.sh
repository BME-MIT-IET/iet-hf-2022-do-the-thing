#!/bin/bash
#
# 2017-02-27
#
script_dir="$(dirname "$(readlink -f "$0")")"
#
SRC="${script_dir}/../src"
BUILD="${script_dir}/../build"
#
where=`pwd`
#
# build the lists
cd ${SRC}
list_of_C=`ls *.cpp`
list_of_H=`ls *.h`
list_of_files="${list_of_C} ${list_of_H}" 
cd ${where}
#
RESULTS="${script_dir}/../results"
#
rm -rf ${RESULTS}
mkdir ${RESULTS}
#
COMPILE_COMMANDS="compile_commands.json"
cp ${BUILD}/${COMPILE_COMMANDS} ${SRC}
#
# choise one of list of checks
list_of_Check="\
   boost-use-to-string\
   cert-dcl21-cpp\
   cert-dcl50-cpp\
   cert-dcl58-cpp\
   cert-env33-c\
   cert-err34-c\
   cert-err52-cpp\
   cert-err58-cpp\
   cert-err60-cpp\
   cert-flp30-c\
   cert-msc50-cpp\
   cppcoreguidelines-interfaces-global-init\
   cppcoreguidelines-no-malloc\
   cppcoreguidelines-pro-bounds-array-to-pointer-decay\
   cppcoreguidelines-pro-bounds-constant-array-index\
   cppcoreguidelines-pro-bounds-pointer-arithmetic\
   cppcoreguidelines-pro-type-const-cast\
   cppcoreguidelines-pro-type-cstyle-cast\
   cppcoreguidelines-pro-type-member-init\
   cppcoreguidelines-pro-type-reinterpret-cast\
   cppcoreguidelines-pro-type-static-cast-downcast\
   cppcoreguidelines-pro-type-union-access\
   cppcoreguidelines-pro-type-vararg\
   cppcoreguidelines-slicing\
   cppcoreguidelines-special-member-functions\
   google-build-explicit-make-pair\
   google-build-namespaces\
   google-build-using-namespace\
   google-default-arguments\
   google-explicit-constructor\
   google-global-names-in-headers\
   google-readability-casting\
   google-readability-todo\
   google-runtime-int\
   google-runtime-member-string-references\
   google-runtime-memset\
   google-runtime-operator\
   google-runtime-references\
   hicpp-explicit-conversions\
   hicpp-function-size\
   hicpp-invalid-access-moved\
   hicpp-member-init\
   hicpp-named-parameter\
   hicpp-new-delete-operators\
   hicpp-no-assembler\
   hicpp-noexcept-move\
   hicpp-special-member-functions\
   hicpp-undelegated-constructor\
   hicpp-use-equals-default\
   hicpp-use-equals-delete\
   hicpp-use-override\
   llvm-header-guard\
   llvm-include-order\
   llvm-namespace-comment\
   llvm-twine-local"
#list_of_Check="misc-argument-comment\
#   misc-assert-side-effect\
#   misc-bool-pointer-implicit-conversion\
#   misc-dangling-handle\
#   misc-definitions-in-headers\
#   misc-fold-init-type\
#   misc-forward-declaration-namespace\
#   misc-forwarding-reference-overload\
#   misc-inaccurate-erase\
#   misc-incorrect-roundings\
#   misc-inefficient-algorithm\
#   misc-macro-parentheses\
#   misc-macro-repeated-side-effects\
#   misc-misplaced-const\
#   misc-misplaced-widening-cast\
#   misc-move-const-arg\
#   misc-move-constructor-init\
#   misc-move-forwarding-reference\
#   misc-multiple-statement-macro\
#   misc-new-delete-overloads\
#   misc-noexcept-move-constructor\
#   misc-non-copyable-objects\
#   misc-redundant-expression\
#   misc-sizeof-container\
#   misc-sizeof-expression\
#   misc-static-assert\
#   misc-string-compare\
#   misc-string-constructor\
#   misc-string-integer-assignment\
#   misc-string-literal-with-embedded-nul\
#   misc-suspicious-enum-usage\
#   misc-suspicious-missing-comma\
#   misc-suspicious-semicolon\
#   misc-suspicious-string-compare\
#   misc-swapped-arguments\
#   misc-throw-by-value-catch-by-reference\
#   misc-unconventional-assign-operator\
#   misc-undelegated-constructor\
#   misc-uniqueptr-reset-release\
#   misc-unused-alias-decls\
#   misc-unused-parameters\
#   misc-unused-raii\
#   misc-unused-using-decls\
#   misc-use-after-move\
#   misc-virtual-near-miss"
#list_of_Check="modernize-avoid-bind\
#   modernize-deprecated-headers\
#   modernize-loop-convert\
#   modernize-make-shared\
#   modernize-make-unique\
#   modernize-pass-by-value\
#   modernize-raw-string-literal\
#   modernize-redundant-void-arg\
#   modernize-replace-auto-ptr\
#   modernize-replace-random-shuffle\
#   modernize-return-braced-init-list\
#   modernize-shrink-to-fit\
#   modernize-use-auto\
#   modernize-use-bool-literals\
#   modernize-use-default-member-init\
#   modernize-use-emplace\
#   modernize-use-equals-default\
#   modernize-use-equals-delete\
#   modernize-use-nullptr\
#   modernize-use-override\
#   modernize-use-transparent-functors\
#   modernize-use-using\
#   mpi-buffer-deref\
#   mpi-type-mismatch\
#   performance-faster-string-find\
#   performance-for-range-copy\
#   performance-implicit-cast-in-loop\
#   performance-inefficient-string-concatenation\
#   performance-inefficient-vector-operation\
#   performance-type-promotion-in-math-fn\
#   performance-unnecessary-copy-initialization\
#   performance-unnecessary-value-param"
#list_of_Check="readability-avoid-const-params-in-decls\
#   readability-braces-around-statements\
#   readability-container-size-empty\
#   readability-delete-null-pointer\
#   readability-deleted-default\
#   readability-else-after-return\
#   readability-function-size\
#   readability-identifier-naming\
#   readability-implicit-bool-cast\
#   readability-inconsistent-declaration-parameter-name\
#   readability-misleading-indentation\
#   readability-misplaced-array-index\
#   readability-named-parameter\
#   readability-non-const-parameter\
#   readability-redundant-control-flow\
#   readability-redundant-declaration\
#   readability-redundant-function-ptr-dereference\
#   readability-redundant-member-init\
#   readability-redundant-smartptr-get\
#   readability-redundant-string-cstr\
#   readability-redundant-string-init\
#   readability-simplify-boolean-expr\
#   readability-static-definition-in-anonymous-namespace\
#   readability-uniqueptr-delete-release"
#
for file in ${list_of_files}
do
  echo "test for "${file}
  OUTPUT="${RESULTS}/${file}.txt"
  for check in ${list_of_Check}
  do
    echo "  test for "${check}
    clang-tidy -checks="-*, ${check}" -header-filter="./${SRC}/*" ${SRC}/${file} \
      > ${OUTPUT} 2>/dev/null
    if [[ -s ${OUTPUT} ]]
    then
      head ${OUTPUT}
      break
    else
      rm -f ${OUTPUT}
    fi
  done
done
#
rm ${SRC}/${COMPILE_COMMANDS}
rmdir --ignore-fail-on-non-empty ${RESULTS}
if [[ -d ${RESULTS} ]]
then
  echo "some problem(s) are still present"
  exit 1
else
  echo "all clang-tidy are OK"
  exit 0
fi
