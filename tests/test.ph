function fact_rec(n: int) -> int {
    if (n <= 1) {
        return 1;
    }
    else {
        return n * fact_rec(n - 1);
    }
}

function fact_loop(n: int) -> int {
    f := 1;
    for (i := 1; i <= n; i++) {
        f *= i;
    }
    return f;
}
