#!/bin/bash

#swy-- set the ModuleSystem folder as the current directory ($PWD)
cd "$(dirname "$0")" || exit

# Who said that porting this behemoth to Warband was difficult? :)
export BUILD_TLD_WB=1
./build_module.sh
