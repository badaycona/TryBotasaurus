.data
    prompt1: .asciiz "Nhap so nguyen thu nhat: "
    prompt2: .asciiz "Nhap so nguyen thu hai: "
    msg_greater: .asciiz "So lon hon: "
    msg_sum:   .asciiz "Tong: "
    msg_diff:  .asciiz "Hieu: "
    msg_prod:  .asciiz "Tich: "
    msg_quot:  .asciiz "Thuong: "
    msg_rem:   .asciiz " (Du: "
    end_paren: .asciiz ")"
    newline:   .asciiz "\n"

.text
.globl main
main:
    li   $v0, 4
    la   $a0, prompt1
    syscall
    
    li   $v0, 5
    syscall
    move $t0, $v0
    
    li   $v0, 4
    la   $a0, prompt2
    syscall
    
    li   $v0, 5
    syscall
    move $t1, $v0
    
    li   $v0, 4
    la   $a0, newline
    syscall
    
    li   $v0, 4
    la   $a0, msg_greater
    syscall
    
    move $a0, $t0
    bge  $t0, $t1, print_greater
    move $a0, $t1
print_greater:
    li   $v0, 1
    syscall
    li   $v0, 4
    la   $a0, newline
    syscall

    li   $v0, 4
    la   $a0, msg_sum
    syscall
    add  $a0, $t0, $t1
    li   $v0, 1
    syscall
    li   $v0, 4
    la   $a0, newline
    syscall

    li   $v0, 4
    la   $a0, msg_diff
    syscall
    sub  $a0, $t0, $t1
    li   $v0, 1
    syscall
    li   $v0, 4
    la   $a0, newline
    syscall

    li   $v0, 4
    la   $a0, msg_prod
    syscall
    mult $t0, $t1
    mflo $a0
    li   $v0, 1
    syscall
    li   $v0, 4
    la   $a0, newline
    syscall

    li   $v0, 4
    la   $a0, msg_quot
    syscall
    div  $t0, $t1
    mflo $a0
    li   $v0, 1
    syscall

    li   $v0, 4
    la   $a0, msg_rem
    syscall
    mfhi $a0
    li   $v0, 1
    syscall
    
    li   $v0, 4
    la   $a0, end_paren
    syscall
    
    li   $v0, 10
    syscall