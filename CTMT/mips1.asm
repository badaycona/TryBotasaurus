    bne  $s0, $s1, else_branch
    add  $s2, $t0, $t1
    j    exit_if

else_branch:
    sub  $s2, $t0, $t1

exit_if: