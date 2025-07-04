.data
    prompt_char:  .asciiz "Nhap ky tu (chi mot ky tu): "
    prompt_prev:  .asciiz "Ky tu truoc: "
    prompt_next:  .asciiz "Ky tu sau: "
    type_digit:   .asciiz "Loai: So"
    type_lower:   .asciiz "Loai: Chu thuong"
    type_upper:   .asciiz "Loai: Chu hoa"
    type_invalid: .asciiz "invalid type"
    newline:      .asciiz "\n"

.text
.globl main
main:
    li   $v0, 4
    la   $a0, prompt_char
    syscall

    li   $v0, 12
    syscall
    move $t0, $v0

    li   $v0, 4
    la   $a0, newline
    syscall

    li   $v0, 4
    la   $a0, prompt_prev
    syscall
    
    subi $a0, $t0, 1
    li   $v0, 11
    syscall

    li   $v0, 4
    la   $a0, newline
    syscall

    li   $v0, 4
    la   $a0, prompt_next
    syscall

    addi $a0, $t0, 1
    li   $v0, 11
    syscall

    li   $v0, 4
    la   $a0, newline
    syscall

    blt  $t0, '0', check_lower
    bgt  $t0, '9', check_lower
    li   $v0, 4
    la   $a0, type_digit
    syscall
    j    exit_program

check_lower:
    blt  $t0, 'a', check_upper
    bgt  $t0, 'z', check_upper
    li   $v0, 4
    la   $a0, type_lower
    syscall
    j    exit_program

check_upper:
    blt  $t0, 'A', invalid
    bgt  $t0, 'Z', invalid
    li   $v0, 4
    la   $a0, type_upper
    syscall
    j    exit_program

invalid:
    li   $v0, 4
    la   $a0, type_invalid
    syscall
    
exit_program:
    li   $v0, 10
    syscall