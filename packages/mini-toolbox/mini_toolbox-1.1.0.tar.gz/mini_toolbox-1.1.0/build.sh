#!/bin/bash
# @File: build.sh
# @Date: 2024-03-19 11:30:42
# @Desc: 项目打包脚本

TOP_DIR=$(cd `dirname $0`; pwd); cd ${TOP_DIR}
set -x -e

deal_ver(){
    set +x
    ver_old=$(sed -n '/version = /p' pyproject.toml | awk -F "'" '{print $2}')
    x=$(echo $ver_old | awk -F'.' '{print $1}')
    y=$(echo $ver_old | awk -F'.' '{print $2}')
    z=$(echo $ver_old | awk -F'.' '{print $3}')
    
    echo "Now: $ver_old"
    case $1 in
        'x') x=$[x+1]; y=0; z=0 ;;
        'y') y=$[y+1]; z=0 ;;
        'z') z=$[z+1] ;;
        '*') : ;;
    esac
    
    ver_new="$x.$y.$z"
    
    if [ "$ver_old"x != "$ver_new"x ]; then
        echo "New: $ver_new"
        sed -i "s/version = .*$/version = '$ver_new'/g" pyproject.toml
        sed -i "s/release = .*$/release = '$ver_new'/g" docs/source/conf.py
    fi
    set -x
}

make_docs(){
    rm -rf docs/build
    rm -f docs/source/modules.rst docs/source/mini_toolbox.* docs/source/*.md
    
    cp -af README.md CHANGELOG.md docs/source/
    sphinx-apidoc -Mf -o docs/source mini_toolbox
    sed -i '/^Subpackages$/,//{/^Submodules$/!d}' docs/source/mini_toolbox.rst
    
    pushd docs
        make -i clean && make html
    popd
}

make_pkg(){
    rm -rf dist
    python3 -m build
}

# main
case "$1" in 
    'f'|'format')
        # 格式化代码, 并检查英文符号(,:;)
        yapf -ir --style "{based_on_style: google, column_limit: 120}" .
        grep -rn '[，：；]' . | grep -vE '(html|grep|Binary|Python迷你工具箱|功能描述详见)'
        ;;
    't'| 'test')
        # 执行单元测试
        pytest -v
        ;;
    'p'|'publish'|'pypi')
        # 发布至pypi
        python3 -m twine upload --repository pypi dist/*
        ;;
    'd'|'doc'|'docs'|'w'|'web')
        # 编译文档并本地预览
        make_docs
        cd docs/build/html; python3 -m http.server 6605
        ;;
    'x'|'y'|'z')
        # 版本迭代及编译
        deal_ver "$1"
        make_docs
        make_pkg
        ;;
    *)
        # 编译
        make_docs
        make_pkg
        ;;
esac
