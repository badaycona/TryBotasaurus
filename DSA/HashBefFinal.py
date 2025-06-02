def solve_rolling_hash():
    N, M, Q = map(int, input().split())
    grid = [input() for _ in range(N)]

    # Store virus patterns and their precomputed hashes
    # Using two hash functions to reduce collisions
    virus_data = {} # {pattern_str: (hash1, hash2)}
    
    # Parameters for rolling hash (chọn số nguyên tố lớn)
    P1, MOD1 = 31, 10**9 + 7
    P2, MOD2 = 37, 10**9 + 9
    
    # Precompute powers of P1, P2
    MAX_LEN = 10
    pow1 = [1] * (MAX_LEN + 1)
    pow2 = [1] * (MAX_LEN + 1)
    for i in range(1, MAX_LEN + 1):
        pow1[i] = (pow1[i-1] * P1) % MOD1
        pow2[i] = (pow2[i-1] * P2) % MOD2

    # Store original patterns to verify after hash match
    original_patterns = ["" for _ in range(Q)]
    # Map hashes to list of virus indices that have these hashes
    # {(h1, h2): [index1, index2]}
    hash_to_virus_indices = {}

    for i in range(Q):
        pattern = input()
        original_patterns[i] = pattern
        L = len(pattern)
        h1, h2 = 0, 0
        for char_idx in range(L):
            char_val = ord(pattern[char_idx]) - ord('a') + 1
            h1 = (h1 * P1 + char_val) % MOD1
            h2 = (h2 * P2 + char_val) % MOD2
        
        if (h1, h2) not in hash_to_virus_indices:
            hash_to_virus_indices[(h1, h2)] = []
        hash_to_virus_indices[(h1, h2)].append(i)

    found_viruses = [False] * Q

    # --- Check Horizontal ---
    for r in range(N):
        row_str = grid[r]
        for length in range(2, MAX_LEN + 1):
            if length > M: continue
            
            # Calculate initial hash for the first window of current length
            current_h1, current_h2 = 0, 0
            for k in range(length):
                char_val = ord(row_str[k]) - ord('a') + 1
                current_h1 = (current_h1 * P1 + char_val) % MOD1
                current_h2 = (current_h2 * P2 + char_val) % MOD2
            
            if (current_h1, current_h2) in hash_to_virus_indices:
                # Verify actual string match for all viruses with this hash pair
                segment_to_check = row_str[0:length]
                for virus_idx in hash_to_virus_indices[(current_h1, current_h2)]:
                    if not found_viruses[virus_idx] and original_patterns[virus_idx] == segment_to_check:
                        found_viruses[virus_idx] = True
            
            # Roll the hash
            for c_start in range(1, M - length + 1):
                char_val_remove = ord(row_str[c_start-1]) - ord('a') + 1
                char_val_add = ord(row_str[c_start + length - 1]) - ord('a') + 1
                
                current_h1 = (current_h1 - char_val_remove * pow1[length-1]) % MOD1
                current_h1 = (current_h1 * P1 + char_val_add) % MOD1
                if current_h1 < 0: current_h1 += MOD1 # Ensure positive

                current_h2 = (current_h2 - char_val_remove * pow2[length-1]) % MOD2
                current_h2 = (current_h2 * P2 + char_val_add) % MOD2
                if current_h2 < 0: current_h2 += MOD2 # Ensure positive

                if (current_h1, current_h2) in hash_to_virus_indices:
                    segment_to_check = row_str[c_start : c_start + length]
                    for virus_idx in hash_to_virus_indices[(current_h1, current_h2)]:
                         if not found_viruses[virus_idx] and original_patterns[virus_idx] == segment_to_check:
                            found_viruses[virus_idx] = True
    
    # --- Check Vertical ---
    # Build columns first, then apply the same rolling hash logic
    for c in range(M):
        col_str_list = [grid[r][c] for r in range(N)]
        col_str = "".join(col_str_list) # This might be slow if N is large, better to adapt rolling hash directly
        
        # Re-apply rolling hash logic for col_str (length N)
        # (Similar to horizontal part, replace M with N, row_str with col_str)
        for length in range(2, MAX_LEN + 1):
            if length > N: continue
            
            current_h1, current_h2 = 0, 0
            for k in range(length):
                char_val = ord(col_str[k]) - ord('a') + 1
                current_h1 = (current_h1 * P1 + char_val) % MOD1
                current_h2 = (current_h2 * P2 + char_val) % MOD2
            
            if (current_h1, current_h2) in hash_to_virus_indices:
                segment_to_check = col_str[0:length]
                for virus_idx in hash_to_virus_indices[(current_h1, current_h2)]:
                    if not found_viruses[virus_idx] and original_patterns[virus_idx] == segment_to_check:
                        found_viruses[virus_idx] = True
            
            for r_start in range(1, N - length + 1):
                char_val_remove = ord(col_str[r_start-1]) - ord('a') + 1
                char_val_add = ord(col_str[r_start + length - 1]) - ord('a') + 1
                
                current_h1 = (current_h1 - char_val_remove * pow1[length-1]) % MOD1
                current_h1 = (current_h1 * P1 + char_val_add) % MOD1
                if current_h1 < 0: current_h1 += MOD1

                current_h2 = (current_h2 - char_val_remove * pow2[length-1]) % MOD2
                current_h2 = (current_h2 * P2 + char_val_add) % MOD2
                if current_h2 < 0: current_h2 += MOD2

                if (current_h1, current_h2) in hash_to_virus_indices:
                    segment_to_check = col_str[r_start : r_start + length]
                    for virus_idx in hash_to_virus_indices[(current_h1, current_h2)]:
                         if not found_viruses[virus_idx] and original_patterns[virus_idx] == segment_to_check:
                            found_viruses[virus_idx] = True

    result_str = "".join(['1' if found else '0' for found in found_viruses])
    print(result_str)

solve_rolling_hash()