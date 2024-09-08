#! /usr/bin/env bash

function kamangir_action_git_before_push() {
    kamangir build_README

    [[ "$(abcli_git get_branch)" == "main" ]] &&
        kamangir pypi build
}
