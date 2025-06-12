    li   $s2, 0
    li   $s0, 1

loop:
    bgt  $s0, $s1, end_loop
    add  $s2, $s2, $s0
    addi $s0, $s0, 1
    j    loop
    
end_loop: