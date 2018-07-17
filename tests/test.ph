function fact_rec(n: int) -> int {
    struct Fact {
        count: int;
        cache: int[];
        result: int*;
    }
    if (n <= 1) {
        return 1;
    }
    else {
        return n * fact_rec(n - 1);
    }
}
