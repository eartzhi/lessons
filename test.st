VAR
    a: BYTE := 2#1000_0000;
    b: WORD;
    ar: ARRAY[0..4] OF INT;
    c: INT;

END_VAR
b := SHL(a, 1); (* Результат 0 *)
b := SHL(BYTE_TO_WORD(a), 1); (* Результат 256 *)
с := SIZEOF(ar);
